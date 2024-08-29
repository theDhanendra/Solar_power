#!/usr/bin/env python
# coding: utf-8

# # Importing libraries

# In[2]:


import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 


# # Planting 1 data

# In[3]:


df_p1 = pd.read_csv("../data/Plant_1_Generation_Data.csv")
df_p1


# In[4]:


df1_p1 = pd.read_csv("../data/Plant_1_Weather_Sensor_Data.csv")
df1_p1


# # Checking for duplicates in plant 1

# In[5]:


df_p1.duplicated().sum()


# # Checking for null values in plant 1

# In[6]:


df_p1.isnull().sum()


# # Getting information of plant 1

# In[7]:


df_p1.info()


# # Adding "00" to the generation data set so that the both data sets have same format

# In[8]:


df_p1['DATE_TIME'] = pd.to_datetime(df_p1['DATE_TIME'], format='mixed').dt.strftime('%Y-%m-%d %H:%M:%S')
df_p1


# # Plant 1  Merging both the datasets  

# In[9]:


df_p1_solar = pd.merge(df_p1.drop(columns = ['PLANT_ID']), df1_p1.drop(columns = ['PLANT_ID', 'SOURCE_KEY']), on='DATE_TIME')
df_p1_solar


# # Plant1 merged data information  

# In[12]:


df_p1_solar.info()


# # checking the null values in merged data plant 1

# In[13]:


df_p1_solar.isnull().sum()


# # creating the data and time colums in PLANT 1

# In[14]:


df_p1_solar['DATE_TIME'] = pd.to_datetime(df_p1_solar['DATE_TIME'])
df_p1_solar['DATE'] = df_p1_solar['DATE_TIME'].dt.date
df_p1_solar['TIME'] = df_p1_solar['DATE_TIME'].dt.time
df_p1_solar['DAY'] = df_p1_solar['DATE_TIME'].dt.day


# In[15]:


df_p1_solar['YEAR_MONTH'] = df_p1_solar['DATE_TIME'].dt.to_period('M')
df_p1_solar


# # Grouping plant 1 data based on the time

# In[16]:


def categorize_time_of_day(time):
    if time >= pd.to_datetime('00:00:00').time() and time < pd.to_datetime('06:00:00').time():
        return 'Night'
    elif time >= pd.to_datetime('06:00:00').time() and time < pd.to_datetime('12:00:00').time():
        return 'Morning'
    elif time >= pd.to_datetime('12:00:00').time() and time < pd.to_datetime('18:00:00').time():
        return 'Afternoon'
    else:
        return 'Evening'
df_p1_solar['TIME_OF_DAY'] = df_p1_solar['TIME'].apply(categorize_time_of_day)


# In[17]:


df_p1_solar


# # Plant 1 AC and DC production based on day

# In[45]:


AC_prod = df_p1_solar[["AC_POWER", "DAY"]].groupby("DAY").mean().reset_index()
DC_prod = df_p1_solar[["DC_POWER", "DAY"]].groupby("DAY").mean().reset_index()


# In[46]:


plt.figure(figsize=(14, 7))
sns.lineplot(x='DAY', y='AC_POWER', data=AC_prod, marker='o',label='AC Power Sum')
sns.lineplot(x='DAY', y="DC_POWER", data=DC_prod, marker='o', label='DC Power Sum')
plt.title('Sum of AC and DC Power by Day')
plt.xlabel('Day')
plt.ylabel('Power')
plt.legend()
plt.grid(True)
plt.show()


# # Cheking why we have more production on 21st rather than other days for plant1 

# In[47]:


Ambtemp_day = df_p1_solar[['AMBIENT_TEMPERATURE', "DAY"]].groupby("DAY").mean().reset_index()
Modtemp_day = df_p1_solar[["MODULE_TEMPERATURE", "DAY"]].groupby("DAY").mean().reset_index()


# In[48]:


