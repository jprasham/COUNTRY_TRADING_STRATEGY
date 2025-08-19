import pandas as pd
import streamlit as st
from typing import Optional

# Set Streamlit page configuration
st.set_page_config(page_title='COUNTRY TRADING STRATEGY', page_icon=':bar_chart:', layout = "wide")

# Display header for the dashboard
st.header('COUNTRY TRADING STRATEGY')

# Display the last update date
st.markdown('#### Updated: 19/08/2025')

excel_file = 'COUNTRY_TRADING_STRATEGY.xlsx'
sheet_name1 = 'FILTER1'
sheet_name2 = 'FILTER2'
use_cols = "A:I"                          
header_row = 0                            

# ---------- Helpers ----------
@st.cache_data
def load_excel_data(file_name: str,
                    sheet: str,
                    use_columns: str,
                    header_row: int,
                    nrows: Optional[int] = None) -> pd.DataFrame:
    """Loads Excel range and returns a DataFrame. nrows=None => all rows (dynamic)."""
    return pd.read_excel(
        file_name,
        sheet_name=sheet,
        usecols=use_columns,
        header=header_row,
        nrows=nrows
    )

def coerce_percent(col: pd.Series) -> pd.Series:
    """Accepts values like 0.099 or '9.9%' and returns float (0–1)."""
    if pd.api.types.is_numeric_dtype(col):
        # already fraction like 0.099
        return col
    # strings such as '9.9%' or ' 9.9 %'
    cleaned = (
        col.astype(str)
           .str.strip()
           .str.replace('%', '', regex=False)
           .str.replace(',', '', regex=False)
    )
    return pd.to_numeric(cleaned, errors='coerce') / 100.0

# ---------- Load & Clean ----------
# ---------- Load & Clean ----------
df = load_excel_data(excel_file, sheet_name1, use_cols, header_row, nrows=None)

# If your sheet header names already match, this will be a no-op.
expected = ["ETF", "COUNTRY", "CATEGORY",
            "CURRENT_RETURNS", "MEAN", "STD_DEV", "2_SIGMA",
            "CURRENT_PRICE", "200 DMA"]
df.columns = expected[:len(df.columns)]  # keep safe if fewer cols returned
# Reorder if the sheet contains them in any order
df = df[[c for c in expected if c in df.columns]]

# --- helpers ---
def coerce_percent(s):
    # turns "9.3%", " 9.3 %", 0.093 -> 0.093 as float
    return (s.astype(str)
             .str.replace('%', '', regex=False)
             .str.replace(',', '', regex=False)
             .str.strip()
             .replace({'': None})
             .astype(float)) / 100.0

def coerce_num(s):
    # turns "80.3", "80,3", " 80.3 " -> 80.3 as float
    return (s.astype(str)
             .str.replace(',', '', regex=False)
             .str.strip()
             .replace({'': None})
             .astype(float))

# Coerce percentage & numeric columns
pct_cols = [c for c in ["CURRENT_RETURNS", "MEAN", "STD_DEV", "2_SIGMA"] if c in df.columns]
num_cols = [c for c in ["CURRENT_PRICE", "200 DMA"] if c in df.columns]

for c in pct_cols:
    df[c] = coerce_percent(df[c])

for c in num_cols:
    df[c] = coerce_num(df[c])

# ---------- Display (styled like the screenshot) ----------
styler = (
    df.style
      .format(
          {**{c: "{:.1%}" for c in pct_cols},   # 1 decimal place for %
           **{c: "{:.1f}" for c in num_cols}}   # 1 decimal place for numbers
          , na_rep="-"
      )
      .set_properties(subset=["ETF"], **{"font-weight": "bold"})
      .hide(axis="index")
)

st.subheader("Countries above 2 Sigma")
st.table(styler)


# ---------- Load & Clean ----------
df = load_excel_data(excel_file, sheet_name2, use_cols, header_row, nrows=None)

# If your sheet header names already match, this will be a no-op.
expected = ["ETF", "COUNTRY", "CATEGORY",
            "CURRENT_RETURNS", "MEAN", "STD_DEV", "2_SIGMA",
            "CURRENT_PRICE", "200 DMA"]
df.columns = expected[:len(df.columns)]  # keep safe if fewer cols returned
# Reorder if the sheet contains them in any order
df = df[[c for c in expected if c in df.columns]]

# --- helpers ---
def coerce_percent(s):
    # turns "9.3%", " 9.3 %", 0.093 -> 0.093 as float
    return (s.astype(str)
             .str.replace('%', '', regex=False)
             .str.replace(',', '', regex=False)
             .str.strip()
             .replace({'': None})
             .astype(float)) / 100.0

def coerce_num(s):
    # turns "80.3", "80,3", " 80.3 " -> 80.3 as float
    return (s.astype(str)
             .str.replace(',', '', regex=False)
             .str.strip()
             .replace({'': None})
             .astype(float))

# Coerce percentage & numeric columns
pct_cols = [c for c in ["CURRENT_RETURNS", "MEAN", "STD_DEV", "2_SIGMA"] if c in df.columns]
num_cols = [c for c in ["CURRENT_PRICE", "200 DMA"] if c in df.columns]

for c in pct_cols:
    df[c] = coerce_percent(df[c])

for c in num_cols:
    df[c] = coerce_num(df[c])

# ---------- Display (styled like the screenshot) ----------
styler = (
    df.style
      .format(
          {**{c: "{:.1%}" for c in pct_cols},   # 1 decimal place for %
           **{c: "{:.1f}" for c in num_cols}}   # 1 decimal place for numbers
          , na_rep="-"
      )
      .set_properties(subset=["ETF"], **{"font-weight": "bold"})
      .hide(axis="index")
)

st.subheader("Countries below 2 Sigma")
st.table(styler)



