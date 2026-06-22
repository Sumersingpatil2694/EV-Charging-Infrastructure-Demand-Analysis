"""
EV Charging Station Demand Analysis
Premium Streamlit dashboard with NVIDIA-inspired dark theme.
"""

from pathlib import Path
import re

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EV Charging Infrastructure Demand Analysis",
    page_icon="🔋⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# THEME + LABELS
# -----------------------------------------------------------------------------
THEME = {
    "bg": "#080B07",
    "surface": "#0F140E",
    "surface_2": "#151D14",
    "card": "#101710",
    "grid": "rgba(162, 196, 140, 0.16)",
    "text": "#F5FFF0",
    "muted": "#A7B8A0",
    "divider": "#1C2A19",
    "demand": "#76B900",      # green
    "infra": "#3DDB84",       # light green
    "risk": "#FF6B6B",        # risk red
    "attention": "#FFC857",   # amber
    "adequate": "#7CFF8A",    # adequacy green
    "accent": "#B8FF5C",
}

PROJECT_NAME = "EV Charging Infrastructure Demand Analysis"
PORTFOLIO_LINKS = {
    "GitHub": "https://github.com/Sumersingpatil2694",
    "LinkedIn": "https://www.linkedin.com/in/sumersing-patil-ai/",
}


STATUS_COLORS = {
    "Critical Gap": THEME["risk"],
    "Needs Attention": THEME["attention"],
    "Adequate": THEME["adequate"],
}

COUNTRY_NAME_FIXES = {
    "czech republic": "Czech Republic",
    "czech_republic": "Czech Republic",
    "the czech republic": "Czech Republic",
    "uk": "United Kingdom",
    "u k": "United Kingdom",
    "united kingdom": "United Kingdom",
    "uae": "United Arab Emirates",
    "u a e": "United Arab Emirates",
    "usa": "United States",
    "u s a": "United States",
    "us": "United States",
}

LABEL_MAP = {
    "country": "Country",
    "state": "State",
    "city": "City",
    "date": "Date",
    "year": "Year",
    "month": "Month",
    "month_name": "Month Name",
    "quarter": "Quarter",
    "population": "Population",
    "population_density": "Population Density",
    "ev_registrations": "EV Registrations",
    "bev_registrations": "Battery EV Registrations",
    "phev_registrations": "Plug-in Hybrid EV Registrations",
    "charging_stations": "Charging Stations",
    "charging_points": "Charging Points",
    "ev_per_station": "EVs per Station",
    "station_density": "Station Density",
    "monthly_growth_pct": "Monthly EV Growth (%)",
    "yoy_growth_pct": "Year-over-Year EV Growth (%)",
    "coverage_gap": "Coverage Gap",
    "demand_score": "Demand Score",
    "priority_score": "Priority Score",
    "infra_status": "Infrastructure Status",
    "city_tier": "City Tier",
    "ev_market_share_pct": "EV Market Share (%)",
    "bev_share_pct": "Battery EV Share (%)",
    "adoption_stage": "Adoption Stage",
    "ev_stock_city": "City EV Stock",
    "month_sin": "Seasonality Signal (Sine)",
    "month_cos": "Seasonality Signal (Cosine)",
    "ev_registrations_lag1": "EV Registrations (Previous Month)",
    "ev_registrations_lag3": "EV Registrations (3 Months Ago)",
    "bev_registrations_lag1": "Battery EV Registrations (Previous Month)",
    "bev_registrations_lag3": "Battery EV Registrations (3 Months Ago)",
    "phev_registrations_lag1": "Plug-in Hybrid EV Registrations (Previous Month)",
    "phev_registrations_lag3": "Plug-in Hybrid EV Registrations (3 Months Ago)",
    "charging_stations_lag1": "Charging Stations (Previous Month)",
    "charging_stations_lag3": "Charging Stations (3 Months Ago)",
    "charging_points_lag1": "Charging Points (Previous Month)",
    "charging_points_lag3": "Charging Points (3 Months Ago)",
    "monthly_growth_pct_lag1": "Monthly EV Growth (Previous Month)",
    "monthly_growth_pct_lag3": "Monthly EV Growth (3 Months Ago)",
    "yoy_growth_pct_lag1": "YoY EV Growth (Previous Month)",
    "yoy_growth_pct_lag3": "YoY EV Growth (3 Months Ago)",
    "demand_score_lag1": "Demand Score (Previous Month)",
    "demand_score_lag3": "Demand Score (3 Months Ago)",
    "priority_score_lag1": "Priority Score (Previous Month)",
    "priority_score_lag3": "Priority Score (3 Months Ago)",
    "ev_registrations_roll3_mean": "EV Registrations (3-Month Average)",
    "charging_stations_roll3_mean": "Charging Stations (3-Month Average)",
    "demand_score_roll3_mean": "Demand Score (3-Month Average)",
    "priority_score_roll3_mean": "Priority Score (3-Month Average)",
    "city_avg_ev": "City Average EV Demand",
    "city_avg_gap": "City Average Coverage Gap",
    "city_avg_priority": "City Average Priority Score",
    "avg_priority": "Average Priority Score",
    "avg_gap": "Average Coverage Gap",
    "avg_ev_reg": "Average EV Registrations",
    "avg_stations": "Average Charging Stations",
    "avg_ev_per_st": "Average EVs per Station",
    "total_ev": "Total EV Registrations",
    "total_stations": "Total Charging Stations",
    "total_st": "Total Charging Stations",
    "yoy_ev_pct": "YoY EV Growth (%)",
    "yoy_st_pct": "YoY Station Growth (%)",
    "ev_reg": "EV Registrations",
    "stations": "Charging Stations",
    "demand": "Demand Score",
    "priority": "Priority Score",
}