plt.figure(figsize=(14, 7))
sns.lineplot(x='DAY', y='AMBIENT_TEMPERATURE', data=Ambtemp_day, marker='o',label='Ambtemp_day')
sns.lineplot(x='DAY', y="MODULE_TEMPERATURE", data=Modtemp_day, marker='o', label='Modtemp_day')
plt.title('Ambient temperature and module temperature for each day')
plt.xlabel('Day')
plt.ylabel('Temperature')
plt.legend()
plt.grid(True)
plt.show()


# # Histplot for the AC and DC production

# In[49]:


df_p1_solar['TIME'] = pd.to_datetime(df_p1_solar['TIME'], format='%H:%M:%S')

# Option 2: Convert the time to the number of minutes since midnight (for plotting)
df_p1_solar['TIME_HOURS'] = (df_p1_solar['TIME'].dt.hour + df_p1_solar['TIME'].dt.minute) / 60

# Find the peak DC Power
peak_dc_power = df_p1_solar[df_p1_solar['DC_POWER'] == df_p1_solar['DC_POWER'].max()]

# Find the peak AC Power
peak_ac_power = df_p1_solar[df_p1_solar['AC_POWER'] == df_p1_solar['AC_POWER'].max()]

# Plot histograms of DC Power and AC Power
plt.figure(figsize=(14, 6))

# Histogram for DC Power
plt.subplot(1, 2, 1)
plt.hist(df_p1_solar['DC_POWER'], bins=30, color='blue', edgecolor='black')
plt.title('Histogram of DC Power')
plt.xlabel('DC Power (W)')
plt.ylabel('Frequency')

