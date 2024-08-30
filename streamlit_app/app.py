import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import base64
import io

# Upload logo
def load_logo(image_path):                   
    icon = Image.open(image_path)
    icon = icon.resize((100, 100)) 
    buffered = io.BytesIO()
    icon.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

img_str = load_logo('../images/logo.jpeg')
 
# Adjustment of header 
st.markdown(
    f"""
    <style>
    .header {{                             /*Used for top header*/
        width: 100%;
        background-color: #FFFFFF;  
        padding: 10px;
        display: flex;
        align-items: center;
        position: fixed;
        top: 0;
        border-bottom: 2px solid #FFFFFF;
        z-index: 1000;
    }}
    .header-title {{                              /*Used for Title Name*/
        font-size: 35px;
        font-weight: bold;
        color: #333333;
        flex: 0.5;  
        text-align: center;
        margin-top: 40px;
    }}
    .header-logo {{                               /* logo position and alignment*/
        height: 100px; 
        display: flex;
        align-items: center;
        margin-left: 250px; 
        margin-top: 40px;
    }}
    .header-logo img {{                           /*logo size*/
        height: 100%; 
        width: auto;
    }}
    </style>
    <div class="header">
        <div class="header-title">Solar Power Analysis</div>
        <div class="header-logo">
            <img src="data:image/png;base64,{img_str}" alt="Logo">
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Adjust the sidebar width
st.markdown(
    """
    <style>
    /* Adjust the width of the sidebar */
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 320px;  /* Set your desired width here */
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        margin-left: -100px;  /* Set your desired width here */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv('cleaned_data.csv')

df = load_data()


# Navigation Section
option_dict = {
    'plant 1': ['Summary Statistics',
                'AC and DC Power by day',
                'Ambient and Module Temperature by Day', 
                'Power Output for Selected Day',
                'Power Output Over Time',
                'Peak Power Production Hours'],

    'plant 2': ['Summary Statistics of AC and DC Power',
                'Correlation between Ambient and Module Temperature',
                'Power Production by Hour',
                'Temperature Distribution',
                'Temperature Relationship',
                'Peak Power Production Hours']
}

st.sidebar.title("Navigation")
select_option = st.sidebar.selectbox("Select a Plant:", option_dict.keys())
buttons = option_dict[select_option]

unique_key = f"radio_{select_option}"
selected_button = st.sidebar.radio('Select an insight', buttons, key=unique_key)

# Filter Options
st.sidebar.subheader("Filter Options")

# Filter by day
day_filter = st.sidebar.multiselect(
    "Select Days:",
    options=df['DAY'].unique(),
    default=df['DAY'].unique()[:0]  # Select the first 5 days by default
)

# Filter by module temperature
temp_range = st.sidebar.slider(
    "Select Module Temperature Range:",
    min_value=float(df['MODULE_TEMPERATURE'].min()),
    max_value=float(df['MODULE_TEMPERATURE'].max()),
    value=(float(df['MODULE_TEMPERATURE'].min()), float(df['MODULE_TEMPERATURE'].max()))
)

# Apply filters to the dataframe
filtered_df = df[(df['DAY'].isin(day_filter)) & 
                 (df['MODULE_TEMPERATURE'] >= temp_range[0]) & 
                 (df['MODULE_TEMPERATURE'] <= temp_range[1])]



# Display different insights based on button selection
st.header(" ")
if selected_button == 'Summary Statistics':
    st.header("Summary Statistics")
    st.write(df.describe())

elif selected_button == 'AC and DC Power by day':
    st.header("AC and DC Power by Day")
    AC_prod = df[["AC_POWER", "DAY"]].groupby("DAY").mean().reset_index()
    DC_prod = df[["DC_POWER", "DAY"]].groupby("DAY").mean().reset_index()
    plt.figure(figsize=(18, 9))
    sns.lineplot(x='DAY', y='AC_POWER', data=AC_prod, marker='o', label='AC Power')
    sns.lineplot(x='DAY', y='DC_POWER', data=DC_prod, marker='o', label='DC Power')
    plt.title('Sum of AC and DC Power by Day')
    plt.xlabel('Day')
    plt.ylabel('Power')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

elif selected_button == 'Ambient and Module Temperature by Day':
    st.header("Ambient and Module Temperature by Day")
    Ambtemp_day = df[['AMBIENT_TEMPERATURE', 'DAY']].groupby('DAY').mean().reset_index()
    Modtemp_day = df[['MODULE_TEMPERATURE', 'DAY']].groupby('DAY').mean().reset_index()
    plt.figure(figsize=(14, 7))
    sns.lineplot(x='DAY', y='AMBIENT_TEMPERATURE', data=Ambtemp_day, marker='o', label='Ambient Temperature')
    sns.lineplot(x='DAY', y='MODULE_TEMPERATURE', data=Modtemp_day, marker='o', label='Module Temperature')
    plt.title('Ambient and Module Temperature by Day')
    plt.xlabel('Day')
    plt.ylabel('Temperature')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

elif selected_button == 'Power Output for Selected Day':
    st.header("Power Output for Selected Day")
    selected_day = st.selectbox('Select Day', sorted(df['DAY'].unique()))
    filtered_data = df[df['DAY'] == selected_day]
    st.write(f"Data for Day {selected_day}")
    st.write(filtered_data)
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=filtered_data, x='TIME', y='AC_POWER', label='AC Power')
    sns.lineplot(data=filtered_data, x='TIME', y='DC_POWER', label='DC Power')
    plt.title(f"Power Output on Day {selected_day}")
    plt.xlabel("Time")
    plt.ylabel("Power")
    plt.grid(True)
    st.pyplot(plt)