# -----------------------------------------------------------------------------
# STYLING
# -----------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
        :root {{
            --bg: {THEME['bg']};
            --surface: {THEME['surface']};
            --surface-2: {THEME['surface_2']};
            --card: {THEME['card']};
            --text: {THEME['text']};
            --muted: {THEME['muted']};
            --divider: {THEME['divider']};
            --demand: {THEME['demand']};
            --infra: {THEME['infra']};
            --risk: {THEME['risk']};
            --attention: {THEME['attention']};
            --adequate: {THEME['adequate']};
            --accent: {THEME['accent']};
        }}

        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background: linear-gradient(180deg, #060906 0%, #0A0F09 100%);
            color: var(--text);
        }}

        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0B100A 0%, #101710 100%);
            border-right: 1px solid rgba(118, 185, 0, 0.14);
        }}

        .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }}

        h1, h2, h3, h4, h5, h6, p, label, div, span {{
            color: var(--text);
        }}

        div[data-testid="stSidebarNav"] {{ display: none; }}

        .hero-wrap {{
            background:
                radial-gradient(circle at top right, rgba(118,185,0,0.18), transparent 30%),
                linear-gradient(135deg, rgba(118,185,0,0.08), rgba(61,219,132,0.04));
            border: 1px solid rgba(118,185,0,0.18);
            border-radius: 22px;
            padding: 1.4rem 1.4rem 1.1rem 1.4rem;
            margin-bottom: 1.4rem;
        }}

        .hero-title {{
            font-size: 2.25rem;
            font-weight: 900;
            margin-bottom: 0.2rem;
            letter-spacing: -0.03em;
        }}

        .hero-subtitle {{
            font-size: 1rem;
            color: var(--muted);
            margin-bottom: 0;
        }}

        .section-divider {{
            height: 1px;
            width: 100%;
            background: linear-gradient(90deg, rgba(118,185,0,0.65), rgba(118,185,0,0.08));
            margin: 0.65rem 0 1.25rem 0;
        }}

        .section-title {{
            font-size: 1.45rem;
            font-weight: 800;
            margin-top: 0.35rem;
            margin-bottom: 0.25rem;
        }}

        .section-caption {{
            color: var(--muted);
            margin-bottom: 1rem;
            font-size: 0.96rem;
        }}

        .kpi-card {{
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 0.35rem;
            background:
                radial-gradient(circle at top left, rgba(184,255,92,0.10), transparent 34%),
                linear-gradient(180deg, rgba(20,28,19,0.98), rgba(10,14,9,0.98));
            border: 1px solid rgba(118,185,0,0.18);
            border-radius: 16px;
            padding: 0.7rem 0.85rem 0.65rem 0.85rem;
            min-height: 110px;
            height: 100%;
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.05),
                inset 0 -1px 0 rgba(118,185,0,0.05),
                0 18px 34px rgba(0,0,0,0.30),
                0 8px 18px rgba(118,185,0,0.08);
        }}

        .kpi-card::before {{
            content: "";
            position: absolute;
            inset: 0;
            pointer-events: none;
            background: linear-gradient(135deg, rgba(255,255,255,0.06), transparent 28%, transparent 72%, rgba(118,185,0,0.08));
        }}

        .kpi-label {{
            color: var(--muted);
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 800;
            margin-bottom: 0.15rem;
        }}

        .kpi-value {{
            font-size: clamp(1.55rem, 1.75vw, 1.85rem);
            line-height: 1.08;
            font-weight: 900;
            letter-spacing: -0.03em;
            min-height: 3.4rem;
            display: flex;
            align-items: flex-end;
            margin-bottom: 0;
            word-break: break-word;
        }}

        .kpi-value.kpi-value--compact {{
            font-size: clamp(1.35rem, 1.6vw, 1.65rem);
        }}

        .kpi-sub {{
            color: var(--muted);
            font-size: 0.79rem;
            line-height: 1.3;
            min-height: 1.6rem;
        }}

        .kpi-delta {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            width: fit-content;
            font-size: 0.78rem;
            font-weight: 800;
            border-radius: 999px;
            padding: 0.22rem 0.52rem;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
        }}

        .empty-state-box {{
            background: linear-gradient(180deg, rgba(19,28,18,0.92), rgba(10,14,9,0.96));
            border: 1px solid rgba(255,107,107,0.20);
            border-left: 4px solid var(--attention);
            border-radius: 18px;
            padding: 1rem 1.05rem;
            margin-top: 0.9rem;
        }}

        .footer-links {{
            margin-top: 0.35rem;
            display: flex;
            justify-content: center;
            gap: 0.9rem;
            flex-wrap: wrap;
        }}

        .footer-links a {{
            color: var(--accent);
            text-decoration: none;
            font-weight: 700;
        }}

        .info-chip {{
            display: inline-block;
            font-size: 0.82rem;
            color: var(--text);
            background: rgba(118,185,0,0.10);
            border: 1px solid rgba(118,185,0,0.16);
            padding: 0.25rem 0.55rem;
            border-radius: 999px;
            margin-right: 0.4rem;
            margin-bottom: 0.35rem;
        }}

        .insight-box {{
            background: linear-gradient(180deg, rgba(19,28,18,0.9), rgba(10,14,9,0.95));
            border: 1px solid rgba(118,185,0,0.12);
            border-left: 4px solid var(--demand);
            border-radius: 16px;
            padding: 0.9rem 1rem;
            color: var(--text);
            margin-top: 0.8rem;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.4rem;
            background: rgba(15,20,14,0.75);
            padding: 0.4rem;
            border-radius: 16px;
            border: 1px solid rgba(118,185,0,0.12);
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 12px;
            padding: 0.6rem 1rem;
            color: var(--muted);
        }}

        .stTabs [aria-selected="true"] {{
            background: rgba(118,185,0,0.14) !important;
            color: var(--text) !important;
        }}

        div[data-testid="stMetric"] {{
            background: transparent;
            border: none;
            padding: 0;
        }}

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        .stMultiSelect div[data-baseweb="select"] > div,
        .stDateInput > div,
        .stSlider > div,
        .stSelectbox > div > div,
        .stTextInput > div > div {{
            background: linear-gradient(180deg, rgba(17,24,17,0.96), rgba(10,14,9,0.98)) !important;
            color: var(--text) !important;
            border-radius: 14px !important;
            border: 1px solid rgba(118,185,0,0.20) !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 6px 16px rgba(0,0,0,0.18) !important;
        }}

        .stMultiSelect label,
        .stSlider label,
        .stSelectbox label {{
            font-weight: 700 !important;
            color: var(--text) !important;
        }}

        .stMultiSelect [data-baseweb="tag"] {{
            background: linear-gradient(135deg, rgba(118,185,0,0.95), rgba(184,255,92,0.88)) !important;
            border: 1px solid rgba(184,255,92,0.55) !important;
            border-radius: 999px !important;
            color: #091006 !important;
            font-weight: 800 !important;
            box-shadow: 0 8px 16px rgba(118,185,0,0.18) !important;
        }}

        .stMultiSelect [data-baseweb="tag"] span,
        .stMultiSelect [data-baseweb="tag"] svg {{
            color: #091006 !important;
            fill: #091006 !important;
        }}

        div[data-baseweb="slider"] [role="slider"] {{
            background: radial-gradient(circle at 30% 30%, #E8FFC2, var(--accent)) !important;
            border: 2px solid rgba(118,185,0,0.82) !important;
            box-shadow: 0 0 0 4px rgba(118,185,0,0.16), 0 8px 18px rgba(118,185,0,0.22) !important;
        }}

        div[data-baseweb="slider"] > div > div > div {{
            background: linear-gradient(90deg, rgba(118,185,0,0.92), rgba(184,255,92,0.85)) !important;
        }}

        .sidebar-section-title {{
            margin-top: 1rem;
            margin-bottom: 0.3rem;
            font-size: 0.84rem;
            font-weight: 900;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            color: var(--accent);
        }}

        .sidebar-section-note {{
            font-size: 0.8rem;
            color: var(--muted);
            margin-bottom: 0.35rem;
        }}

        .tier-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.55rem;
            margin: 0.35rem 0 0.3rem 0;
        }}

        .tier-card {{
            background: linear-gradient(180deg, rgba(18,25,17,0.96), rgba(10,14,9,0.98));
            border: 1px solid rgba(118,185,0,0.14);
            border-radius: 16px;
            padding: 0.75rem 0.8rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 8px 20px rgba(0,0,0,0.16);
        }}

        .tier-card.tier-card--active {{
            border-color: rgba(184,255,92,0.55);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 12px 24px rgba(118,185,0,0.10);
        }}

        .tier-card-title {{
            font-size: 0.92rem;
            font-weight: 800;
            color: var(--text);
        }}

        .tier-card-meta {{
            font-size: 0.78rem;
            color: var(--muted);
            margin-top: 0.2rem;
        }}

        .stDataFrame, div[data-testid="stTable"] {{
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid rgba(118,185,0,0.10);
        }}

        .footer-note {{
            color: var(--muted);
            font-size: 0.88rem;
            text-align: center;
            padding-top: 0.5rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def smart_title(text: str) -> str:
    words = text.split()
    small_words = {"and", "of", "the", "de", "la", "da", "di"}
    titled = []
    for idx, word in enumerate(words):
        if word.isupper() and len(word) <= 3:
            titled.append(word)
        elif idx > 0 and word.lower() in small_words:
            titled.append(word.lower())
        else:
            titled.append(word.capitalize())
    return " ".join(titled)


def canonicalize_country_name(value: object) -> object:
    if pd.isna(value):
        return value
    text = str(value).replace("_", " ").replace("-", " ")
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return text
    lowered = text.casefold()
    if lowered in COUNTRY_NAME_FIXES:
        return COUNTRY_NAME_FIXES[lowered]
    return smart_title(text.lower())


def canonicalize_city_tier(value: object) -> object:
    if pd.isna(value):
        return value
    text = re.sub(r"\s+", " ", str(value)).strip()
    match = re.search(r"(\d+)", text)
    if match:
        return f"Tier {match.group(1)}"
    return smart_title(text.lower())


def render_tier_cards(options: list[str], selected: list[str], frame: pd.DataFrame) -> str:
    tier_counts = frame["city_tier"].value_counts(dropna=False).to_dict() if "city_tier" in frame.columns else {}
    cards = []
    for tier in options:
        active = " tier-card--active" if tier in selected else ""
        count = int(tier_counts.get(tier, 0))
        label = "cities" if count != 1 else "city"
        cards.append(
            f"<div class='tier-card{active}'><div class='tier-card-title'>{tier}</div><div class='tier-card-meta'>{count} {label}</div></div>"
        )
    return "<div class='tier-grid'>" + "".join(cards) + "</div>"


def fmt_number(value: float, digits: int = 0) -> str:
    if pd.isna(value):
        return "—"
    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{value/1_000:.1f}K"
    return f"{value:,.{digits}f}" if digits else f"{value:,.0f}"


def pretty_label(col_name: str) -> str:
    return LABEL_MAP.get(col_name, col_name.replace("_", " ").title())


def rename_for_display(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.rename(columns={col: pretty_label(col) for col in frame.columns})


def section_header(title: str, caption: str = "") -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="section-caption">{caption}</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


def kpi_card(
    label: str,
    value: str,
    subtext: str,
    accent: str,
    delta_text: str | None = None,
    delta_color: str | None = None,
) -> str:
    import html as _html
    safe_label = _html.escape(str(label))
    safe_value = _html.escape(str(value))
    safe_subtext = _html.escape(str(subtext))
    value_class = ""  # kept for compatibility, inline styles used below
    delta_html = ""
    if delta_text:
        chip_color = delta_color or accent
        safe_delta = _html.escape(str(delta_text))
        delta_html = f"<div class='kpi-delta' style='color:{chip_color}; border-color:{chip_color};'>{safe_delta}</div>"
    font_size = "clamp(1.55rem, 1.75vw, 1.85rem)" if len(str(value)) <= 12 else "clamp(1.35rem, 1.6vw, 1.65rem)"
    delta_html_out = ""
    if delta_text:
        chip_color = delta_color or accent
        safe_delta = _html.escape(str(delta_text))
        delta_html_out = f'<div class="kpi-wrap-delta" style="color:{chip_color}; border-color:{chip_color};">{safe_delta}</div>'
    return f"""
    <div class="kpi-wrap" style="border-top: 3px solid {accent};">
        <div class="kpi-wrap-label">{safe_label}</div>
        <div class="kpi-wrap-value" style="color:{accent}; font-size:{font_size};">{safe_value}</div>
        {delta_html_out}
        <div class="kpi-wrap-sub">{safe_subtext}</div>
    </div>
    """


def apply_chart_theme(fig: go.Figure, height: int = 420, legend_title: str | None = None) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=THEME["surface"],
        font=dict(color=THEME["text"], family="Inter, Segoe UI, sans-serif"),
        title_font=dict(size=20, color=THEME["text"]),
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=THEME["muted"]),
            title=legend_title,
        ),
        hoverlabel=dict(bgcolor="#0E130D", bordercolor=THEME["demand"], font_color=THEME["text"]),
        xaxis=dict(
            showgrid=True,
            gridcolor=THEME["grid"],
            zeroline=False,
            title_font=dict(color=THEME["muted"]),
            tickfont=dict(color=THEME["muted"]),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=THEME["grid"],
            zeroline=False,
            title_font=dict(color=THEME["muted"]),
            tickfont=dict(color=THEME["muted"]),
        ),
    )
    return fig


