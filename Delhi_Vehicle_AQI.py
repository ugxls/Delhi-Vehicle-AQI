#!/usr/bin/env python
# coding: utf-8

# ## Vehicular Activities and its Contribution to Particulate Matter Levels

# ## An Analysis of Air Quality Index and AQI Bucket in Delhi from 2015 to 2020

# In[3]:


#Importing Libraries 
import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


# In[4]:


#Loading datasets into data frames
df = pd.read_csv("city_day.csv")
df_auto = pd.read_csv("delhi-vehicles-2006-2022.csv")


# In[5]:


#Viewing the first five rows of both data frames
#df.head()
df_auto.head()


# In[6]:


#Getting information about both data frames
#df.info()
df_auto.info()


# In[7]:


#Filtering the data frame to cover the scope of the project 
df_delhi = df[df.City == 'Delhi']
df_delhi.reset_index(drop = True, inplace = True)


# In[8]:


#Viewing first five rows of the new data frame
df_delhi.head()


# In[9]:


#Viewing the shape of the data frame
df_delhi.shape


# In[10]:


#Viewing information about the numeric columns
df_delhi.describe()


# In[11]:


#Getting information about the new filtered data frame
df_delhi.info()


# In[12]:


#Filling the missing values in the numeric columns with the mean value

def fill_null_with_mean(df):
    for col in df_delhi.columns:
        if pd.api.types.is_numeric_dtype(df_delhi[col]):
            df_delhi[col] = df_delhi[col].fillna(df_delhi[col].mean())
    return df_delhi

df_delhi = fill_null_with_mean(df_delhi)


# In[13]:


#Dropping AQI and AQI_Bucket to recalculate them
df_delhi.drop(columns = ['AQI', 'AQI_Bucket'], axis = 1, inplace = True)


# In[14]:


#Computing the AQI for each day
def compute_max(row):
    return max(row[2:14])

df_delhi['AQI'] = df_delhi.apply(compute_max, axis=1)


# In[15]:


#Computing the AQI_Bucket for each day based on the AQI
def get_AQI_bucket(x):
    if x <= 50:
        return 'Good'
    elif x <= 100:
        return 'Satisfactory'
    elif x <= 200:
        return 'Moderate'
    elif x <= 300:
        return 'Poor'
    elif x <= 400:
        return 'Very Poor'
    elif x > 400:
        return 'Severe'

df_delhi['AQI_Bucket'] = df_delhi['AQI'].apply(lambda x: get_AQI_bucket(x))


# In[16]:


#Correlation Heatmap Plot
numeric_df = df_delhi.iloc[:, 2:15]
df_corr = numeric_df.corr()
plt.figure(figsize=(10, 6))
sns.heatmap(df_corr, annot = True)
plt.title('Correlation Heatmap of Numeric Columns')
plt.show()


# In[17]:


#Reducing the PM2.5 and PM.10 values by 50% and other pollutants by 50%
reduction_50 = 0.50

df_PM = df_delhi.copy()
df_PM[['PM2.5', 'PM10']] *= (reduction_50)

df_others = df_delhi.copy()
df_others[['NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']] *= (reduction_50)

df_PM['AQI'] = df_PM.apply(compute_max, axis=1)
df_PM['AQI_Bucket'] = df_PM['AQI'].apply(lambda x: get_AQI_bucket(x))


df_others['AQI'] = df_others.apply(compute_max, axis=1)
df_others['AQI_Bucket'] = df_others['AQI'].apply(lambda x: get_AQI_bucket(x))



# In[18]:


#Plots of the AQI Bucket Distribution under three different conditions
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
grouped = df_delhi.groupby('AQI_Bucket')['AQI_Bucket'].count()
grouped.plot(kind='bar', ax=ax1)
ax1.set_xlabel('AQI Bucket')
ax1.set_ylabel('AQI Bucket Count')
ax1.set_title('AQI Bucket Distribution')

grouped_others = df_others.groupby('AQI_Bucket')['AQI_Bucket'].count()
grouped_others.plot(kind='bar', ax=ax2)
ax2.set_xlabel('AQI Bucket')
ax2.set_title('Other pollutants reduced by 50%')

grouped_PM = df_PM.groupby('AQI_Bucket')['AQI_Bucket'].count()
grouped_PM.plot(kind='bar', ax=ax3)
ax3.set_xlabel('AQI Bucket')
ax3.set_title('PM reduced by 50%')

plt.subplots_adjust(wspace=0.5) 

plt.show()


# In[19]:


#Average PM AQI values for each year
df_delhi['Date'] = pd.to_datetime(df_delhi['Date'])
PM_group_year = df_delhi.groupby(df_delhi['Date'].dt.year)[['PM2.5', 'PM10']].mean()
PM_group_year.reset_index(inplace = True)
PM_group_year


# In[20]:


#Formatting Year and Increase (num) column and changing their data types in order to filter the dataframe 
df_auto['Year'] = df_auto['Year'].astype('str')
df_auto['Year'] = df_auto['Year'].str.split('-').str[0]
df_auto['Increase (num)'] = df_auto['Increase (num)'].str.replace(',', '').astype(int)
df_auto['Year'] = df_auto['Year'].astype('int')


# In[21]:


#Filtering the data frame to cover the scope of the project 
filtered_df = df_auto[(df_auto['Year']>= 2015) & (df_auto['Year'] <= 2020)]
filtered_df


# In[22]:


#Plots of the average PM concentration levels and vehicle increase (%) over the years
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(PM_group_year['Date'], PM_group_year['PM2.5'], label='PM2.5')
ax1.plot(PM_group_year['Date'], PM_group_year['PM10'], label='PM10')
ax1.set_xlabel('Year')
ax1.set_ylabel('Average Concentration')
ax1.set_title('Average PM2.5 and PM10 Concentration from 2015 to 2020 in Delhi')
ax1.legend()

ax2.plot(filtered_df['Year'], filtered_df['Increase (%)'])
ax2.set_xlabel('Year')
ax2.set_ylabel('Vehicle Increase (%)')
ax2.set_title('Vehicles Percentage Increase for each Year from 2015 to 2020 in Delhi')

plt.tight_layout()
plt.show()

