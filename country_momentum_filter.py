import pandas as pd
import streamlit as st
from typing import Optional

# Set Streamlit page configuration
st.set_page_config(page_title='COUNTRY MOMENTUM FILTER', page_icon=':bar_chart:', layout = "wide")

# Display header for the dashboard
st.header('COUNTRY MOMENTUM FILTER')

# Display the last update date
st.markdown('#### Updated: 18/08/2025')

excel_file = 'COUNTRY_MOMENTUM_FILTER.xlsx'
sheet_name1 = 'FILTER'
use_cols = "A:F"                          
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
df = load_excel_data(excel_file, sheet_name, use_cols, header_row, nrows=None)

# Ensure exact column order (rename if your sheet uses spaces/variants)
expected = ["ETF", "COUNTRY", "CATEGORY", "CURRENT_MEAN", "STD_DEV", "2_SIGMA"]
df.columns = expected  # if your headers already match, this is a no-op

# Coerce percentage columns
pct_cols = ["CURRENT_MEAN", "STD_DEV", "2_SIGMA"]
for c in pct_cols:
    if c in df.columns:
        df[c] = coerce_percent(df[c])

# ---------- Display (styled like the screenshot) ----------
# Use pandas Styler for bold ETF and percentage formatting
styler = (
    df.style
      .format({c: "{:.1%}" for c in pct_cols}, na_rep="-")
      .set_properties(subset=["ETF"], **{"font-weight": "bold"})
      .hide(axis="index")
)


st.table(styler)




