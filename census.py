# Import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

@st.cache()
def load_data():
	# Load the Adult Income dataset into DataFrame.

	df = pd.read_csv('https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/whitehat-ds-datasets/adult.csv', header=None)
	df.head()

	# Rename the column names in the DataFrame using the list given above. 

	# Create the list
	column_name =['age', 'workclass', 'fnlwgt', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race','gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']

	# Rename the columns using 'rename()'
	for i in range(df.shape[1]):
	  df.rename(columns={i:column_name[i]},inplace=True)

	# Print the first five rows of the DataFrame
	df.head()

	# Replace the invalid values ' ?' with 'np.nan'.

	df['native-country'] = df['native-country'].replace(' ?',np.nan)
	df['workclass'] = df['workclass'].replace(' ?',np.nan)
	df['occupation'] = df['occupation'].replace(' ?',np.nan)

	# Delete the rows with invalid values and the column not required 

	# Delete the rows with the 'dropna()' function
	df.dropna(inplace=True)

	# Delete the column with the 'drop()' function
	df.drop(columns='fnlwgt',axis=1,inplace=True)

	return df

census_df = load_data()

# Write your code to filter streamlit warnings 
st.set_option('deprecation.showPyplotGlobalUse', False)

# Write the code to design the web app
st.title("Census Visualisation App")
 
# Add title on the main page and in the sidebar.
st.sidebar.title("Menu")
# Using the 'if' statement, display raw data on the click of the checkbox.
if st.sidebar.checkbox("Show Raw Data"):
  st.subheader("Census Data Frame")
  st.dataframe(census_df)
  st.write(f"Number of rows are:{census_df.shape[0]} , Number of Columns are:{census_df.shape[1]}") 
# Add a multiselect widget to allow the user to select multiple visualisations.
# Add a subheader in the sidebar with the label "Visualisation Selector"
st.sidebar.subheader("Visualisation Selector")

# Add a multiselect in the sidebar with label 'Select the Charts/Plots:'
# Store the current value of this widget in a variable 'plot_list'.
plt_typ = st.sidebar.multiselect("Select the Plot" , ('Box Plot', 'Count Plot', 'Pie Chart'))

# Display pie plot using matplotlib module and 'st.pyplot()'
if 'Pie Chart' in plt_typ:
  st.subheader("Pie Chart") 
  plt_pie = st.sidebar.multiselect("Select the column for Pie chart" , ("income" , "gender"))
  for i in plt_pie:
    data_pie = census_df[i].value_counts()
    plt.figure(figsize = (15 , 10))
    plt.title(f"Pie Chart for {i}")
    plt.pie(data_pie , labels = data_pie.index , autopct = "%.2f%%" , explode = np.linspace(0.05 , 0.15 , len(data_pie)))
    st.pyplot()

# Display box plot using matplotlib module and 'st.pyplot()'
if 'Box Plot' in plt_typ:
  st.subheader("Box Plot")
  cols = st.sidebar.multiselect("Select the columns to create its Box Plot" , ('income' , 'gender')) 
  for i in cols:
    plt.figure(figsize = (15 , 10))
    plt.title(f"Box Plot for {i}")
    sns.boxplot(census_df["hours-per-week"] , census_df[i])
    st.pyplot()

# Display count plot using seaborn module and 'st.pyplot()' 
if 'Count Plot' in plt_typ:
  st.subheader("Count Plot") 
  plt.figure(figsize = (15 , 10))
  plt.title(f"Count Plot for Workclass")
  sns.countplot(census_df['workclass'] , hue = census_df["income"])
  st.pyplot()
