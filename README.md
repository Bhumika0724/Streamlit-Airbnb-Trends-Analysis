# Airbnb Analysis Using PowerBI
## Overview
This project enables users to delve into accommodation trends. After retrieving and cleaning sample data, insights are derived through exploratory data analysis (EDA). The cleaned data is then utilized for analysis and visualization of trends using Power BI.
## Table of Contents
- [Key Technologies and Skills](#key-technologies-and-skills)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Approach](#approach)
- [Contact](#contact)
# Key Technologies and Skills
- Python Scripting
- Streamlit
- Data Cleaning and analysis
- Pandas-Dataframe
- EDA Analysis
- Data visualization using Plotly and Powerbi
# Installation
To run this project, please install below python packages as prerequisites.

```bash
pip install streamlit
pip install pandas
pip install plotly
pip install numpy
pip install scipy
```
# Usage
To use this project, Please follow the below steps.
- To clone this repository: ```git clone https://github.com/Gokulakkrizhna/Airbnb_analysis.git```
- Install the required packages: ```pip install -r requirements.txt ```
- To extract and clean data:```python Datacoll_dataclean.py```
- To perform EDA analysis:```python eda_analysis.py```
- Run the Streamlit app: ```streamlit run Dataextract_visual.py```
- Access the app in your browser at ```http://localhost:8501```
# Features
- Fetch Airbnb data from JSON file
- Data Cleaning and pre-processing
- Perform EDA analysis
- Visualize data using Plotly and Pandas DataFrames
- User-friendly interface powered by Streamlit
- User-friendly Powerbi dashboard
# Approach
```Data Collection```: Clone the airbnb data from your local directory. 

```Data Cleaning```: Refine pre-processing methods like Data handling is applied to the collected data.

```Statistical Analysis```: Cleaned numerical data has been analysed to get a valuable insights.

```EDA Analysis```: The cleaned data has been analyzed using various exploratory data analysis (EDA) techniques, revealing insights into current trends.

```Setup the Streamlit app```: Streamlit is a user-friendly web development tool that simplifies the process of creating intuitive interfaces.

```Data Analysis```: Cleaned data has been analyzed and visualized in Streamlit through Pandas DataFrame.

```Data Visualization```: Cleaned data has been visualized using Plotly to gain valuable insights from the datasets.

```Setup Powerbi dashboard```: The cleaned data has been analyzed and visualized using an interactive Power BI dashboard.

The provided code utilizes Python scripting along with various libraries to fetch data from the our local directory. Data manipulation techniques are then applied, followed by exploratory data analysis (EDA) on the cleaned dataset to extract meaningful insights. Furthermore, the implementation includes a Streamlit web application to enhance user engagement and create an intuitive dashboard in PowerBi.

Here's a breakdown of what the code does:
- Importing all the neccessary libraries includes ```Streamlit``` which creates UI to interact with user and display the analysed data, ```Pandas``` which helps to display the analysed data in Streamlit web,```numpy``` which will help in mathematical conversion,```Plotly```  is employed to visualize the data and gain insights from it,```OS``` assists in reading data from the local directory,```JSON``` is used to load JSON files into Python,```Scipy``` aids in conducting exploratory data analysis (EDA) and extracting valuable insights.
```bash
import os
import pandas as pd
import json
import numpy as np
import scipy.stats as stats
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
```
- ```Datacoll_dataclean``` file is responsible for fetching data from the local directory and performing necessary data cleaning operations. **Note: Replace your actual path in ```path```**
```bash
path = r"please provide the path"
```
- ```eda_analysis``` file is responsible for exploratory data analysis (EDA) and extracting valuable insights.
- ```Dataextract_visual``` file is used to extract the data stored in MySQL and visualize it to derive valuable insights using Plotly.
- Five separate tabs have been implemented in the Streamlit web application to facilitate user interaction and enhance data visualization for insightful analysis.
```bash
tab1, tab2, tab3, tab4,tab5,tab6= st.tabs(["Home", "Geo visualization", " Website","Statistical Insights","EDA Insights","Data visualization"])
```
- In Tab1 of the Streamlit web application, user can select type of ```Country``` and ```No of people``` for which they need to visualize the data in Geo visualization.
- In Tab2 of the Streamlit web application, the user-input location will be displayed using Geo visualization.
- In Tab3, the Streamlit web application mimics the layout and functionality of the Airbnb website using the cleaned data, providing users with an interactive experience similar to browsing Airbnb listings.
- In Tab4, Cleaned data has undergone Statistical analysis procedure to get a valuable insights.
- In Tab5, exploratory data analysis (EDA) was conducted on the dataset to extract valuable insights, which are then presented to the user for further analysis and interpretation.
- In Tab6, Cleaned data has been analyzed, and visualized to extract valuable insights.


This Python script streamlines the process of fetching data from a local directory, implementing crucial data cleaning procedures, and conducting exploratory data analysis (EDA) to extract valuable insights. This comprehensive approach empowers users to gain valuable insights and make informed decisions based on the visualized data.

## PowerBI Dashboard
Build an user friendly PowerBI dashboard to vizualize and get an insights of an airbnb data. Explore ```Airbnb.pdf``` for in-depth analysis.

# Contact
📧 Email: [gokulakkrizhna@gmail.com](mailto:gokulakkrizhna@gmail.com)

🌐 LinkedIn: [linkedin.com/in/gokulakkrizhna-s-241562159](https://www.linkedin.com/in/gokulakkrizhna-s-241562159/)

For any further questions or inquiries, feel free to reach out. We are happy to assist you with any queries.
  
