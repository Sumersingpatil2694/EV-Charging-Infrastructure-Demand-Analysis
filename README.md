# 🔋  EV Charging Infrastructure Demand Analysis

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-purple.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**An end-to-end EV infrastructure analytics project that analyzes charging demand, identifies priority investment cities, and visualizes infrastructure gaps across city-level EV markets**

[Live Demo](https://ev-charging-infrastructure-demand-analysis-june-2026.streamlit.app/) • [Features](#-features) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Power BI dashboards](#-power-bi-screenshots)

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
- [Function Reference](#-function-reference)
- [Screenshots](#-screenshots)
- [Power BI Screenshots](#-power-bi-screenshots)
- [Project Screenshots](#-project-screenshots)
- [Future Enhancements](#-future-enhancements)
- [Contact](#-contact)

---

## 🎯 Introduction

**EV Charging Infrastructure Demand Analysis** is a premium dark-theme analytics project designed to study **EV adoption**, **charging infrastructure adequacy**, and **investment priority** across European city-level markets. The solution combines a **Streamlit dashboard**, **MySQL database**, **SQL analytical views**, **CSV-based exploration**, and a **Jupyter notebook workflow** to support smarter charging network expansion.

The project follows a practical analytics pipeline: EV data is loaded from CSV → cleaned and standardized → stored in MySQL → queried through reusable SQL views → presented in an interactive Streamlit dashboard with KPIs, filters, trends, maps, and downloadable insights.

### 🌟 Why This Project Stands Out

- ✅ **14,120+ records** in the provided EV dataset
- ✅ **27 analytical fields** covering EV demand, station density, coverage gap, growth, and priority score
- ✅ **8 dashboard sections** including overview, priority cities, trends, geography, feature intelligence, SQL insights, forecast, and about
- ✅ **6 SQL analytical views** for business-ready EV infrastructure insights
- ✅ **Premium NVIDIA-inspired UI** with black + neon green theme styling
- ✅ **CSV export support** for filtered records and priority city summaries
- ✅ **Power BI screenshot section included** for portfolio-ready documentation

---

## ✨ Features

### 🔍 Core Features

| Feature | Description |
|---------|-------------|
| **Interactive Dashboard** | Streamlit dashboard with premium dark UI and interactive controls |
| **Priority City Analysis** | Ranks cities using `priority_score`, `coverage_gap`, and EV demand indicators |
| **Infrastructure Gap Detection** | Highlights underserved cities with charging shortages |
| **Trend Analysis** | Tracks monthly and yearly EV growth patterns across countries |
| **Geographic Visualization** | Interactive city-level map for EV and charging metrics |
| **SQL Insights Layer** | Six analytical views transformed into dashboard-ready business insights |
| **Forecast Support** | Optional forecast tab when compatible forecast files are available |
| **Data Export** | Download filtered dataset and priority-city outputs as CSV |

### 🎨 Dashboard Experience

- 🌙 **Dark Premium Theme** with NVIDIA-inspired black and neon-green design language
- ⚡ **Executive KPI Cards** for EV demand, infrastructure availability, and coverage gaps
- 🧭 **Advanced Sidebar Filters** for geography, timeline, city tier, infrastructure status, and EV-per-station stress
- 🗺️ **Map-based Analytics** using latitude/longitude city points
- 📊 **Interactive Plotly Visuals** including bar, line, pie, bubble, and map charts
- ⬇️ **Download Actions** for quick export of filtered business insights

### 📊 Analytical Highlights

- **Overview Analytics** for market-level KPIs and infrastructure health
- **Priority Cities Ranking** to identify top investment opportunities
- **Trend Monitoring** for month-on-month and year-over-year EV growth
- **Feature Intelligence** to understand demand-driving variables
- **SQL Business Questions** answered through reusable database views
- **Forecast-ready Architecture** for future-demand extension

---

## 🛠️ Tech Stack

### Backend / Analytics
- **Python 3.9+**
- **Pandas / NumPy** — data processing and transformation
- **Scikit-learn** — feature intelligence and model-style analysis
- **SQLAlchemy** — database engine integration
- **PyMySQL** — MySQL connectivity
- **python-dotenv** — environment variable management

### Frontend / Visualization
- **Streamlit** — interactive dashboard framework
- **Plotly** — advanced charts and geo visualizations
- **Matplotlib / Seaborn** — supporting visualization ecosystem
- **Custom HTML/CSS** — premium dashboard cards and layout styling

### Database
- **MySQL 8.0+** — EV analytics storage layer
- **SQL Views** — reusable business insight layer

### Notebook Workflow
- **Jupyter Notebook** — exploratory analysis and experimentation
- **CSV Dataset Pipeline** — direct local dataset support
- **Optional Forecast Inputs** — extend dashboard with predictive visuals

---

## 📦 Installation

### Prerequisites

```bash
# Python 3.9+
python --version

# MySQL 8.0+
mysql --version

# pip
pip --version
```

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ev-charging-demand-analysis.git
cd ev-charging-demand-analysis
```

> Replace the repository URL with your actual GitHub repository link.

### Step 2: Create a Virtual Environment

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

### Step 4: Keep Required Files in Project Root

```text
app.py
db_connection.py
ev_charging_analysis.sql
europe_ev_dataset.csv
requirements.txt
```

### Step 5: Configure Environment Variables

Create a `.env` file in the root directory.

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=ev_charging_analysis
```

### Step 6: Create Database Schema

```bash
mysql -u root -p < ev_charging_analysis.sql
```

Or initialize the schema using the Python helper functions from `db_connection.py`.

### Step 7: Run the Streamlit App

```bash
streamlit run app.py
```

---

## ⚙️ Configuration

### Supported Files

The dashboard can work with the following files:

- `europe_ev_dataset.csv` — main EV charging analysis dataset
- `forecast.csv` — optional forecast file for future demand charts
- `models_summary.csv` — optional model / evaluation summary

### Dependency List

```text
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
python-dotenv>=1.0.0
PyMySQL>=1.1.0
sqlalchemy>=2.0.0
```

### Database Notes

- The project uses **PyMySQL** for MySQL connectivity
- Environment variables are loaded through **python-dotenv**
- Default database name is **`ev_charging_analysis`**
- The helper module can create schema and upload CSV data into MySQL

---

## 🎮 Usage

### 1. **📊 Overview**
Use this section to monitor:
- Total EV registrations
- Total charging stations
- Average coverage gap
- Country-level infrastructure health

### 2. **🏙️ Priority Cities**
Use this section to identify:
- High-priority EV charging investment markets
- Cities with strong demand pressure
- Bubble comparison of EV demand vs infrastructure availability
- Exportable priority-city summaries

### 3. **📈 Trends**
Analyze:
- Month-on-month EV growth
- Year-over-year EV growth
- Country-wise trend comparisons
- Demand momentum across selected markets

### 4. **🗺️ Geography**
Explore city-level EV infrastructure using:
- EV registrations
- Charging stations
- Coverage gap
- Demand and priority metrics

### 5. **🧠 Feature Intelligence**
Understand which variables are most associated with EV registrations and demand patterns using feature-importance style analysis.

### 6. **🔍 SQL Insights**
View reusable SQL-driven insights such as:
- Top Priority Cities
- Monthly MoM Growth
- Infrastructure Status Profile
- Charging Deserts
- City Tier Gap
- YoY Growth

### 7. **📉 Forecast**
If `forecast.csv` is available, this tab can display:
- Forecasted EV demand trends
- Country-wise forecast comparison
- Confidence interval style ranges

### 8. **👤 About**
Summarizes project goal, dataset context, tech stack, and portfolio-ready value.

---

## 🔬 How It Works

### End-to-End Workflow

```text
CSV Dataset
   ↓
Data Cleaning / Standardization
   ↓
MySQL Database Table (`ev_data`)
   ↓
SQL Analytical Views
   ↓
Streamlit Dashboard
   ↓
Insights, Rankings, Filters, Maps, and Downloads
```

### Processing Steps

#### 1. Dataset Loading
The app loads EV data from the project directory and uses local CSV inputs as the primary source.

#### 2. Standardization
Country labels, city tiers, and infrastructure status values are normalized for better filtering and chart consistency.

#### 3. Interactive Filtering
Users can filter by country, year range, city tier, infrastructure status, and charging stress level.

#### 4. SQL Analytics Layer
MySQL stores the data in `ev_data`, while SQL views answer recurring business questions.

#### 5. Insight Generation
The dashboard builds country summaries, city rankings, growth views, map analytics, and feature intelligence outputs.

#### 6. Export Layer
Filtered datasets and priority-city summaries can be exported directly from the dashboard.

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
| `ev_charging_analysis.sql` | Database schema and analytical SQL views |
| `europe_ev_dataset.csv` | Main EV charging analysis dataset |
| `EV_Charging_Analysis.ipynb` | Notebook for analysis and experimentation |
| `requirements.txt` | Python dependencies |
| `.env` | Local environment variables for MySQL |
| `Screenshots/` | Folder for Streamlit and Power BI screenshots |

---

## 🗄️ Database & SQL Views

### Main Table

#### **`ev_data`**
Stores city-level EV and infrastructure metrics such as:
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

### Analytical Views

| View | Purpose |
|------|---------|
| **`v_top_priority_cities`** | Finds cities with the highest average priority score |
| **`v_monthly_mom_growth`** | Tracks month-over-month EV growth by country |
| **`v_infra_status_profile`** | Profiles infrastructure groups by gap and priority |
| **`v_charging_deserts`** | Highlights the most underserved charging markets |
| **`v_city_tier_gap`** | Compares coverage gaps across city tiers |
| **`v_yoy_ev_growth`** | Compares EV growth with charging station growth |

### Example Query

```sql
SELECT *
FROM v_top_priority_cities
ORDER BY avg_priority_score DESC
LIMIT 10;
```

---

## 🔌 Function Reference

### `db_connection.py`

- **`test_connection()`** — validates MySQL connectivity
- **`get_engine()`** — returns a SQLAlchemy engine
- **`ensure_schema(verbose=True)`** — creates the database, table, and analytical views
- **`upload_csv_to_mysql(csv_path)`** — loads CSV data into MySQL after resetting the main table

### `app.py`

- **Dataset loading** from CSV-based sources
- **Country and city summary generation**
- **Monthly trend aggregation**
- **Feature intelligence / model-style insight support**
- **Forecast preparation** when optional files are present

---

## 📸 Screenshots

>  Screenshots below are taken from the live Streamlit deployment. Click the Live Demo link above to explore the interactive dashboard.

### 🏠 Dashboard Home / Overview
![Overview](https://github.com/Sumersingpatil2694/EV-Charging-Infrastructure-Demand-Analysis/blob/main/Screenshots/Dashboard%20Home%20Overview.png)

### 🏙️ Priority Cities
![Priority Cities](https://github.com/Sumersingpatil2694/EV-Charging-Infrastructure-Demand-Analysis/blob/main/Screenshots/Priority%20Cities.png)

### 📈 Trends Analysis
![Trends](https://github.com/Sumersingpatil2694/EV-Charging-Infrastructure-Demand-Analysis/blob/main/Screenshots/Trends%20Analysis.png)

### 🗺️ Geographic Analysis
![Geography](https://github.com/Sumersingpatil2694/EV-Charging-Infrastructure-Demand-Analysis/blob/main/Screenshots/Geographic%20Analysis.png)

### 🔍 SQL Insights
![SQL Insights](https://github.com/Sumersingpatil2694/EV-Charging-Infrastructure-Demand-Analysis/blob/main/Screenshots/SQL%20Insights.png)

### 📉 Forecast View
![Forecast](https://github.com/Sumersingpatil2694/EV-Charging-Infrastructure-Demand-Analysis/blob/main/Screenshots/Forecast%20View.png)

---

## 📊 Power BI Screenshots

> Is section mein aap apne Power BI dashboard ke screenshots bilkul isi structure mein add kar sakte ho.

### 📌 Power BI Dashboard Overview
![Power BI Overview](Screenshots/PowerBI/dashboard-overview.png)

### 🌍 Country-Level EV Analysis
![Country Analysis](Screenshots/PowerBI/country-analysis.png)

### 🏙️ City Gap / Priority Analysis
![City Gap Analysis](Screenshots/PowerBI/city-gap-analysis.png)

### 📋 Executive Summary View
![Executive Summary](Screenshots/PowerBI/executive-summary.png)

---

## 🚀 Future Enhancements

- [ ] Add advanced forecast models and evaluation comparison
- [ ] Add clustering for city segmentation
- [ ] Add anomaly detection for infrastructure stress
- [ ] Add PDF / report export
- [ ] Add dashboard modularization for maintainability
- [ ] Add unit tests and data validation checks
- [ ] Add Docker and cloud deployment support
- [ ] Add direct Power BI link integration

---

## 📞 Contact

### Developer Information

**Your Name**
- 🐙 GitHub: [Sumersingpatil2694](https://github.com/Sumersingpatil2694)
- 💼 LinkedIn: [Sumersing-patil](https://www.linkedin.com/in/sumersing-patil-ai/)
- 📧 Email: sumerrajput0193@gmail.com

### Project Links

- **Repository**: [GitHub repo](https://github.com/Sumersingpatil2694/EV-Charging-Infrastructure-Demand-Analysis)
- **Live Demo**: [Streamlit Live Demo](https://ev-charging-infrastructure-demand-analysis-june-2026.streamlit.app/)
- **Power BI Dashboard**: [Power BI](https://app.powerbi.com/)

---

## 🙏 Acknowledgments

- **Streamlit** — interactive dashboard framework
- **Plotly** — advanced charting and geo visualizations
- **MySQL** — structured analytics storage layer
- **Pandas / NumPy / Scikit-learn** — Python analytics ecosystem
- **Power BI** — stakeholder-friendly BI storytelling

---

## ❓ FAQ

### Does this project require MySQL?
No. The dashboard can run from CSV input, but MySQL is recommended for the SQL analytics workflow.

### Is forecasting mandatory?
No. The forecast section is optional and becomes active only when compatible forecast files are provided.

### Can I add Power BI visuals to this project?
Yes. Use the dedicated **Power BI Screenshots** section or add your Power BI share link in the Project Links section.

### Is this project portfolio-ready?
Yes. It demonstrates Python, SQL, Streamlit, visualization, and business insight generation in one end-to-end workflow.

---

### ⭐ If you found this project useful, give it a star! ⭐
