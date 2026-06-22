"""
db_connection.py — MySQL helper for EV Charging Station Demand Analysis
Fixed: switched from mysql-connector-python to PyMySQL to avoid
       caching_sha2_password auth plugin issues with MySQL 8.0+
"""

import os
import pandas as pd
import pymysql
import pymysql.cursors
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus

load_dotenv()

MYSQL_HOST     = os.getenv("MYSQL_HOST",     "localhost")
MYSQL_PORT     = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER     = os.getenv("MYSQL_USER",     "root")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "ev_charging_analysis")

MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
if not MYSQL_PASSWORD:
    raise ValueError(
        "MYSQL_PASSWORD environment variable is not set. "
        "Please add it to your .env file."
    )


def _connect(database=None):
    """Return a PyMySQL connection. Handles caching_sha2_password automatically."""
    kwargs = dict(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        autocommit=True,
        charset='utf8mb4',
    )
    if database:
        kwargs['database'] = database
    return pymysql.connect(**kwargs)


def get_engine():
    pwd = quote_plus(MYSQL_PASSWORD)
    url = (
        f"mysql+pymysql://{MYSQL_USER}:{pwd}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )
    return create_engine(url, echo=False)


def test_connection() -> bool:
    try:
        conn = _connect()
        conn.close()
        print("  MySQL connection: OK")
        return True
    except Exception as e:
        print(f"  Connection error: {e}")
        return False


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS ev_data (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    country             VARCHAR(200),
    state               VARCHAR(200),
    city                VARCHAR(200),
    year                INT,
    month               INT,
    population          FLOAT,
    population_density  FLOAT,
    ev_registrations    FLOAT,
    bev_registrations   FLOAT,
    phev_registrations  FLOAT,
    charging_stations   FLOAT,
    charging_points     FLOAT,
    latitude            FLOAT,
    longitude           FLOAT,
    ev_per_station      FLOAT,
    station_density     FLOAT,
    monthly_growth_pct  FLOAT,
    yoy_growth_pct      FLOAT,
    coverage_gap        FLOAT,
    demand_score        FLOAT,
    priority_score      FLOAT,
    infra_status        VARCHAR(100),
    city_tier           VARCHAR(100),
    ev_market_share_pct FLOAT,
    bev_share_pct       FLOAT,
    ev_stock_city       FLOAT,
    adoption_stage      VARCHAR(100)
)
"""

VIEW_SQLS = [
    (
        "v_top_priority_cities",
        """
        CREATE OR REPLACE VIEW v_top_priority_cities AS
        SELECT country, city,
               ROUND(AVG(priority_score), 2)    AS avg_priority_score,
               ROUND(AVG(coverage_gap), 2)      AS avg_coverage_gap,
               ROUND(AVG(ev_registrations), 1)  AS avg_ev_registrations,
               ROUND(AVG(charging_stations), 1) AS avg_charging_stations,
               MAX(infra_status)                AS latest_infra_status
        FROM ev_data
        GROUP BY country, city
        ORDER BY avg_priority_score DESC
        LIMIT 20
        """
    ),
    (
        "v_infra_status_profile",
        """
        CREATE OR REPLACE VIEW v_infra_status_profile AS
        SELECT infra_status,
               COUNT(*)                          AS row_count,
               COUNT(DISTINCT city)              AS city_count,
               ROUND(AVG(priority_score),  2)   AS avg_priority_score,
               ROUND(AVG(coverage_gap),    2)   AS avg_coverage_gap,
               ROUND(AVG(ev_per_station),  2)   AS avg_ev_per_station,
               ROUND(AVG(ev_registrations), 1)  AS avg_ev_registrations
        FROM ev_data
        GROUP BY infra_status
        ORDER BY avg_priority_score DESC
        """
    ),
    (
        "v_charging_deserts",
        """
        CREATE OR REPLACE VIEW v_charging_deserts AS
        SELECT country, city,
               ROUND(AVG(ev_registrations), 1)  AS avg_ev_reg,
               ROUND(AVG(charging_stations), 1) AS avg_stations,
               ROUND(AVG(coverage_gap), 2)      AS avg_coverage_gap,
               ROUND(AVG(ev_per_station), 2)    AS avg_ev_per_station,
               MAX(infra_status)                AS infra_status
        FROM ev_data
        WHERE infra_status IN ('Critical Gap', 'Needs Attention')
        GROUP BY country, city
        ORDER BY avg_coverage_gap DESC
        LIMIT 20
        """
    ),
    (
        "v_city_tier_gap",
        """
        CREATE OR REPLACE VIEW v_city_tier_gap AS
        SELECT city_tier,
               COUNT(DISTINCT city)              AS city_count,
               ROUND(AVG(ev_registrations), 1)  AS avg_ev_reg,
               ROUND(AVG(charging_stations), 1) AS avg_stations,
               ROUND(AVG(coverage_gap), 2)      AS avg_coverage_gap,
               ROUND(AVG(priority_score), 2)    AS avg_priority_score
        FROM ev_data
        GROUP BY city_tier
        ORDER BY avg_priority_score DESC
        """
    ),
]


def ensure_schema(verbose: bool = True):
    """Create database + table + views using PyMySQL."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}`")
    cur.execute(f"USE `{MYSQL_DATABASE}`")
    if verbose:
        print(f"  Database `{MYSQL_DATABASE}` ready.")

    cur.execute(CREATE_TABLE_SQL)
    if verbose:
        print("  Table `ev_data` ready.")

    for name, view_sql in VIEW_SQLS:
        cur.execute(view_sql)
        if verbose:
            print(f"  View `{name}` created/replaced.")

    cur.close()
    conn.close()
    if verbose:
        print("  ensure_schema() complete — DB + table + views ready.")


def upload_csv_to_mysql(csv_path: str) -> int:
    """Truncate ev_data and bulk-insert from CSV. Returns row count inserted."""
    df = pd.read_csv(csv_path)

    # Normalize infra_status casing
    if "infra_status" in df.columns:
        status_map = {
            "adequate":        "Adequate",
            "needs attention": "Needs Attention",
            "critical gap":    "Critical Gap",
        }
        df["infra_status"] = (
            df["infra_status"]
            .str.strip()
            .apply(lambda v: status_map.get(str(v).lower(), v) if pd.notna(v) else v)
        )

    # Replace NaN with None for MySQL NULL
    df = df.where(pd.notnull(df), None)

    conn = _connect(database=MYSQL_DATABASE)
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE ev_data")

    cols         = [c for c in df.columns if c != 'id']
    placeholders = ', '.join(['%s'] * len(cols))
    col_names    = ', '.join([f'`{c}`' for c in cols])
    insert_sql   = f"INSERT INTO ev_data ({col_names}) VALUES ({placeholders})"

    rows = [tuple(r) for r in df[cols].values]
    cur.executemany(insert_sql, rows)

    cur.execute("SELECT COUNT(*) FROM ev_data")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()

    print(f"  Uploaded {count:,} rows to `ev_data`.")
    return count
