import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Stock Market Dashboard",
    layout="wide"
)

st.title("📊 Stock Market Analysis Dashboard")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = pd.read_csv(
    "/home/shigilsasi/code/Guvi_Projects/Stock_Analysis/data/nifty_50.csv",
    parse_dates=['date']
)

# -------------------------------------------------
# TABS
# -------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📈 Market Overview",
    "🔥 Top Gainers & Losers",
    "📄 Raw Data"
])

# =================================================
# TAB 1: MARKET OVERVIEW (Q1–Q4)
# =================================================
with tab1:

    st.subheader("📈 Market Overview")

    # YEAR FILTER (ONLY FOR THIS TAB)
    selected_year = st.selectbox(
        "Select Year",
        sorted(df['year'].unique())
    )

    df_year = df[df['year'] == selected_year]

    # ---------------------------
    # 1️⃣ Volatility Analysis
    # ---------------------------
    st.subheader("1️⃣ Top 10 Most Volatile Stocks")

    volatility = (
        df_year.groupby('Ticker')['daily_return']
        .std()
        .sort_values(ascending=False)
        .head(10)
        .reset_index(name='Volatility')
    )

    fig_vol = px.bar(
        volatility,
        x='Ticker',
        y='Volatility',
        title="Top 10 Most Volatile Stocks"
    )

    st.plotly_chart(fig_vol, use_container_width=True)

    # ---------------------------
    # 2️⃣ Cumulative Return
    # ---------------------------
    st.subheader("2️⃣ Cumulative Return – Top 5 Performing Stocks")

    top_5 = (
        df_year.sort_values('date')
        .groupby('Ticker')
        .tail(1)
        .sort_values('cumulative_return', ascending=False)
        .head(5)['Ticker']
    )

    cum_df = df_year[df_year['Ticker'].isin(top_5)]

    fig_cum = px.line(
        cum_df,
        x='date',
        y='cumulative_return',
        color='Ticker',
        title="Cumulative Return Over Time"
    )

    st.plotly_chart(fig_cum, use_container_width=True)

    # ---------------------------
    # 3️⃣ Sector-wise Performance
    # ---------------------------
    st.subheader("3️⃣ Sector-wise Performance")

    sector_perf = (
        df_year.groupby('sector')['daily_return']
        .mean()
        .reset_index(name='Average Yearly Return')
    )

    fig_sector = px.bar(
        sector_perf,
        x='sector',
        y='Average Yearly Return',
        title="Average Yearly Return by Sector"
    )

    st.plotly_chart(fig_sector, use_container_width=True)

    # ---------------------------
    # 4️⃣ Stock Correlation
    # ---------------------------
    st.subheader("4️⃣ Stock Price Correlation")

    pivot_price = df_year.pivot_table(
        index='date',
        columns='Ticker',
        values='close'
    )

    corr_matrix = pivot_price.corr()

    fig_corr = px.imshow(
        corr_matrix,
        color_continuous_scale='RdBu',
        title="Stock Price Correlation Heatmap",
        aspect="auto"
    )

    fig_corr.update_layout(
        height=900,
        width=1200,
        xaxis_title="Ticker",
        yaxis_title="Ticker"
    )

    st.plotly_chart(fig_corr, use_container_width=True)

# =================================================
# TAB 2: TOP 5 GAINERS & LOSERS (Q5)
# =================================================
with tab2:

    st.subheader("🔥 Monthly Top 5 Gainers & Losers")

    monthly_return = (
        df.sort_values('date')
        .groupby(['year', 'month', 'Ticker'])
        .agg(
            first_close=('close', 'first'),
            last_close=('close', 'last')
        )
        .reset_index()
    )

    monthly_return['monthly_return_%'] = (
        (monthly_return['last_close'] - monthly_return['first_close'])
        / monthly_return['first_close'] * 100
    )

    months_list = (
        monthly_return[['year', 'month']]
        .drop_duplicates()
        .sort_values(['year', 'month'])
        .values.tolist()
    )

    cols = 3
    rows = math.ceil(len(months_list) / cols)

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[f"{mon} {yr}" for yr, mon in months_list]
    )

    row, col = 1, 1

    for yr, mon in months_list:

        data = monthly_return[
            (monthly_return['year'] == yr) &
            (monthly_return['month'] == mon)
        ]

        top_gainers = data.sort_values(
            'monthly_return_%', ascending=False
        ).head(5)

        top_losers = data.sort_values(
            'monthly_return_%'
        ).head(5)

        # 🟢 Gainers
        fig.add_trace(
            go.Bar(
                x=top_gainers['Ticker'],
                y=top_gainers['monthly_return_%'],
                text=top_gainers['monthly_return_%'].round(2),
                textposition='outside',
                marker_color='green'
            ),
            row=row,
            col=col
        )

        # 🔴 Losers
        fig.add_trace(
            go.Bar(
                x=top_losers['Ticker'],
                y=top_losers['monthly_return_%'],
                text=top_losers['monthly_return_%'].round(2),
                textposition='outside',
                marker_color='red'
            ),
            row=row,
            col=col
        )

        col += 1
        if col > cols:
            col = 1
            row += 1

    fig.update_layout(
        title="Top 5 Gainers and Losers by Month (All Years)",
        height=350 * rows,
        showlegend=False,
        barmode='group'
    )

    fig.add_hline(y=0, line_dash="dash", line_color="black")

    st.plotly_chart(fig, use_container_width=True)

# =================================================
# TAB 3: RAW DATA
# =================================================
with tab3:

    st.subheader("📄 Raw Stock Data")

    st.dataframe(df)

    st.download_button(
        "⬇️ Download CSV",
        data=df.to_csv(index=False),
        file_name="stock_data.csv"
    )