def make_metric_chip(label: str) -> str:
    return f'<span class="info-chip">{label}</span>'


def make_download_payload(frame: pd.DataFrame) -> bytes:
    return frame.to_csv(index=False).encode("utf-8")


def compute_delta_badge(frame: pd.DataFrame, metric: str, agg: str = "sum") -> tuple[str | None, str]:
    if metric not in frame.columns or frame.empty or "date" not in frame.columns:
        return None, THEME["muted"]

    ordered = frame.sort_values("date").copy()
    midpoint = len(ordered) // 2
    if midpoint <= 0 or midpoint >= len(ordered):
        return None, THEME["muted"]

    first = ordered.iloc[:midpoint][metric]
    second = ordered.iloc[midpoint:][metric]
    before = first.sum() if agg == "sum" else first.mean()
    after = second.sum() if agg == "sum" else second.mean()

    if pd.isna(before) or pd.isna(after):
        return None, THEME["muted"]
    if before == 0:
        if after == 0:
            return "• 0.0% vs early period", THEME["muted"]
        return "▲ New vs early period", THEME["demand"]

    delta_pct = ((after - before) / abs(before)) * 100
    arrow = "▲" if delta_pct >= 0 else "▼"
    color = THEME["demand"] if delta_pct >= 0 else THEME["risk"]
    return f"{arrow} {abs(delta_pct):.1f}% vs early period", color


