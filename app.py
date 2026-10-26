
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Web2Insights",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Web2Insights")
st.subheader("Stock Market Data Dashboard")
st.write("Explore historical stock prices and download your data.")

# Locate the Excel file in the project folder
file_path = Path(__file__).parent / "AAPL_stock_data.xlsx"

if not file_path.exists():
    st.error("Stock data file not found. Run extractor.py first.")
    st.stop()

df = pd.read_excel(file_path)

if df.empty:
    st.warning("The stock data file is empty.")
    st.stop()

# Clean column names
df.columns = [str(col).strip().lower() for col in df.columns]

if "date" not in df.columns or "close" not in df.columns:
    st.error("The Excel file must contain Date and Close columns.")
    st.stop()

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["close"] = pd.to_numeric(df["close"], errors="coerce")
df = df.dropna(subset=["date", "close"]).sort_values("date")

if df.empty:
    st.warning("No valid stock prices were found.")
    st.stop()

# Dashboard filters
min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = df[
        (df["date"].dt.date >= start_date) &
        (df["date"].dt.date <= end_date)
    ]
else:
    filtered = df.copy()

if filtered.empty:
    st.warning("No stock records in this date range.")
    st.stop()

# Summary metrics
latest = filtered.iloc[-1]
previous = filtered.iloc[-2] if len(filtered) > 1 else latest

change = float(latest["close"] - previous["close"])

col1, col2, col3 = st.columns(3)

col1.metric(
    "Latest Closing Price",
    f"${latest['close']:,.2f}",
    f"{change:+.2f}"
)

col2.metric("Records Displayed", len(filtered))

col3.metric(
    "Latest Date",
    latest["date"].strftime("%Y-%m-%d")
)

# Interactive chart
st.subheader("Closing Price Trend")

fig = px.line(
    filtered,
    x="date",
    y="close",
    markers=True,
    labels={
        "date": "Date",
        "close": "Closing Price (USD)"
    },
    title="AAPL Historical Closing Prices"
)

st.plotly_chart(fig, use_container_width=True)

# Data table
st.subheader("Extracted Stock Data")
st.dataframe(filtered, use_container_width=True)


# Excel download
from io import BytesIO

excel_buffer = BytesIO()
filtered.to_excel(excel_buffer, index=False, engine="openpyxl")

st.download_button(
    label="Download Filtered Data as Excel",
    data=excel_buffer.getvalue(),
    file_name="AAPL_stock_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
