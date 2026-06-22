#                             🔋 EV Charging Station Demand Analysis

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-purple.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**An end-to-end EV infrastructure analytics project that analyzes charging demand, identifies priority investment cities, and visualizes infrastructure gaps across city-level EV markets**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Power BI Screenshots](#-power-bi-screenshots)

</div>

---

## 📖 Table of Contents

- [Introduction](#-introduction)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Database & SQL Views](#️-database--sql-views)
- [API / Function Reference](#-api--function-reference)
- [Screenshots](#-screenshots)
- [Power BI Screenshots](#-power-bi-screenshots)
- [Project Screenshots](#-project-screenshots)
- [Contributing](#-contributing)
- [Future Enhancements](#-future-enhancements)
- [Contact](#-contact)

---

## 🎯 Introduction

**EV Charging Station Demand Analysis** is a premium dark-theme analytics project built to study **EV adoption**, **charging infrastructure adequacy**, and **investment priority** across cities and countries. The project combines a **Streamlit dashboard**, **MySQL database**, **SQL analytical views**, and optional **forecast-ready inputs** to help identify underserved EV markets and support smarter charging network expansion.

The workflow follows a practical analytics pipeline: a cleaned EV dataset is loaded into MySQL → SQL views answer business questions → Streamlit renders interactive KPIs, maps, trends, filters, and downloadable insights for decision-making.

### 🌟 Why Choose This Project?

- ✅ **14,120+ records** available in the provided EV dataset
- ✅ **27 analytical fields** including EV demand, charging stations, coverage gap, and priority score
- ✅ **8 Streamlit dashboard sections** for overview, trends, geography, SQL insights, forecast, and more
- ✅ **6 SQL business views** for investment planning and infrastructure gap analysis
- ✅ **Premium NVIDIA-inspired UI** with black + neon green design system
- ✅ **CSV export support** for filtered datasets and priority city summaries
- ✅ **Forecast-ready architecture** with optional `forecast.csv` integration
- ✅ **Power BI screenshot-ready documentation section** for portfolio presentation

---

## ✨ Features

### 🔍 Core Features

| Feature | Description |
|---------|-------------|
| **Interactive Dashboard** | Streamlit-based analytical dashboard with a premium black + light green theme |
| **Investment Priority Analysis** | Ranks cities using `priority_score`, `coverage_gap`, and EV demand indicators |
| **Trend Monitoring** | Tracks month-on-month and year-over-year EV adoption growth |
| **Infrastructure Gap Detection** | Highlights underserved cities with charging shortages |
| **Geographic Visualization** | Interactive map view for city-level EV and charging metrics |
| **SQL Insights Tab** | Six business-ready analytical views translated into dashboard visuals |
| **Forecast Support** | Optional forecast tab that reads a `forecast.csv` file when available |
| **CSV Downloads** | Export filtered dashboard data and priority city summaries directly |

### 🎨 UI Features

- 🌙 **Dark Premium Theme** — NVIDIA-inspired black and neon-green styling
- ⚡ **KPI Cards** — Executive-style metric cards for total EV demand, charging stations, and coverage gap
- 🧭 **Advanced Sidebar Filters** — Country, city, year range, city tier, infrastructure status, and EV-per-station stress filter
- 🗺️ **Mapbox Visuals** — Location-based market exploration
- 📊 **Interactive Plotly Charts** — Bar, line, pie, bubble, and map visualizations
- ⬇️ **Download Buttons** — One-click CSV export for decision-ready data

### 📊 Analytical Highlights

- **Overview Analytics**: High-level KPIs, country comparison, and infrastructure health summary
- **Priority Cities Ranking**: Identify the best cities for new EV charging investment
- **Trends Analysis**: Compare EV growth across countries over time
- **Feature Intelligence**: ML-style feature importance / correlation-based insight generation from the data
- **SQL Business Questions**: Dedicated tab for six analytical query views
- **Forecast Outlook**: Built-in section for future EV demand visualization if forecast data is supplied

---

## 🛠️ Tech Stack

### Backend / Analytics
- **Python 3.9+**
- **Pandas / NumPy** — Data processing and transformation
- **Scikit-learn** — Feature intelligence / model-style importance workflows inside the dashboard
- **SQLAlchemy** — Database engine integration
- **PyMySQL** — MySQL connectivity
- **python-dotenv** — Environment variable handling

### Frontend / Visualization
- **Streamlit** — Interactive dashboard framework
- **Plotly** — Interactive charting and map visualizations
- **Matplotlib / Seaborn** — Supporting data visualization stack
- **Custom HTML/CSS** — Premium KPI cards and styled dashboard sections

### Database
- **MySQL 8.0+** — Storage for EV charging analytics data
- **SQL Views** — Reusable business insights layer

### Notebook / Workflow
- **Jupyter Notebook** — Analysis and experimentation workflow via `EV_Charging_Analysis.ipynb`
- **CSV Dataset Pipeline** — Local dataset ingestion for dashboard + SQL views
- **Optional Forecast Files** — `forecast.csv` and `models_summary.csv` support in dashboard

### Analytics Pipeline

```text
Raw EV Dataset (CSV)
        ↓
Data Cleaning / Standardization
        ↓
MySQL Table Load (`ev_data`)
        ↓
SQL Analytical Views
        ↓
Streamlit Dashboard + Filters + Charts
        ↓
Priority City Insights + Downloads + Forecast-ready View
```

---

## 📦 Installation

### Prerequisites

```bash
# Python 3.9 or higher
python --version

# MySQL 8.0+
mysql --version

# pip
pip --version
```

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/ev-charging-demand-analysis.git
cd ev-charging-demand-analysis
```

> Replace the repository URL above with your actual GitHub repo link.

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Add the Dataset

Make sure the dataset file is available in the project directory:

```text
europe_ev_dataset.csv
```

You can also keep a cleaned version such as:

```text
ev_data_cleaned_final.csv
```

### Step 5: Configure MySQL

1. Create a `.env` file in the project root.
2. Add your MySQL credentials.
3. Ensure the database name matches the SQL script / Python helper.

### Step 6: Create Database Schema

Run the SQL script in MySQL:

```bash
mysql -u root -p < ev_charging_analysis.sql
```

Or use the helper script flow in Python through `db_connection.py`.

### Step 7: Run the Streamlit App

```bash
streamlit run app.py
```

---

## ⚙️ Configuration

### `.env` File

Create a `.env` file with your own local values:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=ev_charging_analysis
```

> Never commit your real password or secrets to GitHub.

### Key App Inputs

The dashboard can automatically work with these files when present:

- `europe_ev_dataset.csv` or `ev_data_cleaned_final.csv`
- `forecast.csv` *(optional for Forecast tab)*
- `models_summary.csv` *(optional for model / comparison summary)*

### Database Notes

- The app uses **PyMySQL** instead of `mysql-connector-python`
- This helps avoid common MySQL 8 authentication plugin issues
- The default database name is `ev_charging_analysis`

---

## 🎮 Usage

### 1. **📊 Overview**

Use the Overview tab to monitor:
- Total EV registrations
- Total charging stations
- Average coverage gap
- Highest-risk country based on priority and gap indicators

### 2. **🏙️ Priority Cities**

This section helps identify:
- Cities with the highest charging demand pressure
- High-priority investment markets
- Bubble-chart comparison of EV demand vs charging availability
- Exportable priority-city summary CSV

### 3. **📈 Trends**

Track market movement with:
- Month-on-month EV growth
- Year-over-year EV growth
- Country-wise trend comparisons
- Growth comparison across selected markets

### 4. **🗺️ Geography**

Explore city-level EV infrastructure on an interactive map using metrics such as:
- EV registrations
- Charging stations
- Coverage gap
- Demand / priority indicators

### 5. **🧠 Feature Intelligence**

Understand which variables are most associated with EV registrations and demand patterns through the dashboard’s feature-importance / correlation-based analytics.

### 6. **🔍 SQL Insights**

View business-ready insights generated from SQL logic:
- Top Priority Cities
- Month-on-Month Growth
- Infrastructure Status Profile
- Charging Deserts
- City Tier Gap
- YoY Growth

### 7. **📉 Forecast**

If `forecast.csv` is available, the Forecast tab can display:
- Forecasted EV demand lines
- Country-level forecast comparison
- Forecast intervals (lower / upper bounds)
- Downloadable forecast view

### 8. **👤 About**

The About section summarizes:
- Project objective
- Dataset context
- Tech stack
- Key findings
- Developer profile links

---

## 🔬 How It Works

### End-to-End Workflow

```text
CSV Dataset
   ↓
Python Cleaning / Normalization
   ↓
MySQL Database Table (`ev_data`)
   ↓
SQL Views for Business Questions
   ↓
Streamlit Dashboard
   ↓
Insights, Rankings, Maps, and Downloads
```

### Step-by-Step Process

#### 1. **Dataset Loading**
The app loads EV charging data from local CSV files using a resilient loader that checks the project folder first.

#### 2. **Data Standardization**
Country names, city tiers, and infrastructure labels are cleaned and standardized for better filtering and chart quality.

#### 3. **Dashboard Filtering**
Users can dynamically filter data by:
- Country
- City search
- Year range
- City tier
- Infrastructure status
- EV-per-station threshold

#### 4. **SQL Layer**
The MySQL schema stores the EV data in `ev_data`, while SQL views answer recurring business questions with reusable logic.

#### 5. **Insight Generation**
The dashboard computes:
- Country-level summaries
- City-level summaries
- Monthly aggregates
- Priority rankings
- Gap analysis
- Feature importance style insights

#### 6. **Export Layer**
Filtered data and top priority city views can be exported as CSV files directly from the app.

#### 7. **Forecast Extension**
A future-demand layer can be activated by adding a compatible `forecast.csv` file to the project directory.

---

## 📁 Project Structure

```bash
ev-charging-demand-analysis/
│
├── app.py
├── db_connection.py
├── ev_charging_analysis.sql
├── europe_ev_dataset.csv
├── EV_Charging_Analysis.ipynb
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── Screenshots/
│   ├── Project/
│   │   ├── overview.png
│   │   ├── priority-cities.png
│   │   ├── trends.png
│   │   ├── geography.png
│   │   ├── sql-insights.png
│   │   └── forecast.png
│   │
│   └── PowerBI/
│       ├── dashboard-overview.png
│       ├── country-analysis.png
│       ├── city-gap-analysis.png
│       └── executive-summary.png
│
└── optional/
    ├── forecast.csv
    └── models_summary.csv
```

### File Descriptions

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit dashboard application |
| `db_connection.py` | MySQL helper for schema creation and CSV upload |
| `ev_charging_analysis.sql` | Database schema + analytical SQL views |
| `europe_ev_dataset.csv` | Main EV charging analysis dataset |
| `EV_Charging_Analysis.ipynb` | Notebook for analysis / experimentation |
| `requirements.txt` | Python dependencies |
| `.env` | Local environment variables for MySQL |
| `Screenshots/` | Folder for project and Power BI screenshots |

---

## 🗄️ Database & SQL Views

### Schema

The database is built around one main table:

#### **`ev_data`**
Stores city-level EV and charging metrics such as:
- Country / state / city
- Year / month
- Population and density
- EV, BEV, and PHEV registrations
- Charging stations and charging points
- EV-per-station ratio
- Coverage gap
- Demand score
- Priority score
- Infrastructure status
- City tier
- EV market share and adoption stage

### 6 Analytical Views

| View | Purpose |
|------|---------|
| **`v_top_priority_cities`** | Finds cities with the highest average priority score |
| **`v_monthly_mom_growth`** | Tracks month-over-month EV growth by country |
| **`v_infra_status_profile`** | Profiles infrastructure status groups by gap and priority |
| **`v_charging_deserts`** | Highlights the most underserved charging markets |
| **`v_city_tier_gap`** | Compares coverage gaps across city tiers |
| **`v_yoy_ev_growth`** | Compares year-over-year EV and station growth |

### Example Query

```sql
SELECT *
FROM v_top_priority_cities
ORDER BY avg_priority_score DESC
LIMIT 10;
```

---

## 🔌 API / Function Reference

### Database Functions (`db_connection.py`)

#### **`test_connection() -> bool`**
Checks whether MySQL credentials and connectivity are valid.

#### **`get_engine()`**
Creates and returns a SQLAlchemy engine using the configured MySQL credentials.

#### **`ensure_schema(verbose=True)`**
Creates the database, main table, and analytical SQL views.

#### **`upload_csv_to_mysql(csv_path: str) -> int`**
Loads the CSV into MySQL, normalizes `infra_status`, truncates old data, and inserts fresh rows.

### App Functions (`app.py`)

#### **`load_data()`**
Loads the main CSV dataset used by the dashboard.

#### **`build_country_summary(frame)`**
Builds country-level summary metrics for charts and KPIs.

#### **`build_city_summary(frame)`**
Builds city-level ranking summaries including average priority and gap.

#### **`build_monthly_summary(frame)`**
Creates time-series aggregates for monthly trend analysis.

#### **`compute_feature_importance(frame)`**
Generates feature-importance style insight for EV demand analysis.

#### **`prepare_forecast_frame(frame)`**
Standardizes forecast columns so the Forecast tab can render properly.

---

## 📸 Screenshots

> Replace the image paths below with your actual uploaded screenshots.

### 🏠 Dashboard Home / Overview
![Overview](Screenshots/Project/overview.png)

### 🏙️ Priority Cities
![Priority Cities](Screenshots/Project/priority-cities.png)

### 📈 Trends Analysis
![Trends](Screenshots/Project/trends.png)

### 🗺️ Geographic Analysis
![Geography](Screenshots/Project/geography.png)

### 🔍 SQL Insights
![SQL Insights](Screenshots/Project/sql-insights.png)

### 📉 Forecast View
![Forecast](Screenshots/Project/forecast.png)

---

## 📊 Power BI Screenshots

> Is section mein apne Power BI dashboard ke screenshots add karo.

### 📌 Power BI Dashboard Overview
![Power BI Overview](Screenshots/PowerBI/dashboard-overview.png)

### 🌍 Country-Level EV Analysis
![Country Analysis](Screenshots/PowerBI/country-analysis.png)

### 🏙️ City Gap / Priority Analysis
![City Gap Analysis](Screenshots/PowerBI/city-gap-analysis.png)

### 📋 Executive Summary View
![Executive Summary](Screenshots/PowerBI/executive-summary.png)

---

## 🖼️ Project Screenshots

> Is section mein project ke extra screenshots add kar sakte ho jaise notebook outputs, SQL results, dataset preview, ya deployment view.

### 📓 Notebook Analysis
![Notebook Analysis](Screenshots/Project/notebook-analysis.png)

### 🗄️ SQL Query Output
![SQL Output](Screenshots/Project/sql-output.png)

### 📁 Dataset Preview
![Dataset Preview](Screenshots/Project/dataset-preview.png)

### 🚀 Streamlit Deployment
![Deployment](Screenshots/Project/deployment.png)

---

## 🤝 Contributing

Contributions are welcome.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test the dashboard and SQL flow**
5. **Commit with a clear message**
6. **Open a pull request**

### Contribution Guidelines

- ✅ Write clean and readable Python code
- ✅ Keep SQL queries well-documented
- ✅ Avoid hardcoding credentials
- ✅ Update README when features change
- ✅ Add screenshots if UI changes are significant
- ✅ Test both CSV and MySQL workflows before submitting

---

## 🚀 Future Enhancements

### Planned Features

#### Phase 1 — Dashboard Experience
- [ ] Add smarter KPI comparisons and benchmark cards
- [ ] Add saved filter presets
- [ ] Add PDF / report export
- [ ] Add mobile-friendly responsive improvements

#### Phase 2 — Advanced Analytics
- [ ] Add dedicated forecasting pipeline with Prophet / XGBoost
- [ ] Add clustering for city segmentation
- [ ] Add anomaly detection for infrastructure stress
- [ ] Add charger demand forecasting by city tier

#### Phase 3 — Integrations
- [ ] Add Power BI file / dashboard link integration
- [ ] Add REST API endpoints for serving filtered insights
- [ ] Add cloud database deployment option
- [ ] Add Docker support for one-command setup

#### Phase 4 — Data & Engineering
- [ ] Break `app.py` into modules for maintainability
- [ ] Add unit tests and logging
- [ ] Add automated data validation checks
- [ ] Add CI/CD pipeline for deployment

### Technical Debt

- [ ] Refactor large dashboard sections into reusable modules
- [ ] Improve exception handling around optional forecast files
- [ ] Add stronger schema validation before uploads
- [ ] Add typing and documentation across the codebase

---

## 📞 Contact

### Developer Information

**Sumersing Patil**
- 🐙 GitHub: [Sumersingpatil2694](https://github.com/Sumersingpatil2694)
- 💼 LinkedIn: [Sumersing Patil AI](https://www.linkedin.com/in/sumersing-patil-ai/)
- 📧 Email: your-email@example.com

### Project Links

- **Repository**: [Add your GitHub repo link here](https://github.com/yourusername/ev-charging-demand-analysis)
- **Live Demo**: [Add your Streamlit deployment link here](https://streamlit.io/)
- **Power BI Dashboard**: [Add your Power BI share link here](https://app.powerbi.com/)

---

## 🙏 Acknowledgments

- **Streamlit** — For the rapid dashboard framework
- **Plotly** — For beautiful interactive visuals
- **MySQL** — For the analytics storage layer
- **Pandas / NumPy / Scikit-learn** — For the Python analytics ecosystem
- **Power BI** — For stakeholder-friendly BI presentation
- **Python Community** — For open-source tools and libraries

---

## ❓ FAQ

### Does the project require MySQL?
No. The dashboard can run from CSV input, but MySQL is recommended for the SQL analytics workflow.

### Is forecasting mandatory?
No. The forecast tab is optional and becomes active when `forecast.csv` is provided.

### Can I add Power BI visuals to this project?
Yes. Use the dedicated **Power BI Screenshots** section in this README or attach a Power BI share link in the Project Links section.

### Can I use this project in my portfolio?
Absolutely. This project is portfolio-friendly because it demonstrates Python, SQL, Streamlit, visualization, and business insight generation in one workflow.

---

### ⭐ If you found this project helpful, please give it a star! ⭐