def prepare_forecast_frame(frame: pd.DataFrame | None) -> pd.DataFrame | None:
    if frame is None or frame.empty:
        return None

    renamed = frame.copy()
    lower_map = {str(col).lower(): col for col in renamed.columns}
    rename_map = {}
    if "ds" in lower_map and "date" not in renamed.columns:
        rename_map[lower_map["ds"]] = "date"
    if "yhat" in lower_map and "forecast" not in renamed.columns:
        rename_map[lower_map["yhat"]] = "forecast"
    if "yhat_lower" in lower_map and "forecast_lower" not in renamed.columns:
        rename_map[lower_map["yhat_lower"]] = "forecast_lower"
    if "yhat_upper" in lower_map and "forecast_upper" not in renamed.columns:
        rename_map[lower_map["yhat_upper"]] = "forecast_upper"
    if rename_map:
        renamed = renamed.rename(columns=rename_map)

    if "date" in renamed.columns:
        renamed["date"] = pd.to_datetime(renamed["date"], errors="coerce")
        renamed = renamed.dropna(subset=["date"]).sort_values("date")
        renamed["date"] = renamed["date"].dt.strftime("%Y-%m-%d")

    return renamed

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame | None:
    data_paths = [
        # Streamlit Cloud — app/ folder ke andar se relative paths
        "Outputs/Data/ev_data_cleaned_final.csv",
        "../Outputs/Data/ev_data_cleaned_final.csv",
        "Data/europe_ev_dataset.csv",
        "../Data/europe_ev_dataset.csv",
        # Local / fallback paths
        "ev_data_cleaned_final.csv",
        "europe_ev_dataset.csv",
        "data/ev_data_cleaned_final.csv",
        "data/europe_ev_dataset.csv",
        "../ev_data_cleaned_final.csv",
        "../europe_ev_dataset.csv",
        # Root level cleaned file
        "Outputs/cleaned_ev_data.csv",
        "../Outputs/cleaned_ev_data.csv",
    ]

    for path in data_paths:
        if Path(path).exists():
            df = pd.read_csv(path)
            df.columns = [str(c).strip() for c in df.columns]

            if "country" in df.columns:
                df["country"] = df["country"].apply(canonicalize_country_name)
            if "city" in df.columns:
                df["city"] = df["city"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip().str.title()
            if "infra_status" in df.columns:
                df["infra_status"] = (
                    df["infra_status"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip().str.title()
                )
            if "city_tier" in df.columns:
                df["city_tier"] = df["city_tier"].apply(canonicalize_city_tier)

            if "month" in df.columns:
                df = df[df["month"].between(1, 12)].copy()
            if "year" in df.columns:
                df = df[df["year"].between(2000, 2035)].copy()

            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
            elif {"year", "month"}.issubset(df.columns):
                df["date"] = pd.to_datetime(dict(year=df["year"], month=df["month"], day=1), errors="coerce")

            df = df.dropna(subset=["date"]).copy()
            return df.sort_values("date")
    return None


@st.cache_data(show_spinner=False)
def load_optional_csv(file_name: str) -> pd.DataFrame | None:
    candidate_paths = [
        # Streamlit Cloud paths (app/ folder ke andar se)
        f"Outputs/Model Outputs/{file_name}",
        f"../Outputs/Model Outputs/{file_name}",
        f"Outputs/Data/{file_name}",
        f"../Outputs/Data/{file_name}",
        # Local / fallback paths
        file_name,
        f"data/{file_name}",
        f"../{file_name}",
        f"outputs/models/{file_name}",
        f"outputs/{file_name}",
    ]
    for candidate in candidate_paths:
        if Path(candidate).exists():
            return pd.read_csv(candidate)
    return None


@st.cache_data(show_spinner=False)
def build_country_summary(frame: pd.DataFrame) -> pd.DataFrame:
    summary = (
        frame.groupby("country")
        .agg(
            total_ev=("ev_registrations", "sum"),
            total_st=("charging_stations", "sum"),
            avg_gap=("coverage_gap", "mean"),
            avg_priority=("priority_score", "mean"),
            ev_share=("ev_market_share_pct", "mean"),
        )
        .reset_index()
    )
    return summary.round(2)


@st.cache_data(show_spinner=False)
def build_city_summary(frame: pd.DataFrame) -> pd.DataFrame:
    city_summary = (
        frame.groupby(["country", "city", "infra_status", "city_tier"])
        .agg(
            avg_priority=("priority_score", "mean"),
            avg_gap=("coverage_gap", "mean"),
            avg_ev_reg=("ev_registrations", "mean"),
            avg_stations=("charging_stations", "mean"),
            avg_ev_per_st=("ev_per_station", "mean"),
            demand_score=("demand_score", "mean"),
        )
        .reset_index()
        .round(2)
    )
    return city_summary


@st.cache_data(show_spinner=False)
def build_monthly_summary(frame: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        frame.groupby(["date", "country"])
        .agg(
            ev_reg=("ev_registrations", "sum"),
            stations=("charging_stations", "sum"),
            demand=("demand_score", "mean"),
            priority=("priority_score", "mean"),
            gap=("coverage_gap", "mean"),
        )
        .reset_index()
    )
    return monthly


@st.cache_data(show_spinner=False)
def compute_feature_importance(frame: pd.DataFrame):
    feature_candidates = [
        "ev_registrations_roll3_mean",
        "ev_registrations_lag1",
        "ev_registrations_lag3",
        "monthly_growth_pct",
        "city_avg_ev",
        "charging_stations",
        "yoy_growth_pct",
        "demand_score",
        "month_cos",
        "charging_points",
        "month_sin",
        "month",
        "station_density",
        "ev_per_station",
        "year",
        "coverage_gap",
        "priority_score",
        "charging_stations_roll3_mean",
        "city_avg_gap",
        "city_avg_priority",
    ]

    usable = [col for col in feature_candidates if col in frame.columns]
    if len(usable) < 5 or "ev_registrations" not in frame.columns:
        return None, None

    model_note = "Feature signal computed from a cached surrogate model."

    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        from sklearn.model_selection import train_test_split

        work = frame[usable + ["ev_registrations"]].copy()
        work = work.replace([np.inf, -np.inf], np.nan)
        for col in usable:
            work[col] = pd.to_numeric(work[col], errors="coerce")
            work[col] = work[col].fillna(work[col].median())
        work = work.dropna(subset=["ev_registrations"])

        if len(work) > 10000:
            work = work.sample(10000, random_state=42)

        X = work[usable]
        y = work["ev_registrations"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(
            n_estimators=180,
            max_depth=12,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
        )
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        importance = (
            pd.DataFrame({"feature": usable, "importance": model.feature_importances_})
            .sort_values("importance", ascending=False)
            .head(15)
        )
        metrics = {
            "R²": round(r2_score(y_test, preds), 4),
            "MAE": round(mean_absolute_error(y_test, preds), 2),
            "RMSE": round(mean_squared_error(y_test, preds) ** 0.5, 2),
            "note": model_note,
        }
        return importance, metrics
    except Exception:
        corr = frame[usable + ["ev_registrations"]].corr(numeric_only=True)["ev_registrations"].drop("ev_registrations")
        importance = corr.abs().sort_values(ascending=False).head(15).reset_index()
        importance.columns = ["feature", "importance"]
        metrics = {"R²": "—", "MAE": "—", "RMSE": "—", "note": "Fallback to absolute correlation strength."}
        return importance, metrics


# -----------------------------------------------------------------------------
# LOAD FILES
# -----------------------------------------------------------------------------
df = load_data()
models_summary = load_optional_csv("models_summary.csv")
forecast_df = prepare_forecast_frame(load_optional_csv("forecast.csv"))

if df is None:
    st.error("❌ Data file not found. Place `ev_data_cleaned_final.csv` or `europe_ev_dataset.csv` in the same folder as `app.py`.")
    st.stop()


# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ EV Command Center")
    st.caption("Premium black dashboard · neon green filter system")
    st.markdown(
        "<div style='padding:0.75rem 0 0.2rem 0;'>"
        f"{make_metric_chip('EV Demand')}"
        f"{make_metric_chip('Charging Infra')}"
        f"{make_metric_chip('Investment Risk')}"
        f"{make_metric_chip('Adequacy')}"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='sidebar-section-title'>Geography</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section-note'>Standardized country names and premium green chips for cleaner comparison.</div>", unsafe_allow_html=True)
    all_countries = sorted(df["country"].dropna().unique())
    default_countries = all_countries[:8] if len(all_countries) > 8 else all_countries
    selected_countries = st.multiselect(
        "Country Filter",
        options=all_countries,
        default=default_countries,
        help="Choose the markets you want to compare.",
    )
    st.caption(f"{len(selected_countries)} selected · {len(all_countries)} total markets")

    city_query = st.text_input(
        "Search City",
        value="",
        placeholder="e.g. Berlin, Amsterdam",
        help="Type a full or partial city name to focus the dashboard.",
    ).strip()

    year_min = int(df["year"].min())
    year_max = int(df["year"].max())
    st.markdown("<div class='sidebar-section-title'>Timeline</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section-note'>Green range control for the dashboard time window.</div>", unsafe_allow_html=True)
    selected_years = st.slider(
        "Year Range",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
    )

    tier_options = sorted(
        df["city_tier"].dropna().unique(),
        key=lambda x: int(re.search(r"(\d+)", str(x)).group(1)) if re.search(r"(\d+)", str(x)) else 999,
    )
    st.markdown("<div class='sidebar-section-title'>City Classification</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section-note'>Tier 1–4 cards now follow the same premium visual language.</div>", unsafe_allow_html=True)
    selected_tiers = st.multiselect(
        "City Tier",
        options=tier_options,
        default=tier_options,
    )
    st.markdown(render_tier_cards(tier_options, selected_tiers, df), unsafe_allow_html=True)

    st.markdown("<div class='sidebar-section-title'>Infrastructure</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section-note'>Filter adequacy and infrastructure risk states.</div>", unsafe_allow_html=True)
    selected_infra = st.multiselect(
        "Infrastructure Status",
        options=sorted(df["infra_status"].dropna().unique()),
        default=sorted(df["infra_status"].dropna().unique()),
    )

    ev_station_threshold = None
    if "ev_per_station" in df.columns and df["ev_per_station"].notna().any():
        evps_series = df["ev_per_station"].dropna()
        evps_min = float(max(0, evps_series.min()))
        evps_max = float(evps_series.max())
        st.markdown("<div class='sidebar-section-title'>Charging Desert Control</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-section-note'>Only keep cities above a minimum EV-per-station stress level.</div>", unsafe_allow_html=True)
        ev_station_threshold = st.slider(
            "Minimum EVs per Station",
            min_value=evps_min,
            max_value=evps_max,
            value=evps_min,
        )

    st.markdown("---")
    summary_html = (
        "<div style='padding:0.1rem 0 0.1rem 0;'>"
        + make_metric_chip(f"Rows {len(df):,}")
        + make_metric_chip(f"Countries {df['country'].nunique()}")
        + make_metric_chip(f"Cities {df['city'].nunique()}")
        + make_metric_chip(f"Coverage {year_min}–{year_max}")
        + "</div>"
    )
    st.markdown(summary_html, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# FILTERED FRAME
# -----------------------------------------------------------------------------
mask = (
    df["country"].isin(selected_countries)
    & df["year"].between(selected_years[0], selected_years[1])
    & df["city_tier"].isin(selected_tiers)
    & df["infra_status"].isin(selected_infra)
)
if city_query:
    mask &= df["city"].fillna("").str.contains(city_query, case=False, regex=False)
if ev_station_threshold is not None and "ev_per_station" in df.columns:
    mask &= df["ev_per_station"].fillna(-np.inf) >= ev_station_threshold

fdf = df.loc[mask].copy()
if fdf.empty:
    st.markdown(
        """
        <div class="empty-state-box">
            <b>No data matches the current filter stack.</b><br>
            Try widening the year range, lowering the EV-per-station threshold, clearing the city search, or selecting more countries and tier groups.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

country_summary = build_country_summary(fdf)
city_summary = build_city_summary(fdf)
monthly_summary = build_monthly_summary(fdf)
feature_importance, feature_metrics = compute_feature_importance(fdf)

with st.sidebar:
    st.markdown("<div class='sidebar-section-title'>Export</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section-note'>Download the current filtered dataset or the priority-city summary.</div>", unsafe_allow_html=True)
    st.download_button(
        "⬇ Download Filtered Data (CSV)",
        data=make_download_payload(fdf),
        file_name="ev_filtered_data.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.download_button(
        "⬇ Download Priority Cities (CSV)",
        data=make_download_payload(city_summary.sort_values(["avg_priority", "avg_gap"], ascending=False)),
        file_name="ev_priority_cities.csv",
        mime="text/csv",
        use_container_width=True,
    )


# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-title">🔋⚡ EV Charging Infrastructure Demand Analysis</div>
        <p class="hero-subtitle">Europe-wide EV demand, charging infrastructure, and investment risk dashboard with a premium black + light green theme.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    [
        "📊 Overview",
        "🏙️ Priority Cities",
        "📈 Trends",
        "🗺️ Geography",
        "🧠 Feature Intelligence",
        "🔍 SQL Insights",
        "📉 Forecast",
        "👤 About",
    ]
)


# =============================================================================
# TAB 1 — OVERVIEW
# =============================================================================
with tab1:
    total_ev = fdf["ev_registrations"].sum()
    total_stations = fdf["charging_stations"].sum()
    avg_gap = fdf["coverage_gap"].mean()
    total_ev_delta, total_ev_delta_color = compute_delta_badge(fdf, "ev_registrations", agg="sum")
    total_station_delta, total_station_delta_color = compute_delta_badge(fdf, "charging_stations", agg="sum")
    avg_gap_delta, avg_gap_delta_color = compute_delta_badge(fdf, "coverage_gap", agg="mean")

    risk_country_row = country_summary.sort_values(["avg_priority", "avg_gap"], ascending=False).iloc[0]
    top_risk_country = risk_country_row["country"]
    risk_country_text = f"Priority {risk_country_row['avg_priority']:.1f} · Gap {risk_country_row['avg_gap']:.1f}"

    kpi_html = f"""
    <style>
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin-bottom: 0.5rem;
        }}
        .kpi-wrap {{
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 0.35rem;
            background: linear-gradient(180deg, rgba(20,28,19,0.98), rgba(10,14,9,0.98));
            border: 1px solid rgba(118,185,0,0.18);
            border-radius: 16px;
            padding: 0.7rem 0.85rem 0.65rem 0.85rem;
            min-height: 110px;
            box-sizing: border-box;
        }}
        .kpi-wrap-label {{
            color: #A7B8A0;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 800;
            font-family: Inter, Segoe UI, sans-serif;
        }}
        .kpi-wrap-value {{
            font-size: clamp(1.55rem, 1.75vw, 1.85rem);
            font-weight: 900;
            letter-spacing: -0.03em;
            line-height: 1.08;
            word-break: break-word;
            font-family: Inter, Segoe UI, sans-serif;
        }}
        .kpi-wrap-delta {{
            display: inline-flex;
            align-items: center;
            width: fit-content;
            font-size: 0.78rem;
            font-weight: 800;
            border-radius: 999px;
            padding: 0.22rem 0.52rem;
            background: rgba(255,255,255,0.04);
            border: 1px solid;
            font-family: Inter, Segoe UI, sans-serif;
        }}
        .kpi-wrap-sub {{
            color: #A7B8A0;
            font-size: 0.79rem;
            line-height: 1.3;
            font-family: Inter, Segoe UI, sans-serif;
        }}
    </style>
    <div class="kpi-grid">
        {kpi_card("Total EV Registrations", fmt_number(total_ev), "Demand footprint across filtered market", THEME["demand"], delta_text=total_ev_delta, delta_color=total_ev_delta_color)}
        {kpi_card("Charging Stations", fmt_number(total_stations), "Installed public charging infrastructure", THEME["infra"], delta_text=total_station_delta, delta_color=total_station_delta_color)}
        {kpi_card("Average Coverage Gap", f"{avg_gap:.1f}", "Higher gap = stronger infra deficit", THEME["risk"], delta_text=avg_gap_delta, delta_color=avg_gap_delta_color)}
        {kpi_card("Top Risk Country", top_risk_country, risk_country_text, THEME["attention"])}
    </div>
    """
    import streamlit.components.v1 as components
    components.html(kpi_html, height=145, scrolling=False)


    st.markdown("<div style='height: 1.1rem'></div>", unsafe_allow_html=True)
    section_header(
        "Country Overview",
        "Consistent color system: green = EV demand, mint = infrastructure, red/amber = risk, bright green = adequacy.",
    )

    ov1, ov2 = st.columns(2)
    with ov1:
        top_ev = country_summary.sort_values("total_ev", ascending=False).head(12).sort_values("total_ev")
        fig = px.bar(
            top_ev,
            x="total_ev",
            y="country",
            orientation="h",
            color_discrete_sequence=[THEME["demand"]],
            labels={"total_ev": pretty_label("total_ev"), "country": ""},
            title="Top Countries by EV Demand",
            text="total_ev",
        )
        fig.update_traces(texttemplate="%{x:,.0f}", hovertemplate="<b>%{y}</b><br>EV Registrations: %{x:,.0f}<extra></extra>")
        apply_chart_theme(fig, height=430)
        st.plotly_chart(fig, use_container_width=True)

    with ov2:
        high_gap = country_summary.sort_values("avg_gap", ascending=False).head(12).sort_values("avg_gap")
        fig = px.bar(
            high_gap,
            x="avg_gap",
            y="country",
            orientation="h",
            color_discrete_sequence=[THEME["risk"]],
            labels={"avg_gap": pretty_label("avg_gap"), "country": ""},
            title="Highest Infrastructure Risk by Country",
            text="avg_gap",
        )
        fig.update_traces(texttemplate="%{x:.1f}", hovertemplate="<b>%{y}</b><br>Average Coverage Gap: %{x:.2f}<extra></extra>")
        apply_chart_theme(fig, height=430)
        st.plotly_chart(fig, use_container_width=True)

    ov3, ov4 = st.columns([1, 1])
    with ov3:
        infra_counts = fdf["infra_status"].value_counts().reset_index()
        infra_counts.columns = ["status", "count"]
        fig = px.pie(
            infra_counts,
            values="count",
            names="status",
            hole=0.56,
            color="status",
            color_discrete_map=STATUS_COLORS,
            title="Infrastructure Status Mix",
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        apply_chart_theme(fig, height=360)
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    with ov4:
        tier_agg = (
            fdf.groupby("city_tier")
            .agg(avg_gap=("coverage_gap", "mean"), avg_priority=("priority_score", "mean"), city_count=("city", "nunique"))
            .reset_index()
            .sort_values("avg_gap", ascending=False)
        )
        fig = px.bar(
            tier_agg,
            x="city_tier",
            y="avg_gap",
            color="avg_priority",
            color_continuous_scale=[[0, THEME["attention"]], [1, THEME["risk"]]],
            title="Coverage Gap by City Tier",
            labels={"city_tier": pretty_label("city_tier"), "avg_gap": pretty_label("avg_gap"), "avg_priority": pretty_label("avg_priority")},
            text=tier_agg["avg_gap"].round(1),
        )
        fig.update_traces(textposition="outside")
        apply_chart_theme(fig, height=360)
        fig.update_layout(coloraxis_colorbar_title="Priority")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "<div class='insight-box'><b>Quick read:</b> Jahan EV demand fast grow kar rahi hai aur coverage gap bhi high hai, waha charging expansion ka ROI strongest hoga. Metro markets demand lead karte hain, lekin mid-tier cities mein underserved pockets clearly dikhte hain.</div>",
        unsafe_allow_html=True,
    )


# =============================================================================
# TAB 2 — PRIORITY CITIES
# =============================================================================
with tab2:
    section_header(
        "Priority Cities Bubble",
        "Overlap-free view with hover-based city details. Bubble size = priority score.",
    )

    priority_country_options = sorted(city_summary["country"].dropna().unique())
    selected_priority_countries = st.multiselect(
        "Focus Countries for Priority Cities",
        options=priority_country_options,
        default=priority_country_options,
        help="Narrow the Top Cities view to one or more specific EV markets.",
    )
    city_summary_tab2 = city_summary[city_summary["country"].isin(selected_priority_countries)].copy() if selected_priority_countries else city_summary.copy()

    filter_col, sort_col = st.columns([1, 1])
    with filter_col:
        n_cities = st.slider("Top Cities to Show", min_value=10, max_value=50, value=25, step=5)
    with sort_col:
        sort_options = {
            pretty_label("avg_priority"): "avg_priority",
            pretty_label("avg_gap"): "avg_gap",
            pretty_label("avg_ev_per_st"): "avg_ev_per_st",
            pretty_label("avg_ev_reg"): "avg_ev_reg",
        }
        chosen_sort = st.selectbox("Sort Priority Cities By", list(sort_options.keys()))
        sort_by = sort_options[chosen_sort]

    top_cities = city_summary_tab2.sort_values(sort_by, ascending=False).head(n_cities).copy()

    COUNTRY_PALETTE = [
        "#76B900","#3DDB84","#FFC857","#FF6B6B","#7CFF8A","#B8FF5C",
        "#00C9FF","#FF9F43","#A29BFE","#FD79A8","#55EFC4","#FDCB6E",
        "#E17055","#74B9FF","#D63031","#00B894","#6C5CE7","#FAB1A0",
        "#81ECEC","#DFE6E9","#2D3436","#636E72","#B2BEC3","#00CEC9",
    ]
    all_countries_tab2 = sorted(top_cities["country"].dropna().unique())
    country_color_map = {c: COUNTRY_PALETTE[i % len(COUNTRY_PALETTE)] for i, c in enumerate(all_countries_tab2)}

    pc1, pc2 = st.columns([1.05, 1.55])
    with pc1:
        fig = px.bar(
            top_cities.sort_values(sort_by),
            x=sort_by,
            y="city",
            orientation="h",
            color="country",
            color_discrete_map=country_color_map,
            title=f"Top {n_cities} Cities by {pretty_label(sort_by)}",
            labels={sort_by: pretty_label(sort_by), "city": "", "country": "Country"},
            hover_data={
                "country": True,
                "avg_gap": ":.2f",
                "avg_priority": ":.2f",
                "avg_ev_reg": ":.2f",
                "avg_stations": ":.2f",
                "infra_status": True,
            },
        )
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>Country: %{customdata[0]}<br>Priority Score: %{x:.2f}<br>Coverage Gap: %{customdata[1]:.2f}<br>EV Registrations: %{customdata[3]:.1f}<br>Infra Status: %{customdata[4]}<extra></extra>",
        )
        apply_chart_theme(fig, height=560)
        fig.update_layout(
            legend_title_text="Country",
            margin=dict(l=160),
            yaxis=dict(tickfont=dict(size=12)),
        )
        st.plotly_chart(fig, use_container_width=True)

    with pc2:
        bubble_df = city_summary_tab2.sort_values("avg_priority", ascending=False).head(max(20, min(40, n_cities))).copy()
        all_countries_bubble = sorted(bubble_df["country"].dropna().unique())
        country_color_map_bubble = {c: COUNTRY_PALETTE[i % len(COUNTRY_PALETTE)] for i, c in enumerate(all_countries_bubble)}
        fig_bubble = px.scatter(
            bubble_df,
            x="avg_stations",
            y="avg_ev_reg",
            size="avg_priority",
            color="country",
            color_discrete_map=country_color_map_bubble,
            hover_name="city",
            hover_data={
                "country": True,
                "city_tier": True,
                "avg_gap": ":.2f",
                "avg_priority": ":.2f",
                "avg_ev_per_st": ":.2f",
                "avg_stations": ":.2f",
                "avg_ev_reg": ":.2f",
                "infra_status": True,
            },
            title="EV Demand vs Charging Infrastructure",
            labels={
                "avg_stations": pretty_label("avg_stations"),
                "avg_ev_reg": pretty_label("avg_ev_reg"),
                "avg_priority": pretty_label("avg_priority"),
                "country": "Country",
            },
            size_max=42,
        )
        fig_bubble.update_traces(marker=dict(line=dict(width=1, color="#D7FFD4"), opacity=0.82))
        apply_chart_theme(fig_bubble, height=560)
        fig_bubble.update_layout(legend_title_text="Country")
        st.plotly_chart(fig_bubble, use_container_width=True)

    section_header(
        "Priority Cities Table",
        "Business-friendly column labels for stakeholder-ready review.",
    )
    display_df = rename_for_display(
        city_summary_tab2.sort_values(["avg_priority", "avg_gap"], ascending=False).reset_index(drop=True)
    )
    display_df.index = np.arange(1, len(display_df) + 1)
    st.dataframe(display_df, use_container_width=True, height=460)

    st.markdown(
        "<div class='insight-box'><b>How to read the bubble chart:</b> Upper-left zone ka matlab hai higher EV demand with relatively fewer stations — yehi true charging-desert opportunities hain. Labels intentionally hover pe rakhe gaye hain taaki overlap na ho.</div>",
        unsafe_allow_html=True,
    )


# =============================================================================
# TAB 3 — TRENDS
# =============================================================================
with tab3:
    section_header(
        "Interactive EV Trends",
        "Spaghetti chart ko interactive bana diya gaya hai — metric aur country selection dono available hain.",
    )

    metric_map = {
        "EV Registrations": "ev_reg",
        "Charging Stations": "stations",
        "Demand Score": "demand",
        "Priority Score": "priority",
        "Coverage Gap": "gap",
    }

    trend_controls_1, trend_controls_2 = st.columns([1, 1.4])
    with trend_controls_1:
        selected_metric = st.selectbox("Trend Metric", list(metric_map.keys()))
        default_trend = monthly_summary.groupby("country")["ev_reg"].sum().sort_values(ascending=False).head(5).index.tolist()
    with trend_controls_2:
        trend_countries = st.multiselect(
            "Countries for Trend Comparison",
            options=sorted(monthly_summary["country"].unique()),
            default=default_trend,
            help="Best readability ke liye 3–6 countries select karo.",
        )

    col_name = metric_map[selected_metric]
    trend_df = monthly_summary[monthly_summary["country"].isin(trend_countries)].copy()
    if trend_df.empty:
        st.info("Trend chart ke liye kam se kam ek country select karo.")
    else:
        fig = px.line(
            trend_df,
            x="date",
            y=col_name,
            color="country",
            labels={"date": "Date", col_name: selected_metric, "country": "Country"},
            title=f"{selected_metric} Trend by Country",
            markers=False,
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(hovermode="x unified")
        apply_chart_theme(fig, height=470)
        st.plotly_chart(fig, use_container_width=True)

    section_header(
        "Year-over-Year Growth Check",
        "Compare EV growth vs station growth to see whether infrastructure is keeping up.",
    )

    yearly = (
        fdf.groupby(["year", "country"])
        .agg(total_ev=("ev_registrations", "sum"), total_stations=("charging_stations", "sum"))
        .reset_index()
        .sort_values(["country", "year"])
    )
    yearly["yoy_ev_pct"] = yearly.groupby("country")["total_ev"].pct_change() * 100
    yearly["yoy_st_pct"] = yearly.groupby("country")["total_stations"].pct_change() * 100

    compare_yoy = st.toggle("Compare multiple countries in YoY view", value=False)
    yoy_options = sorted(yearly["country"].dropna().unique())
    default_yoy = yoy_options[:3] if len(yoy_options) >= 3 else yoy_options
    if compare_yoy:
        yoy_countries = st.multiselect(
            "Countries for YoY Comparison",
            options=yoy_options,
            default=default_yoy,
            help="Best readability ke liye 2–3 countries select karo.",
        )
        yoy_view = yearly[yearly["country"].isin(yoy_countries)].dropna(subset=["yoy_ev_pct", "yoy_st_pct"]).copy()
        yoy_long = yoy_view.melt(
            id_vars=["year", "country"],
            value_vars=["yoy_ev_pct", "yoy_st_pct"],
            var_name="metric",
            value_name="growth_pct",
        )
        yoy_long["metric"] = yoy_long["metric"].map({"yoy_ev_pct": "EV Growth (%)", "yoy_st_pct": "Station Growth (%)"})
        fig = px.line(
            yoy_long,
            x="year",
            y="growth_pct",
            color="country",
            line_dash="metric",
            markers=True,
            title="YoY EV vs Station Growth — Comparison Mode",
            labels={"year": "Year", "growth_pct": "Growth (%)", "country": "Country", "metric": "Series"},
        )
        fig.add_hline(y=0, line_dash="dash", line_color=THEME["muted"], opacity=0.6)
        apply_chart_theme(fig, height=460, legend_title="Country / Series")
        st.plotly_chart(fig, use_container_width=True)
    else:
        yoy_country = st.selectbox("Country for YoY Growth", yoy_options)
        yoy_view = yearly[yearly["country"] == yoy_country].dropna(subset=["yoy_ev_pct", "yoy_st_pct"]).copy()

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=yoy_view["year"],
                y=yoy_view["yoy_ev_pct"],
                name="EV Growth (%)",
                marker_color=THEME["demand"],
                hovertemplate="Year %{x}<br>EV Growth: %{y:.2f}%<extra></extra>",
            )
        )
        fig.add_trace(
            go.Bar(
                x=yoy_view["year"],
                y=yoy_view["yoy_st_pct"],
                name="Station Growth (%)",
                marker_color=THEME["infra"],
                hovertemplate="Year %{x}<br>Station Growth: %{y:.2f}%<extra></extra>",
            )
        )
        fig.add_hline(y=0, line_dash="dash", line_color=THEME["muted"], opacity=0.6)
        fig.update_layout(barmode="group", title=f"YoY EV vs Station Growth — {yoy_country}")
        apply_chart_theme(fig, height=420)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "<div class='insight-box'><b>Decision lens:</b> Agar EV growth bars consistently station growth se upar hain, toh demand-supply imbalance widen ho raha hai — us market ko proactive infrastructure investment chahiye.</div>",
        unsafe_allow_html=True,
    )


# =============================================================================
# TAB 4 — GEOGRAPHY
# =============================================================================
with tab4:
    section_header(
        "Geography & Market Footprint",
        "Dark map theme for quick spatial scanning of demand, gap, and investment urgency.",
    )

    if {"latitude", "longitude"}.issubset(fdf.columns):
        city_map = (
            fdf.groupby(["city", "country", "infra_status"])
            .agg(
                lat=("latitude", "mean"),
                lon=("longitude", "mean"),
                avg_priority=("priority_score", "mean"),
                avg_gap=("coverage_gap", "mean"),
                avg_ev=("ev_registrations", "mean"),
                avg_stations=("charging_stations", "mean"),
            )
            .reset_index()
            .round(3)
        )

        map_metric = st.selectbox(
            "Bubble Size Metric",
            ["avg_priority", "avg_gap", "avg_ev"],
            format_func=pretty_label,
        )

        fig_map = px.scatter_mapbox(
            city_map,
            lat="lat",
            lon="lon",
            color="infra_status",
            color_discrete_map=STATUS_COLORS,
            size=map_metric,
            size_max=20,
            zoom=3.2,
            center={"lat": 54, "lon": 14},
            hover_name="city",
            hover_data={
                "country": True,
                "avg_priority": ":.2f",
                "avg_gap": ":.2f",
                "avg_ev": ":.2f",
                "avg_stations": ":.2f",
                "lat": False,
                "lon": False,
            },
            title="Europe EV Infrastructure Map",
            mapbox_style="carto-darkmatter",
            height=620,
        )
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=60, b=10),
            font=dict(color=THEME["text"]),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=THEME["muted"])),
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("Latitude/Longitude columns available nahi hain, isliye map render nahi ho pa raha.")


# =============================================================================
# TAB 5 — FEATURE INTELLIGENCE
# =============================================================================
with tab5:
    section_header(
        "Feature Importance",
        "Raw technical labels ko business-friendly naming ke saath present kiya gaya hai.",
    )

    left, right = st.columns([1.45, 1])
    with left:
        if feature_importance is not None:
            chart_df = feature_importance.copy()
            chart_df["feature_label"] = chart_df["feature"].map(pretty_label)
            fig = px.bar(
                chart_df.sort_values("importance"),
                x="importance",
                y="feature_label",
                orientation="h",
                color_discrete_sequence=[THEME["demand"]],
                title="Top Drivers of EV Registrations",
                labels={"importance": "Importance", "feature_label": ""},
            )
            fig.update_traces(hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>")
            apply_chart_theme(fig, height=540)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Feature importance available nahi hai for current dataset structure.")

    with right:
        metric_1, metric_2, metric_3 = st.columns(3)
        if feature_metrics is not None:
            metric_1.metric("R²", feature_metrics["R²"])
            metric_2.metric("MAE", feature_metrics["MAE"])
            metric_3.metric("RMSE", feature_metrics["RMSE"])
            st.markdown(
                f"<div class='insight-box'><b>Model note:</b> {feature_metrics['note']}</div>",
                unsafe_allow_html=True,
            )

        if models_summary is not None:
            st.markdown("### Model Summary")
            st.dataframe(rename_for_display(models_summary), use_container_width=True, height=210)

        if feature_importance is not None:
            top_labels = chart_df.head(5)["feature_label"].tolist()
            bullet_html = "".join([f"<li>{item}</li>" for item in top_labels])
            st.markdown(
                f"""
                <div class='insight-box'>
                    <b>Top business signals:</b>
                    <ul style='margin-top:0.5rem; padding-left:1.1rem;'>
                        {bullet_html}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )


# =============================================================================
# TAB 6 — SQL INSIGHTS
# =============================================================================
with tab6:
    section_header(
        "SQL Insights",
        "Business questions ko dashboard-ready views mein convert kiya gaya hai.",
    )

    query_choice = st.radio(
        "Insight View",
        [
            "Q1 — Top Priority Cities",
            "Q2 — Month-on-Month Growth",
            "Q3 — Infrastructure Status Profile",
            "Q4 — Charging Deserts",
            "Q5 — City Tier Gap",
            "Q6 — YoY Growth",
        ],
        horizontal=True,
    )

    if query_choice == "Q1 — Top Priority Cities":
        q1 = (
            fdf.groupby(["country", "city"])
            .agg(
                avg_priority_score=("priority_score", "mean"),
                avg_coverage_gap=("coverage_gap", "mean"),
                avg_ev_registrations=("ev_registrations", "mean"),
                avg_charging_stations=("charging_stations", "mean"),
                infra_status=("infra_status", "last"),
            )
            .reset_index()
            .sort_values("avg_priority_score", ascending=False)
            .head(15)
            .round(2)
        )
        st.dataframe(rename_for_display(q1), use_container_width=True)
        fig = px.bar(
            q1.sort_values("avg_priority_score"),
            x="avg_priority_score",
            y="city",
            orientation="h",
            color="infra_status",
            color_discrete_map=STATUS_COLORS,
            title="Top Priority Cities",
            labels={"avg_priority_score": "Average Priority Score", "city": ""},
        )
        apply_chart_theme(fig, height=480)
        fig.update_layout(margin=dict(l=160), yaxis=dict(tickfont=dict(size=12)))
        st.plotly_chart(fig, use_container_width=True)

    elif query_choice == "Q2 — Month-on-Month Growth":
        monthly_q2 = (
            fdf.groupby(["country", "year", "month"])
            .agg(total_ev=("ev_registrations", "sum"), total_stations=("charging_stations", "sum"))
            .reset_index()
            .sort_values(["country", "year", "month"])
        )
        monthly_q2["prev_ev"] = monthly_q2.groupby("country")["total_ev"].shift(1)
        monthly_q2["mom_growth_pct"] = ((monthly_q2["total_ev"] - monthly_q2["prev_ev"]) / monthly_q2["prev_ev"].replace(0, np.nan) * 100).round(2)
        monthly_q2 = monthly_q2.dropna(subset=["mom_growth_pct"])
        monthly_q2["month_str"] = monthly_q2["year"].astype(str) + "-" + monthly_q2["month"].astype(str).str.zfill(2)
        compare_q2 = st.toggle("Compare Mode for MoM Growth", value=False)
        if compare_q2:
            q2_countries = st.multiselect(
                "Countries for MoM Comparison",
                options=sorted(monthly_q2["country"].unique()),
                default=sorted(monthly_q2["country"].unique())[:3],
            )
            sub = monthly_q2[monthly_q2["country"].isin(q2_countries)].copy()
            fig = px.line(
                sub,
                x="month_str",
                y="mom_growth_pct",
                color="country",
                markers=True,
                title="Month-on-Month EV Growth — Comparison Mode",
                labels={"month_str": "Month", "mom_growth_pct": "MoM Growth (%)", "country": "Country"},
            )
            fig.add_hline(y=0, line_dash="dash", line_color=THEME["muted"])
            apply_chart_theme(fig, height=430)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(rename_for_display(sub.tail(36)), use_container_width=True)
        else:
            sel_country = st.selectbox("Country", sorted(monthly_q2["country"].unique()))
            sub = monthly_q2[monthly_q2["country"] == sel_country]
            fig = px.bar(
                sub,
                x="month_str",
                y="mom_growth_pct",
                title=f"Month-on-Month EV Growth — {sel_country}",
                color="mom_growth_pct",
                color_continuous_scale=[[0, THEME["risk"]], [0.5, THEME["attention"]], [1, THEME["demand"]]],
                labels={"month_str": "Month", "mom_growth_pct": "MoM Growth (%)"},
            )
            fig.add_hline(y=0, line_dash="dash", line_color=THEME["muted"])
            apply_chart_theme(fig, height=430)
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(rename_for_display(sub.tail(24)), use_container_width=True)

    elif query_choice == "Q3 — Infrastructure Status Profile":
        q3 = (
            fdf.groupby("infra_status")
            .agg(
                row_count=("city", "count"),
                city_count=("city", "nunique"),
                avg_priority_score=("priority_score", "mean"),
                avg_coverage_gap=("coverage_gap", "mean"),
                avg_ev_per_station=("ev_per_station", "mean"),
            )
            .reset_index()
            .round(2)
            .sort_values("avg_priority_score", ascending=False)
        )
        a, b = st.columns([1, 1])
        with a:
            st.dataframe(rename_for_display(q3), use_container_width=True)
        with b:
            fig = px.bar(
                q3,
                x="infra_status",
                y="avg_coverage_gap",
                color="infra_status",
                color_discrete_map=STATUS_COLORS,
                title="Average Coverage Gap by Infrastructure Status",
                labels={"infra_status": "Infrastructure Status", "avg_coverage_gap": "Average Coverage Gap"},
            )
            apply_chart_theme(fig, height=360)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    elif query_choice == "Q4 — Charging Deserts":
        q4 = (
            fdf[fdf["infra_status"].isin(["Critical Gap", "Needs Attention"])]
            .groupby(["country", "city"])
            .agg(
                avg_ev_reg=("ev_registrations", "mean"),
                avg_stations=("charging_stations", "mean"),
                avg_coverage_gap=("coverage_gap", "mean"),
                avg_ev_per_station=("ev_per_station", "mean"),
                infra_status=("infra_status", "last"),
            )
            .reset_index()
            .sort_values("avg_coverage_gap", ascending=False)
            .head(20)
            .round(2)
        )
        st.dataframe(rename_for_display(q4), use_container_width=True)
        fig = px.bar(
            q4.sort_values("avg_coverage_gap"),
            x="avg_coverage_gap",
            y="city",
            orientation="h",
            color="infra_status",
            color_discrete_map={"Critical Gap": THEME["risk"], "Needs Attention": THEME["attention"]},
            title="Charging Desert Cities",
            labels={"avg_coverage_gap": "Average Coverage Gap", "city": ""},
        )
        apply_chart_theme(fig, height=540)
        fig.update_layout(margin=dict(l=160), yaxis=dict(tickfont=dict(size=12)))
        st.plotly_chart(fig, use_container_width=True)

    elif query_choice == "Q5 — City Tier Gap":
        q5 = (
            fdf.groupby("city_tier")
            .agg(
                city_count=("city", "nunique"),
                avg_ev_reg=("ev_registrations", "mean"),
                avg_stations=("charging_stations", "mean"),
                avg_coverage_gap=("coverage_gap", "mean"),
                avg_ev_per_station=("ev_per_station", "mean"),
                avg_priority_score=("priority_score", "mean"),
            )
            .reset_index()
            .round(2)
            .sort_values("avg_priority_score", ascending=False)
        )
        x1, x2 = st.columns([1, 1])
        with x1:
            st.dataframe(rename_for_display(q5), use_container_width=True)
        with x2:
            fig = px.bar(
                q5,
                x="city_tier",
                y="avg_coverage_gap",
                color="avg_priority_score",
                color_continuous_scale=[[0, THEME["attention"]], [1, THEME["risk"]]],
                title="Coverage Gap by City Tier",
                labels={"city_tier": "City Tier", "avg_coverage_gap": "Average Coverage Gap", "avg_priority_score": "Average Priority Score"},
                text=q5["avg_coverage_gap"].round(1),
            )
            fig.update_traces(textposition="outside")
            apply_chart_theme(fig, height=380)
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    elif query_choice == "Q6 — YoY Growth":
        yearly_q6 = (
            fdf.groupby(["country", "year"])
            .agg(total_ev=("ev_registrations", "sum"), total_stations=("charging_stations", "sum"))
            .reset_index()
            .sort_values(["country", "year"])
        )
        yearly_q6["yoy_ev_pct"] = yearly_q6.groupby("country")["total_ev"].pct_change().mul(100).round(2)
        yearly_q6["yoy_st_pct"] = yearly_q6.groupby("country")["total_stations"].pct_change().mul(100).round(2)
        compare_q6 = st.toggle("Compare Mode for SQL YoY View", value=False)
        q6_options = sorted(yearly_q6["country"].dropna().unique())
        if compare_q6:
            q6_countries = st.multiselect(
                "Countries for SQL YoY Comparison",
                options=q6_options,
                default=q6_options[:3],
            )
            sub_y = yearly_q6[yearly_q6["country"].isin(q6_countries)].dropna(subset=["yoy_ev_pct", "yoy_st_pct"]).copy()
            q6_long = sub_y.melt(
                id_vars=["country", "year"],
                value_vars=["yoy_ev_pct", "yoy_st_pct"],
                var_name="metric",
                value_name="growth_pct",
            )
            q6_long["metric"] = q6_long["metric"].map({"yoy_ev_pct": "EV Growth (%)", "yoy_st_pct": "Station Growth (%)"})
            fig = px.line(
                q6_long,
                x="year",
                y="growth_pct",
                color="country",
                line_dash="metric",
                markers=True,
                title="YoY EV vs Station Growth — SQL Comparison Mode",
                labels={"year": "Year", "growth_pct": "Growth (%)", "country": "Country", "metric": "Series"},
            )
            fig.add_hline(y=0, line_dash="dash", line_color=THEME["muted"], opacity=0.6)
            apply_chart_theme(fig, height=430)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(rename_for_display(sub_y), use_container_width=True)
        else:
            sel_country = st.selectbox("Country for SQL YoY View", q6_options)
            sub_y = yearly_q6[yearly_q6["country"] == sel_country].dropna(subset=["yoy_ev_pct", "yoy_st_pct"])
            fig = go.Figure()
            fig.add_trace(go.Bar(x=sub_y["year"], y=sub_y["yoy_ev_pct"], name="EV Growth (%)", marker_color=THEME["demand"]))
            fig.add_trace(go.Bar(x=sub_y["year"], y=sub_y["yoy_st_pct"], name="Station Growth (%)", marker_color=THEME["infra"]))
            fig.add_hline(y=0, line_dash="dash", line_color=THEME["muted"], opacity=0.6)
            fig.update_layout(title=f"YoY EV vs Station Growth — {sel_country}", barmode="group")
            apply_chart_theme(fig, height=430)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(rename_for_display(sub_y), use_container_width=True)


# =============================================================================
# TAB 7 — FORECAST
# =============================================================================
with tab7:
    section_header(
        "Forecast Outlook",
        "Optional Prophet-style forecast view. If a forecast CSV is available, the dashboard will surface it here.",
    )

    if forecast_df is None or forecast_df.empty or "date" not in forecast_df.columns:
        st.info("Forecast tab ready hai. Bas `forecast.csv` add karo with columns like `ds/yhat` ya `date/forecast`, aur chart yahan render ho jayega.")
    else:
        forecast_view = forecast_df.copy()
        if "country" in forecast_view.columns:
            forecast_options = sorted(forecast_view["country"].dropna().astype(str).unique())
            selected_forecast_countries = st.multiselect(
                "Forecast Countries",
                options=forecast_options,
                default=forecast_options[:3] if len(forecast_options) > 3 else forecast_options,
            )
            if selected_forecast_countries:
                forecast_view = forecast_view[forecast_view["country"].astype(str).isin(selected_forecast_countries)]

        y_col = "forecast" if "forecast" in forecast_view.columns else None
        if y_col is None:
            numeric_cols = [col for col in forecast_view.columns if col != "date" and pd.api.types.is_numeric_dtype(forecast_view[col])]
            y_col = numeric_cols[0] if numeric_cols else None

        if y_col is None:
            st.warning("Forecast CSV mil gaya, lekin numeric forecast column detect nahi hua.")
        else:
            if "country" in forecast_view.columns:
                fig = px.line(
                    forecast_view,
                    x="date",
                    y=y_col,
                    color="country",
                    title="Forecasted EV Demand",
                    labels={"date": "Date", y_col: pretty_label(y_col), "country": "Country"},
                )
            else:
                fig = px.line(
                    forecast_view,
                    x="date",
                    y=y_col,
                    title="Forecasted EV Demand",
                    labels={"date": "Date", y_col: pretty_label(y_col)},
                )
            if {"forecast_lower", "forecast_upper"}.issubset(forecast_view.columns):
                grouped_forecast = forecast_view.groupby("country") if "country" in forecast_view.columns else [("All Markets", forecast_view)]
                for group_name, group_df in grouped_forecast:
                    fig.add_trace(
                        go.Scatter(
                            x=group_df["date"],
                            y=group_df["forecast_upper"],
                            mode="lines",
                            line=dict(width=0),
                            hoverinfo="skip",
                            showlegend=False,
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=group_df["date"],
                            y=group_df["forecast_lower"],
                            mode="lines",
                            line=dict(width=0),
                            fill="tonexty",
                            fillcolor="rgba(118,185,0,0.10)",
                            name=f"{group_name} interval",
                            hoverinfo="skip",
                        )
                    )
            apply_chart_theme(fig, height=480)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(rename_for_display(forecast_view.tail(50)), use_container_width=True)
            st.download_button(
                "⬇ Download Forecast CSV",
                data=make_download_payload(forecast_view),
                file_name="ev_forecast_view.csv",
                mime="text/csv",
            )


# =============================================================================
# TAB 8 — ABOUT
# =============================================================================
with tab8:
    section_header("About This Project", "EV Charging Station Demand Analysis — Europe")

    import streamlit.components.v1 as _components

    gh_url  = PORTFOLIO_LINKS.get("GitHub",   "#")
    li_url  = PORTFOLIO_LINKS.get("LinkedIn", "#")

    badge = "background:rgba(118,185,0,0.15);border:1px solid rgba(118,185,0,0.3);border-radius:6px;padding:0.15rem 0.55rem;margin:0.15rem;display:inline-block;color:#F5FFF0;font-size:0.88rem;"
    card  = "background:linear-gradient(180deg,rgba(20,28,19,0.98),rgba(10,14,9,0.98));border:1px solid rgba(118,185,0,0.20);border-radius:16px;padding:1.1rem 1.2rem;"
    label = "color:#A7B8A0;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;font-weight:800;margin-bottom:0.5rem;font-family:Inter,sans-serif;"
    body  = "color:#F5FFF0;font-size:0.92rem;line-height:1.65;font-family:Inter,sans-serif;"

    about_html = f"""
    <style>
        body {{ margin:0; padding:0; background:transparent; }}
        .about-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:1.2rem; margin-bottom:1.2rem; }}
        .about-card {{ {card} }}
        .about-label {{ {label} }}
        .about-body {{ {body} }}
        .badge {{ {badge} }}
        .insight {{ background:rgba(118,185,0,0.07);border-left:3px solid #76B900;border-radius:0 10px 10px 0;padding:0.75rem 1rem;color:#F5FFF0;font-size:0.88rem;line-height:1.6;font-family:Inter,sans-serif;margin-bottom:1.2rem; }}
        .dev-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-top:0.8rem; }}
        .dev-card {{ {card} text-align:center; }}
        .dev-name {{ color:#F5FFF0;font-weight:800;font-size:1rem;font-family:Inter,sans-serif; }}
        .dev-sub {{ color:#A7B8A0;font-size:0.82rem;margin-top:0.2rem;font-family:Inter,sans-serif; }}
        .btn-green {{ background:#76B900;color:#000;font-weight:800;font-size:0.82rem;padding:0.35rem 0.9rem;border-radius:8px;text-decoration:none;display:inline-block;margin-top:0.5rem; }}
        .btn-teal  {{ background:#3DDB84;color:#000;font-weight:800;font-size:0.82rem;padding:0.35rem 0.9rem;border-radius:8px;text-decoration:none;display:inline-block;margin-top:0.5rem; }}
        .sec-title {{ color:#F5FFF0;font-size:1.05rem;font-weight:800;font-family:Inter,sans-serif;margin:1.2rem 0 0.2rem 0; }}
        .sec-sub   {{ color:#A7B8A0;font-size:0.84rem;font-family:Inter,sans-serif;margin-bottom:0.8rem; }}
    </style>

    <div class="about-grid">
        <div class="about-card" style="border-top:3px solid #76B900;">
            <div class="about-label">Project Objective</div>
            <div class="about-body">
                Analyze EV charging demand across <b style="color:#76B900;">23 European countries</b> to identify
                infrastructure gaps, priority investment cities, and forecast future demand — enabling
                data-driven decisions for EV charging expansion.
            </div>
        </div>
        <div class="about-card" style="border-top:3px solid #3DDB84;">
            <div class="about-label">Dataset</div>
            <div class="about-body">
                <b style="color:#3DDB84;">13,620 rows</b> · 23 columns · 2021–2024<br>
                Europe-wide EV registrations, charging stations, coverage gap, priority scores across cities and countries.
            </div>
        </div>
        <div class="about-card" style="border-top:3px solid #FFC857;">
            <div class="about-label">Tech Stack</div>
            <div class="about-body">
                <span class="badge">Python</span>
                <span class="badge">Pandas</span>
                <span class="badge">MySQL</span>
                <span class="badge">Scikit-learn</span>
                <span class="badge">Prophet</span>
                <span class="badge">Streamlit</span>
                <span class="badge">Plotly</span>
                <span class="badge">SQLAlchemy</span>
                <span class="badge">Power BI</span>
            </div>
        </div>
        <div class="about-card" style="border-top:3px solid #FF6B6B;">
            <div class="about-label">Key Findings</div>
            <div class="about-body">
                🔴 <b style="color:#FF6B6B;">Greece &amp; Czech Republic</b> have the highest infrastructure gap<br>
                🟢 <b style="color:#76B900;">Germany &amp; France</b> lead in EV demand<br>
                📈 EV registrations grew <b style="color:#3DDB84;">15%+</b> vs early period<br>
                ⚡ Tier 3–4 cities are the most underserved markets
            </div>
        </div>
    </div>

    <div class="insight">
        <b>Dashboard Sections:</b> Overview (KPIs + country charts) · Priority Cities (investment ranking) ·
        Trends (MoM/YoY growth) · Geography (map) · Feature Intelligence (ML correlation) ·
        SQL Insights (6 business queries) · Forecast (Prophet 12-month) · About
    </div>

    <div class="sec-title">Developer</div>
    <div class="sec-sub">Built by Sumersing Patil</div>

    <div class="dev-grid">
        <div class="dev-card">
            <div style="font-size:2rem;margin-bottom:0.4rem;">👨‍💻</div>
            <div class="dev-name">Sumersing Patil</div>
            <div class="dev-sub">B.Tech AI ·Graduate</div>
            <div class="dev-sub">GH Raisoni Institute, Jalgaon</div>
        </div>
        <div class="dev-card">
            <div style="font-size:2rem;margin-bottom:0.4rem;">💼</div>
            <div class="dev-name">LinkedIn</div>
            <div class="dev-sub">Connect &amp; Collaborate</div>
            <a href="{li_url}" target="_blank" class="btn-green">View Profile →</a>
        </div>
        <div class="dev-card">
            <div style="font-size:2rem;margin-bottom:0.4rem;">🐙</div>
            <div class="dev-name">GitHub</div>
            <div class="dev-sub">Source Code &amp; Projects</div>
            <a href="{gh_url}" target="_blank" class="btn-teal">View GitHub →</a>
        </div>
    </div>
    """

    _components.html(about_html, height=620, scrolling=False)

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
footer_links = [f"<span>{PROJECT_NAME}</span>"]
for label, url in PORTFOLIO_LINKS.items():
    if url:
        footer_links.append(f"<a href='{url}' target='_blank'>{label}</a>")

st.markdown(
    f"<div class='footer-note'>Built with Streamlit + Plotly · Premium EV demand dashboard theme · Black + Light Green UI</div><div class='footer-links'>{''.join(footer_links)}</div>",
    unsafe_allow_html=True,
)
