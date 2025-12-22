# Stock_Analysis

## Project Overview

This project is an end-to-end stock market analysis and visualization dashboard built using Python, Pandas, Plotly, and Streamlit.
It processes 14 months of daily stock data (YAML format) for NIFTY 50 companies, performs financial analysis, and presents insights through an interactive web dashboard.

The dashboard helps users:

--Analyze stock performance year-wise

--Identify top gainers and losers

--Understand volatility and sector-wise trends

--Explore correlations between stocks

## Data Pipeline (ETL Flow)
## Data Ingestion

--Reads multiple YAML files from monthly folders

--Each YAML file represents daily stock data

--All files are combined into a single DataFrame

## Data Cleaning & Feature Engineering

--Convert date to datetime

--Extract year from date

--Calculate:

    --Daily Returns

    --Cumulative Returns

    --Monthly Returns

    --Volatility

    --Merge sector information

    --Handle missing values

    --Fix incorrect or missing sector mappings

## Data Export

Final cleaned dataset saved as:

data/nifty_50.csv

## Dashboard Features (Streamlit App)
## Tab 1: Market Overview

Filters

    --Year selector

KPIs

    --Total stocks traded

    --Average daily return

    --Best performing stock

    --Worst performing stock

Visualizations

    --Top 10 most volatile stocks

    --Cumulative return (Top 5 stocks)

    --Sector-wise average returns

    --Stock correlation heatmap

## Tab 2: Monthly Top Gainers & Losers

    --Monthly performance analysis

    --Top 5 gainers and losers for each month

    --Interactive grouped bar charts

    --Multi-panel layout for all months

## Tab 3: Raw Data

--View complete dataset

--Download processed CSV file


## How to Run the Project

## 1. Clone the Repository

git clone <your-github-repo-link>
cd Stock_Analysis


## 2. Install Dependencies

pip install pandas numpy pyyaml matplotlib seaborn plotly streamlit

## 3.Generate Final Dataset

yaml_files_load.ipynb


## 4. Launch Dashboard

streamlit run app.py


## Key Insights from the Project

    --Identifies high-volatility stocks

    --Highlights consistent performers

    --Reveals sector-level trends

    --Shows correlation between stock returns

    --Helps understand market behavior over time

