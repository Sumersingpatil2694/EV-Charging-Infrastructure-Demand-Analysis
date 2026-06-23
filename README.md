# 🔋 EV Charging Station Demand Analysis

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
- [API Reference](#-api-reference)
- [Screenshots](#-screenshots)
- [Power BI Screenshots](#-power-bi-screenshots)
- [Contributing](#-contributing)
- [Future Enhancements](#-future-enhancements)
- [Contact](#-contact)
- [Acknowledgments](#-acknowledgments)
- [FAQ](#-faq)

---

## 🎯 Introduction

**EV Charging Station Demand Analysis** is a premium analytics web application designed to study **EV adoption**, **charging infrastructure adequacy**, and **investment priority** across cities and countries. The project combines a **Streamlit dashboard**, **MySQL database**, **SQL analytical views**, and optional **forecast-ready inputs** to help identify underserved EV markets and support smarter charging network expansion.

### 🌟 Why Choose This System?

- ✅ **14,120+ records** available in the EV dataset
- ✅ **27 analytical fields** including EV demand, charging stations, coverage gap, and priority score
- ✅ **Interactive Dashboard** with multiple analytical sections
- ✅ **SQL-Powered Insights** for business-ready infrastructure analysis
- ✅ **Premium UI** with black and neon-green styling
- ✅ **CSV Export Support** for filtered datasets and summaries
- ✅ **Forecast-Ready Architecture** with optional forecast integration
- ✅ **Portfolio-Ready Project** with Streamlit, SQL, analytics, and Power BI support

---

## ✨ Features

### 🔍 Core Features

| Feature | Description |
|---------|-------------|
| **Interactive Dashboard** | Streamlit-based analytical dashboard with a premium black and neon-green theme |
| **Investment Priority Analysis** | Ranks cities using `priority_score`, `coverage_gap`, and EV demand indicators |
| **Trend Monitoring** | Tracks month-on-month and year-over-year EV adoption growth |
| **Infrastructure Gap Detection** | Highlights underserved cities with charging shortages |
| **Geographic Visualization** | Interactive map view for city-level EV and charging metrics |
| **SQL Insights** | Business-ready analytical views translated into dashboard visuals |
| **Forecast Support** | Optional forecast tab that reads a `forecast.csv` file when available |
| **CSV Downloads** | Export filtered dashboard data and priority city summaries directly |

### 🎨 UI Features

- 🌙 **Dark Premium Theme** - NVIDIA-inspired black and neon-green design
- ⚡ **KPI Cards** - Executive-style metric cards for total EV demand, charging stations, and coverage gap
- 📊 **Interactive Plotly Charts** - Bar, line, pie, bubble, and map visualizations
- 🧭 **Advanced Sidebar Filters** - Country, city, year range, city tier, infrastructure status, and EV-per-station stress filter
- 🗺️ **Mapbox Visuals** - Location-based market exploration
- ⬇️ **Download Buttons** - One-click CSV export for decision-ready data

### 📊 Advanced Features

- **Overview Analytics**: High-level KPIs, country comparison, and infrastructure health summary
- **Priority Cities Ranking**: Identify the best cities for new EV charging investment
- **Trends Analysis**: Compare EV growth across countries over time
- **Feature Intelligence**: Correlation-based or feature-importance style insight generation
- **SQL Business Questions**: Dedicated tab for analytical query views
- **Forecast Outlook**: Future EV demand visualization if forecast data is provided

---

## 🛠️ Tech Stack

### Backend
- **Python 3.9+**
- **Pandas / NumPy** - Data processing and transformation
- **Scikit-learn** - Feature intelligence and model-style workflows
- **SQLAlchemy** - Database engine integration
- **PyMySQL** - MySQL connectivity
- **python-dotenv** - Environment variable handling

### Frontend
- **Streamlit** - Interactive dashboard framework
- **Plotly** - Interactive charting and map visualizations
- **Matplotlib / Seaborn** - Supporting data visualization stack
- **HTML/CSS** - Custom styling and KPI cards

### Database & Data
- **MySQL 8.0+** - Storage for EV charging analytics data
- **SQL Views** - Reusable business insights layer
- **CSV Dataset Pipeline** - Local dataset ingestion for dashboard and SQL views

### Analytics Workflow

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

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Add Dataset Files

Place the dataset file in the project directory:

| File | Description |
|------|-------------|
| `europe_ev_dataset.csv` | Main EV charging analysis dataset |
| `ev_data_cleaned_final.csv` | Optional cleaned dataset |
| `forecast.csv` | Optional forecast input |
| `models_summary.csv` | Optional model comparison summary |

### Step 5: Configure MySQL

1. Create a `.env` file in the project root
2. Add your MySQL credentials
3. Ensure the database name matches the SQL script / helper file

### Step 6: Create Database Schema

Run the SQL script in MySQL:

```bash
mysql -u root -p < ev_charging_analysis.sql
```

Or use the helper flow in `db_connection.py`.

### Step 7: Run Application

```bash
streamlit run app.py
```

The application will open at: `http://localhost:8501`

---

## ⚙️ Configuration

### `.env` File

Create a `.env` file with your own values:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=ev_charging_analysis
```

> Never commit your real password or secrets to GitHub.

### Key Input Files

The dashboard can automatically work with these files when present:

```text
europe_ev_dataset.csv
ev_data_cleaned_final.csv
forecast.csv
models_summary.csv
```

### Customization Options

**Dashboard Filters:**
- Country
- City
- Year range
- City tier
- Infrastructure status
- EV-per-station threshold

**UI Theme:**
Edit the custom CSS inside `app.py` to change colors, KPI styling, and section appearance.

**Database Notes:**
- Uses **PyMySQL** instead of `mysql-connector-python`
- Helps avoid common MySQL 8 authentication plugin issues
- Default database name is `ev_charging_analysis`

---

## 🎮 Usage

### 1. **Overview Dashboard** 🏠

- View total EV registrations
- Monitor charging stations
- Analyze coverage gap
- Compare countries at a high level

### 2. **Priority Cities** 🏙️

This section helps identify:
- Cities with the highest charging demand pressure
- High-priority investment markets
- EV demand vs charging availability
- Exportable city summary CSV

### 3. **Trends Analysis** 📈

Track market growth with:
- Month-on-month EV growth
- Year-over-year EV growth
- Country-wise trend comparisons
- Growth performance across selected markets

### 4. **Geographic Analysis** 🗺️

Explore city-level EV infrastructure using:
- EV registrations
- Charging stations
- Coverage gap
- Demand / priority indicators

### 5. **Feature Intelligence** 🧠

Understand which variables are most associated with EV registrations and charging demand patterns using feature-based analytics.

### 6. **SQL Insights** 🔍

View business-ready insights generated from SQL logic:

- Top Priority Cities
- Month-on-Month Growth
- Infrastructure Status Profile
- Charging Deserts
- City Tier Gap
- Year-over-Year Growth

### 7. **Forecast View** 📉

If `forecast.csv` is available, the Forecast tab can display:

- Forecasted EV demand lines
- Country-level forecast comparison
- Forecast intervals
- Downloadable forecast data

### 8. **Power BI Dashboard** 📊

You can also present the same project insights in **Power BI** for stakeholder-friendly storytelling and executive reporting.

Suggested Power BI pages:
- Executive Summary
- Country-Level EV Adoption Analysis
- City Priority & Infrastructure Gap Analysis
- Forecast & Growth Trends

### 9. **About Section** 👤

The About section summarizes:
- Project objective
- Dataset context
- Tech stack
- Key findings
- Developer information

---

## 🔬 How It Works

### Analytics Workflow

```mermaid
graph LR
A[CSV Dataset] --> B[Data Cleaning]
B --> C[MySQL Database]
C --> D[SQL Analytical Views]
D --> E[Streamlit Dashboard]
E --> F[Insights, Rankings, Maps, Downloads]
```

### Step-by-Step Process

#### 1. **Dataset Loading**

The app loads EV charging data from local CSV files using a resilient loader that checks the project folder first.

#### 2. **Data Standardization**

Country names, city tiers, and infrastructure labels are cleaned and standardized for better filtering and chart quality.

#### 3. **Database Integration**

The cleaned dataset is loaded into the MySQL table `ev_data` for structured analysis and reusable SQL workflows.

#### 4. **SQL Layer**

SQL views answer recurring business questions such as:
- Which cities have the highest priority score?
- Which locations are charging deserts?
- Which country is growing fastest month-over-month?

#### 5. **Dashboard Analytics**

The app computes:
- Country-level summaries
- City-level summaries
- Monthly aggregates
- Priority rankings
- Gap analysis
- Feature-based insights

#### 6. **Export Layer**

Filtered data and top priority city views can be exported as CSV directly from the app.

#### 7. **Forecast Extension**

A future-demand layer can be activated by adding a compatible `forecast.csv` file to the project directory.

---

## 📁 Project Structure

```text
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

| File | Purpose | Required |
|------|---------|----------|
| `app.py` | Main Streamlit dashboard application | ✅ Yes |
| `db_connection.py` | MySQL helper for schema creation and CSV upload | ✅ Yes |
| `ev_charging_analysis.sql` | Database schema and analytical SQL views | ✅ Yes |
| `europe_ev_dataset.csv` | Main EV charging dataset | ✅ Yes |
| `EV_Charging_Analysis.ipynb` | Notebook for analysis and experimentation | ⚠️ Optional |
| `requirements.txt` | Python dependencies | ✅ Yes |
| `.env` | Local environment variables for MySQL | ⚠️ Required for DB mode |
| `forecast.csv` | Forecast-ready dataset | ⚠️ Optional |

---

## 🔌 API Reference

### Database Functions (`db_connection.py`)

#### **`test_connection() -> bool`**
Checks whether MySQL credentials and connectivity are valid.

#### **`get_engine()`**
Creates and returns a SQLAlchemy engine using the configured MySQL credentials.

#### **`ensure_schema(verbose=True)`**
Creates the database, main table, and analytical SQL views.

#### **`upload_csv_to_mysql(csv_path: str) -> int`**
Loads the CSV into MySQL, normalizes infrastructure labels, truncates old data, and inserts fresh rows.

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

### SQL Views Used

| View | Purpose |
|------|---------|
| **`v_top_priority_cities`** | Finds cities with the highest average priority score |
| **`v_monthly_mom_growth`** | Tracks month-over-month EV growth by country |
| **`v_infra_status_profile`** | Profiles infrastructure status groups by gap and priority |
| **`v_charging_deserts`** | Highlights underserved charging markets |
| **`v_city_tier_gap`** | Compares coverage gaps across city tiers |
| **`v_yoy_ev_growth`** | Compares year-over-year EV and station growth |

---

## 📸 Screenshots

### 🏠 Dashboard Overview
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

> Add your Power BI dashboard screenshots in this section to make the project more portfolio-ready.

### 📌 Dashboard Overview
![Power BI Dashboard Overview](Screenshots/PowerBI/dashboard-overview.png)

### 🌍 Country-Level EV Analysis
![Country Analysis](Screenshots/PowerBI/country-analysis.png)

### 🏙️ City Gap & Priority Analysis
![City Gap Analysis](Screenshots/PowerBI/city-gap-analysis.png)

### 📋 Executive Summary
![Executive Summary](Screenshots/PowerBI/executive-summary.png)

### Suggested Power BI Insights to Highlight

- Total EV registrations by country
- Charging stations by country and city
- Coverage gap by city tier
- Priority score distribution
- Fastest-growing EV markets
- Top underserved charging markets

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

### How to Contribute

1. **Fork the Repository**
```bash
git clone https://github.com/yourusername/ev-charging-demand-analysis.git
```

2. **Create Feature Branch**
```bash
git checkout -b feature/AmazingFeature
```

3. **Make Changes**
- Write clean and readable Python code
- Improve SQL queries if needed
- Update dashboard or documentation

4. **Commit Changes**
```bash
git commit -m "Add: Amazing new feature"
```

5. **Push to Branch**
```bash
git push origin feature/AmazingFeature
```

6. **Open Pull Request**
- Provide a clear description
- Add screenshots if applicable
- Mention related improvements or fixes

### Contribution Guidelines

- ✅ Write clean and readable Python code
- ✅ Keep SQL queries well-documented
- ✅ Avoid hardcoding credentials
- ✅ Update README when features change
- ✅ Add screenshots if UI changes are significant
- ✅ Test both CSV and MySQL workflows before submitting

### Code Style

```python
def load_data():
    """
    Load EV dataset for dashboard analytics
    
    Returns:
        DataFrame: Cleaned EV dataset
    """
    try:
        df = pd.read_csv("europe_ev_dataset.csv")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
```

### Bug Reports

To report a bug:
1. Go to GitHub Issues
2. Provide a clear title
3. Describe steps to reproduce
4. Explain expected vs actual behavior
5. Add screenshots if possible
6. Mention system information

### Feature Requests

To request a feature:
1. Check existing issues first
2. Clearly describe the feature
3. Explain the use case
4. Provide examples if possible

---

## 🚀 Future Enhancements

### Planned Features

#### Phase 1 - Dashboard Experience
- [ ] Add smarter KPI comparisons and benchmark cards
- [ ] Add saved filter presets
- [ ] Add PDF/report export
- [ ] Improve mobile responsiveness

#### Phase 2 - Advanced Analytics
- [ ] Add dedicated forecasting pipeline with Prophet / XGBoost
- [ ] Add clustering for city segmentation
- [ ] Add anomaly detection for infrastructure stress
- [ ] Add charger demand forecasting by city tier

#### Phase 3 - Integrations
- [ ] Add Power BI dashboard link integration
- [ ] Add REST API endpoints for filtered insights
- [ ] Add cloud database deployment support
- [ ] Add Docker support for one-command setup

#### Phase 4 - Data Engineering
- [ ] Break `app.py` into smaller modules
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

- **Streamlit** - For the rapid dashboard framework
- **Plotly** - For beautiful interactive visuals
- **MySQL** - For the analytics storage layer
- **Pandas / NumPy / Scikit-learn** - For the Python analytics ecosystem
- **Power BI** - For stakeholder-friendly BI presentation
- **Python Community** - For open-source tools and libraries

---

## ❓ FAQ

### Does the project require MySQL?
No. The dashboard can run from CSV input, but MySQL is recommended for the SQL analytics workflow.

### Is forecasting mandatory?
No. The Forecast tab is optional and becomes active when `forecast.csv` is provided.

### Can I add Power BI visuals to this project?
Yes. Use the Power BI screenshots section or attach a Power BI share link in the Project Links section.

### Can I use this project in my portfolio?
Absolutely. This project is portfolio-friendly because it demonstrates Python, SQL, Streamlit, visualization, and business insight generation in one workflow.

---

### ⭐ If you found this project helpful, please give it a star! ⭐