elif selected_button == 'Power Output Over Time':
    st.header("Power Output Over Time")
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df, x='TIME', y='AC_POWER', label='AC Power')
    sns.lineplot(data=df, x='TIME', y='DC_POWER', label='DC Power')
    plt.title('Power Output Over Time')
    plt.xlabel('Time')
    plt.ylabel('Power')
    plt.grid(True)
    st.pyplot(plt)

elif selected_button == 'Summary Statistics of AC and DC Power':
    st.header("Summary Statistics of AC and DC Power")
    st.write(df[['AC_POWER', 'DC_POWER']].describe())

elif selected_button == 'Correlation between Ambient and Module Temperature':
    st.header("Correlation between Ambient and Module Temperature")
    plt.figure(figsize=(10, 5))
    sns.scatterplot(data=df, x='AMBIENT_TEMPERATURE', y='MODULE_TEMPERATURE')
    plt.title('Ambient Temperature vs Module Temperature')
    plt.xlabel('Ambient Temperature')
    plt.ylabel('Module Temperature')
    plt.grid(True)
    st.pyplot(plt)

elif selected_button == 'Power Production by Hour':
    st.header("Power Production by Hour")
    df['HOUR'] = pd.to_datetime(df['TIME']).dt.hour
    hourly_power = df.groupby('HOUR')[['AC_POWER', 'DC_POWER']].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=hourly_power, x='HOUR', y='AC_POWER', label='AC Power')
    sns.lineplot(data=hourly_power, x='HOUR', y='DC_POWER', label='DC Power')
    plt.title('Average Power Production by Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Power')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

elif selected_button == 'Temperature Distribution':
    st.header("Temperature Distribution")
    plt.figure(figsize=(10, 5))
    sns.histplot(df['MODULE_TEMPERATURE'], kde=True)
    plt.title('Distribution of Module Temperature')
    plt.xlabel('Module Temperature')
    plt.ylabel('Frequency')
    st.pyplot(plt)

elif selected_button == 'Temperature Relationship':
    st.header("Relationship Between Ambient and Module Temperature")
    plt.figure(figsize=(10, 5))
    sns.scatterplot(data=df, x='AMBIENT_TEMPERATURE', y='MODULE_TEMPERATURE')
    plt.title('Ambient vs Module Temperature')
    plt.xlabel('Ambient Temperature')
    plt.ylabel('Module Temperature')
    plt.grid(True)
    st.pyplot(plt)

elif selected_button == 'Power Output Comparison Betwenn Plants':
    st.header("Power Output Comparison Between Plants")
    avg_ac_power = df.groupby('PLANT_ID')['AC_POWER'].mean().reset_index()
    avg_dc_power = df.groupby('PLANT_ID')['DC_POWER'].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(x='PLANT_ID', y='AC_POWER', data=avg_ac_power, label='AC Power')
    sns.barplot(x='PLANT_ID', y='DC_POWER', data=avg_dc_power, label='DC Power')
    plt.title('Average Power Output Comparison')
    plt.xlabel('Plant ID')
    plt.ylabel('Average Power')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

elif selected_button == 'Peak Power Production Hours':
    st.header("Peak Power Production Hours")
    df['HOUR'] = pd.to_datetime(df['TIME']).dt.hour
    hourly_avg_power = df.groupby('HOUR')[['AC_POWER', 'DC_POWER']].mean().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=hourly_avg_power, x='HOUR', y='AC_POWER', label='AC Power')
    sns.lineplot(data=hourly_avg_power, x='HOUR', y='DC_POWER', label='DC Power')
    plt.title('Average Power Production by Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Power')
    plt.axvline(hourly_avg_power['AC_POWER'].idxmax(), color='r', linestyle='--', label='Peak AC Power Hour')
    plt.axvline(hourly_avg_power['DC_POWER'].idxmax(), color='g', linestyle='--', label='Peak DC Power Hour')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)