# Histogram for AC Power
plt.subplot(1, 2, 2)
plt.hist(df_p1_solar['AC_POWER'], bins=30, color='orange', edgecolor='black')
plt.title('Histogram of AC Power')
plt.xlabel('AC Power (W)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()


# # Scatter plot of AC and DC production plant 1

# In[50]:


sns.scatterplot(data=df_p1_solar,x='AC_POWER',y='DC_POWER')


# # Correlation between AC and DC 

# In[51]:


correlation_matrix = df_p1_solar[['AC_POWER', 'DC_POWER']].corr()
sns.heatmap(correlation_matrix, annot=True, fmt='.2f',cmap="coolwarm",linewidths=0.5)
plt.show()


# # Scatter plot of Amb temp and module temp

# In[52]:


sns.scatterplot(data=df_p1_solar,x='AMBIENT_TEMPERATURE',y='MODULE_TEMPERATURE')


# # Correlation between Irredation, Amb temp and module temp Plant1

# In[53]:


correlation_matrix = df_p1_solar[['IRRADIATION', 'MODULE_TEMPERATURE','AMBIENT_TEMPERATURE']].corr()
sns.heatmap(correlation_matrix, annot=True, fmt='.2f',cmap="coolwarm",linewidths=0.5)
plt.show()


# # Total yeild based on the source key plant 1

# In[54]:


df_p1_solar['SOURCE_KEY'].nunique()


# In[55]:


plt.figure(figsize=(10,6))
plt.xticks(rotation=90)
plt.title("Source key and it's total yeild")
Source_totalyield = df_p1_solar[['SOURCE_KEY', 'TOTAL_YIELD']].groupby('SOURCE_KEY').sum().reset_index()
sns.barplot(data=Source_totalyield, x='SOURCE_KEY', y='TOTAL_YIELD')


# # Time of the day and total AC and DC power Plant1

# In[56]:


Timeofday_AC = df_p1_solar[['TIME_OF_DAY', 'AC_POWER']].groupby('TIME_OF_DAY').mean().reset_index()
Timeofday_DC = df_p1_solar[['TIME_OF_DAY', 'DC_POWER']].groupby('TIME_OF_DAY').mean().reset_index()
Timeofday = Timeofday_AC.merge(Timeofday_DC, on='TIME_OF_DAY', suffixes=('_AC', '_DC'))
melted_df = Timeofday.melt(id_vars='TIME_OF_DAY', value_vars=['AC_POWER', 'DC_POWER'], 
                              var_name='Power Type', value_name='Power Produced')
plt.figure(figsize=(10, 6))
sns.barplot(data=melted_df, x='TIME_OF_DAY', y='Power Produced', hue='Power Type')
plt.title("Time of the Day vs. AC and DC Produced")
plt.xlabel("Time of Day")
plt.ylabel("Power Produced")
plt.show()


# # Time of day and Ambient temperature and module temperature Plant 1

# In[57]:


Timeofday_AT = df_p1_solar[['TIME_OF_DAY', 'AMBIENT_TEMPERATURE']].groupby('TIME_OF_DAY').mean().reset_index()
Timeofday_MT = df_p1_solar[['TIME_OF_DAY', 'MODULE_TEMPERATURE']].groupby('TIME_OF_DAY').mean().reset_index()
Timeofday_temp = Timeofday_AT.merge(Timeofday_MT, on='TIME_OF_DAY', suffixes=('_Ambient', '_Module'))
melted_temp_df = Timeofday_temp.melt(id_vars='TIME_OF_DAY', value_vars=['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE'],
                                     var_name='Temperature Type', value_name='Temperature')

plt.figure(figsize=(10, 6))

# Plot using seaborn barplot with 'hue' for grouped bars
sns.barplot(data=melted_temp_df, x='TIME_OF_DAY', y='Temperature', hue='Temperature Type')

# Add title and labels
plt.title("Time of the Day vs. Ambient and Module Temperature")
plt.xlabel("Time of Day")
plt.ylabel("Temperature (°C)")

# Display the plot
plt.show()


# # Daily total yeild plant 1

# In[122]:


plt.figure(figsize=(10, 6))
plt.title("Daily total yeild plant 1")
Cummilative_daily_yeild = df_p1_solar[["DAY", "DAILY_YIELD"]].groupby("DAY").mean().reset_index()
sns.lineplot(x="DAY", y='DAILY_YIELD', data=Cummilative_daily_yeild, marker='o', color='blue')


# # Effects of Irradiation on Ambient and Module Temperature plant1

# In[117]:


df_p1_solar['IRRADIATION_CATEGORY'] = pd.cut(df_p1_solar['IRRADIATION'], bins=[-float('inf'), 0.5, 0.8, float('inf')], labels=['Low', 'Medium', 'High'])

# Prepare the data for plotting
temperature_vs_irradiation_melted = df_p1_solar.melt(id_vars='IRRADIATION_CATEGORY', value_vars=['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE'], 
                                                     var_name='Temperature_Type', value_name='Temperature')

# Create the plot
plt.figure(figsize=(14, 7))
sns.barplot(x='IRRADIATION_CATEGORY', y='Temperature', hue='Temperature_Type', data=temperature_vs_irradiation_melted)

# Set plot titles and labels
plt.title('Effects of Irradiation on Ambient and Module Temperature')
plt.xlabel('Irradiation Category')
plt.ylabel('Temperature (°C)')
plt.legend(title='Temperature Type')
plt.show()


# # Irradiation VS Power output in AC and DC plant 1

# In[131]:


df_p1_solar['IRRADIATION_CATEGORY'] = pd.cut(df_p1_solar['IRRADIATION'], bins=[-float('inf'), 0.5, 0.8, float('inf')], labels=['Low', 'Medium', 'High'])
irradiation_vs_power = df_p1_solar.groupby('IRRADIATION_CATEGORY')[['DC_POWER', 'AC_POWER']].mean().reset_index()
irradiation_vs_power_melted = irradiation_vs_power.melt(id_vars='IRRADIATION_CATEGORY', var_name='Power_Type', value_name='Power')
plt.figure(figsize=(14, 7))
sns.barplot(x='IRRADIATION_CATEGORY', y='Power', hue='Power_Type', data=irradiation_vs_power_melted)
plt.title('Irradiation vs. Power Output')
plt.xlabel('Irradiation Category')
plt.ylabel('Power (kW)')
plt.legend(title='Power Type')
plt.show()


# # Plotting Ambient Temperature vs. Power Output (DC_POWER and AC_POWER) plant 1

# In[130]:


df_p1_solar['AMBIENT_TEMPERATURE_CATEGORY'] = pd.cut(
    df_p1_solar['AMBIENT_TEMPERATURE'],
    bins=[-float('inf'), 20, 30, float('inf')],
    labels=['Low', 'Medium', 'High']
)
ambient_temp_vs_power = df_p1_solar.groupby('AMBIENT_TEMPERATURE_CATEGORY')[['DC_POWER', 'AC_POWER']].mean().reset_index()
temperature_vs_power_melted = ambient_temp_vs_power.melt(id_vars='AMBIENT_TEMPERATURE_CATEGORY', var_name='Power_Type', value_name='Power')
plt.figure(figsize=(10, 6))
sns.barplot(x='AMBIENT_TEMPERATURE_CATEGORY', y='Power', hue='Power_Type', data=temperature_vs_power_melted)
plt.title('Ambient Temperature vs. Power Output')
plt.xlabel('Ambient Temperature Category')
plt.ylabel('Power (kW)')
plt.legend(title='Power Type')
plt.show()


# # Plotting Module Temperature vs. Power Output (DC_POWER and AC_POWER) plant 1

# In[129]:


df_p1_solar['MODULE_TEMPERATURE_CATEGORY'] = pd.cut(
    df_p1_solar['MODULE_TEMPERATURE'],
    bins=[-float('inf'), 30, 45, float('inf')],
    labels=['Low', 'Medium', 'High']
)
module_temp_vs_power = df_p1_solar.groupby('MODULE_TEMPERATURE_CATEGORY')[['DC_POWER', 'AC_POWER']].mean().reset_index()
module_temp_vs_power_melted = module_temp_vs_power.melt(id_vars='MODULE_TEMPERATURE_CATEGORY', var_name='Power_Type', value_name='Power')
plt.figure(figsize=(14, 7))
sns.barplot(x='MODULE_TEMPERATURE_CATEGORY', y='Power', hue='Power_Type', data=module_temp_vs_power_melted)
plt.title('Module Temperature vs. Power Output')
plt.xlabel('Module Temperature Category')
plt.ylabel('Power (kW)')
plt.legend(title='Power Type')
plt.show()


# In[ ]:





# In[ ]:





# # Plant 2 Data

# In[59]:


df = pd.read_csv("../data/Plant_2_Generation_Data.csv")
df


# In[60]:


df2 = pd.read_csv("../data/Plant_2_Weather_Sensor_Data.csv")
df2


# # cheking null values in plant 2

# In[61]:


df2.isnull().sum()


# # checking duplicates in plant 2

# In[62]:


df2.duplicated().sum()


# # printing information of plant 2

# In[63]:


df2.info()


# # checking for ducplicates in plant 2

# In[38]:


df.duplicated().sum()


# # Merging data sets of plant 2

# In[39]:


merged_df = pd.merge(df.drop(columns = ['PLANT_ID']), df2.drop(columns = ['PLANT_ID', 'SOURCE_KEY']),on='DATE_TIME')
merged_df


# # Checking duplicates in merged plant 2

# In[40]:


merged_df.duplicated().sum()


# # Checking null values in merged data

# In[41]:


merged_df.duplicated().sum()


# # Seperating date and time

# In[42]:


merged_df['DATE_TIME'] = pd.to_datetime(merged_df['DATE_TIME'])
merged_df['DATE'] = merged_df['DATE_TIME'].dt.date
merged_df['TIME'] = merged_df['DATE_TIME'].dt.time
merged_df['DAY'] = merged_df['DATE_TIME'].dt.day
merged_df


# # creating groups based on the time

# In[44]:


def categorize_time_of_day(time):
    if time >= pd.to_datetime('00:00:00').time() and time < pd.to_datetime('06:00:00').time():
        return 'Night'
    elif time >= pd.to_datetime('06:00:00').time() and time < pd.to_datetime('12:00:00').time():
        return 'Morning'
    elif time >= pd.to_datetime('12:00:00').time() and time < pd.to_datetime('18:00:00').time():
        return 'Afternoon'
    else:
        return 'Evening'
merged_df['TIME_OF_DAY'] = merged_df['TIME'].apply(categorize_time_of_day)


# In[43]:


merged_df


# # Power produced based on the Day plant 2

# In[38]:


AC_prod_p2 = merged_df[["AC_POWER", "DAY"]].groupby("DAY").mean().reset_index()
DC_prod_p2 = merged_df[["DC_POWER", "DAY"]].groupby("DAY").mean().reset_index()


# In[50]:


plt.figure(figsize=(14, 7))
sns.lineplot(x='DAY', y='AC_POWER', data=AC_prod_p2, marker='o',label='AC Power Sum')
sns.lineplot(x='DAY', y="DC_POWER", data=DC_prod_p2, marker='o', label='DC Power Sum')
plt.title('Sum of AC and DC Power by Day Plant2')
plt.xlabel('Day')
plt.ylabel('Power')
plt.legend()
plt.grid(True)
plt.show()


# # Checking the production peaked day temp plant 2

# In[47]:


Ambtemp_dayp2 = merged_df[['AMBIENT_TEMPERATURE', "DAY"]].groupby("DAY").mean().reset_index()
Modtemp_dayp2 = merged_df[["MODULE_TEMPERATURE", "DAY"]].groupby("DAY").mean().reset_index()


# In[49]:


plt.figure(figsize=(14, 7))
sns.lineplot(x='DAY', y='AMBIENT_TEMPERATURE', data=Ambtemp_dayp2, marker='o',label='Ambtemp_day')
sns.lineplot(x='DAY', y="MODULE_TEMPERATURE", data=Modtemp_dayp2, marker='o', label='Modtemp_day')
plt.title('Ambient temperature and module temperature for each day Plant2')
plt.xlabel('Day')
plt.ylabel('Temperature')
plt.legend()
plt.grid(True)
plt.show()


# # ploring histogram for the AC and DC production

# In[40]:


merged_df['TIME'] = pd.to_datetime(merged_df['TIME'], format='%H:%M:%S')

# Option 2: Convert the time to the number of minutes since midnight (for plotting)
merged_df['TIME_HOURS'] = (merged_df['TIME'].dt.hour + merged_df['TIME'].dt.minute) / 60

# Find the peak DC Power
peak_dc_power_p2 = merged_df[merged_df['DC_POWER'] == merged_df['DC_POWER'].max()]

# Find the peak AC Power
peak_ac_power_p2 = merged_df[merged_df['AC_POWER'] == merged_df['AC_POWER'].max()]

# Plot histograms of DC Power and AC Power
plt.figure(figsize=(14, 6))

# Histogram for DC Power
plt.subplot(1, 2, 1)
plt.hist(merged_df['DC_POWER'], bins=30, color='blue', edgecolor='black')
plt.title('Histogram of DC Power')
plt.xlabel('DC Power (W)')
plt.ylabel('Frequency')

# Histogram for AC Power
plt.subplot(1, 2, 2)
plt.hist(merged_df['AC_POWER'], bins=30, color='orange', edgecolor='black')
plt.title('Histogram of AC Power')
plt.xlabel('AC Power (W)')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()


# # Scatterplot of AC and DC plant2

# In[54]:


sns.scatterplot(data=merged_df,x='AC_POWER',y='DC_POWER')


# # ccorrelation between AC and DC plant 2

# In[71]:


correlation_matrixp2 = merged_df[['AC_POWER', 'DC_POWER']].corr()
sns.heatmap(correlation_matrixp2, annot=True, fmt='.2f',cmap="coolwarm",linewidths=0.5)
plt.show()


# # Scatter plot of Amb temp and module temp plant2

# In[56]:


sns.scatterplot(data=merged_df,x='AMBIENT_TEMPERATURE',y='MODULE_TEMPERATURE')


# # correlation between iirradiation and module temp and aambient_temperature

# In[70]:


correlation_matrixp2 = merged_df[['IRRADIATION', 'MODULE_TEMPERATURE','AMBIENT_TEMPERATURE']].corr()
sns.heatmap(correlation_matrixp2, annot=True, fmt='.2f',cmap="coolwarm",linewidths=0.5)
plt.show()


# # source key and its maximum yeild

# In[82]:


merged_df['SOURCE_KEY'].nunique()


# In[109]:


plt.figure(figsize=(10,6))
plt.xticks(rotation=90)
plt.title("Source key and it's total yeild")
Source_totalyieldp2 = merged_df[['SOURCE_KEY', 'TOTAL_YIELD']].groupby('SOURCE_KEY').sum().reset_index()
sns.barplot(data=Source_totalyieldp2, x='SOURCE_KEY', y='TOTAL_YIELD')


# # Time of the day and AC and DC produced

# In[118]:


Timeofday_ACp2 = merged_df[['TIME_OF_DAY', 'AC_POWER']].groupby('TIME_OF_DAY').mean().reset_index()
Timeofday_DCp2 = merged_df[['TIME_OF_DAY', 'DC_POWER']].groupby('TIME_OF_DAY').mean().reset_index()
Timeofday_p2 = Timeofday_ACp2.merge(Timeofday_DCp2, on='TIME_OF_DAY', suffixes=('_AC', '_DC'))
melted_df = Timeofday_p2.melt(id_vars='TIME_OF_DAY', value_vars=['AC_POWER', 'DC_POWER'], 
                              var_name='Power Type', value_name='Power Produced')
plt.figure(figsize=(10, 6))
sns.barplot(data=melted_df, x='TIME_OF_DAY', y='Power Produced', hue='Power Type')
plt.title("Time of the Day vs. AC and DC Produced")
plt.xlabel("Time of Day")
plt.ylabel("Power Produced")
plt.show()


# # Ambiemt temperatue and module temperature based on the time of day plant2

# In[64]:


Timeofday_ATp2 = merged_df[['TIME_OF_DAY', 'AMBIENT_TEMPERATURE']].groupby('TIME_OF_DAY').mean().reset_index()
Timeofday_MTp2 = merged_df[['TIME_OF_DAY', 'MODULE_TEMPERATURE']].groupby('TIME_OF_DAY').mean().reset_index()
Timeofday_tempp2 = Timeofday_ATp2.merge(Timeofday_MTp2, on='TIME_OF_DAY', suffixes=('_Ambient', '_Module'))
melted_temp_dfp2 = Timeofday_tempp2.melt(id_vars='TIME_OF_DAY', value_vars=['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE'],
                                     var_name='Temperature Type', value_name='Temperature')

plt.figure(figsize=(10, 6))

# Plot using seaborn barplot with 'hue' for grouped bars
sns.barplot(data=melted_temp_dfp2, x='TIME_OF_DAY', y='Temperature', hue='Temperature Type')

# Add title and labels
plt.title("Time of the Day vs. Ambient and Module Temperature")
plt.xlabel("Time of Day")
plt.ylabel("Temperature (°C)")

# Display the plot
plt.show()


# # Cummilative daily yeild of plant 2

# In[123]:


plt.figure(figsize=(10, 6))
plt.title("Daily total yeild plant 2")
Cummilative_daily_yeildp2 = merged_df[["DAY", "DAILY_YIELD"]].groupby("DAY").mean().reset_index()
sns.lineplot(x="DAY", y='DAILY_YIELD', data=Cummilative_daily_yeildp2, marker='o', color='blue')


# # Effect of irradiation on ambient temperature and module temperature plant 2

# In[124]:


merged_df['IRRADIATION_CATEGORY'] = pd.cut(merged_df['IRRADIATION'], bins=[-float('inf'), 0.5, 0.8, float('inf')], labels=['Low', 'Medium', 'High'])

# Prepare the data for plotting
temperature_vs_irradiation_meltedp2 = merged_df.melt(id_vars='IRRADIATION_CATEGORY', value_vars=['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE'], 
                                                     var_name='Temperature_Type', value_name='Temperature')

# Create the plot
plt.figure(figsize=(14, 7))
sns.barplot(x='IRRADIATION_CATEGORY', y='Temperature', hue='Temperature_Type', data=temperature_vs_irradiation_meltedp2)

# Set plot titles and labels
plt.title('Effects of Irradiation on Ambient and Module Temperature')
plt.xlabel('Irradiation Category')
plt.ylabel('Temperature (°C)')
plt.legend(title='Temperature Type')
plt.show()


# # Effect of irradiation on Power produced plant 2

# In[136]:


merged_df['IRRADIATION_CATEGORY'] = pd.cut(merged_df['IRRADIATION'], bins=[-float('inf'), 0.5, 0.8, float('inf')], labels=['Low', 'Medium', 'High'])
irradiation_vs_powerp2 = merged_df.groupby('IRRADIATION_CATEGORY')[['DC_POWER', 'AC_POWER']].mean().reset_index()
plt.figure(figsize=(14, 7))
irradiation_vs_power_meltedp2 = irradiation_vs_powerp2.melt(id_vars='IRRADIATION_CATEGORY', var_name='Power_Type', value_name='Power')
sns.barplot(x='IRRADIATION_CATEGORY', y='Power', hue='Power_Type', data=irradiation_vs_power_meltedp2)
plt.title('Irradiation vs. Power Output')
plt.xlabel('Irradiation Category')
plt.ylabel('Power (kW)')
plt.legend(title='Power Type')
plt.show()


# # Effect of ambeint temperature on power produced plant 2

# In[135]:


merged_df['AMBIENT_TEMPERATURE_CATEGORY'] = pd.cut(
    merged_df['AMBIENT_TEMPERATURE'],
    bins=[-float('inf'), 20, 30, float('inf')],
    labels=['Low', 'Medium', 'High']
)
ambient_temp_vs_powerp2 = merged_df.groupby('AMBIENT_TEMPERATURE_CATEGORY')[['DC_POWER', 'AC_POWER']].mean().reset_index()
ambient_temp_vs_power_meltedp2 = ambient_temp_vs_powerp2.melt(id_vars='AMBIENT_TEMPERATURE_CATEGORY', var_name='Power_Type', value_name='Power')
plt.figure(figsize=(10, 6))
sns.barplot(x='AMBIENT_TEMPERATURE_CATEGORY', y='Power', hue='Power_Type', data=ambient_temp_vs_power_meltedp2)
plt.title('Ambient Temperature vs. Power Output')
plt.xlabel('Ambient Temperature Category')
plt.ylabel('Power (kW)')
plt.legend(title='Power Type')
plt.show()


# # Effect of module temperature on power produced 

# In[133]:


merged_df['MODULE_TEMPERATURE_CATEGORY'] = pd.cut(
    merged_df['MODULE_TEMPERATURE'],
    bins=[-float('inf'), 30, 45, float('inf')],
    labels=['Low', 'Medium', 'High']
)
module_temp_vs_powerp2 = merged_df.groupby('MODULE_TEMPERATURE_CATEGORY')[['DC_POWER', 'AC_POWER']].mean().reset_index()
module_temp_vs_power_meltedp2 = module_temp_vs_powerp2.melt(id_vars='MODULE_TEMPERATURE_CATEGORY', var_name='Power_Type', value_name='Power')
plt.figure(figsize=(14, 7))
sns.barplot(x='MODULE_TEMPERATURE_CATEGORY', y='Power', hue='Power_Type', data=module_temp_vs_power_meltedp2)
plt.title('Module Temperature vs. Power Output')
plt.xlabel('Module Temperature Category')
plt.ylabel('Power (kW)')
plt.legend(title='Power Type')
plt.show()


# In[ ]:
