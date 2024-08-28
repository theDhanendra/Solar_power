import streamlit as st
import pandas as pd

# Set title
st.title("Solar Power Analysis")

# Display a simple message
st.write("Welcome to the Solar Power Analysis App")

# Example of displaying a DataFrame
data = {
    'Region': ['North', 'South', 'East', 'West'],
    'Power Generation (MW)': [120, 340, 200, 150]
}
df = pd.DataFrame(data)
st.write(df)
