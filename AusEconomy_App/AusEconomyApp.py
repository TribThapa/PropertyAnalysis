import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
from PIL import Image


# Images
#img = Image.open("MapCash.PNG") # this file must be inside the Streamlit folder directory!
#st.image(img, width=None)


st.title("Australian Economy Analysis")

st.write('''
		 This app determines the Australian economy and gives you a quick overview of its
		 finanicals and demographics. Play around with the numbers to see how much Australia's GDP would change
		 by.
		 ''')


# Images
#img = Image.open("GDP_Bar.PNG") # this file must be inside the Streamlit folder directory!
#st.image(img, height=100, width=None,caption="Australia's current GDP")



st.header("Enter your values to predict Australia's GDP")

total_population = st.slider('Population (Example: 7000000)', min_value= 1900000.0, max_value= 50e7, value=25e5, step=1e1)
total_employed = st.slider('Total employed (in millions)', min_value= 4000.0, max_value= 17e4, value=5e3, step=1e1)
total_employed_males = st.slider('Total employed males only (in millions)', min_value= 4000.0, max_value= 17e4, value=5e3, step=1e1)
total_employed_females = st.slider('Total employed females only (in millions)', min_value= 4000.0, max_value= 17e4, value=5e3, step=1e1)
total_unemployed = st.slider('Total unemployed (in millions)', min_value= 4000.0, max_value= 17e4, value=5e3, step=1e1)
total_unemployed_males = st.slider('Total unemployed males only (in millions)', min_value= 4000.0, max_value= 17e4, value=5e3, step=1e1)
total_unemployed_females = st.slider('Total unemployed females only (in millions)', min_value= 4000.0, max_value= 17e4, value=5e3, step=1e1)
cash_rate_target = st.slider('Cash rate', min_value=0.0, max_value= 20.0, value=2.0, step=0.1)
interbank_cash_rate = st.slider('Inter bank cash rate', min_value=0.0, max_value= 20.0, value=2.0, step=0.1)
total_income = st.slider('Total income (in millions)', min_value= 200.0, max_value= 17e6, value=107093.0, step=1e2)
total_savings = st.slider('Total savings (in millions)', min_value= 200.0, max_value= 17e6, value=313.0, step=1e2)



user_input = np.array([total_population,
					   total_employed,
					   total_employed_males,
					   total_employed_females,
					   total_unemployed,
					   total_unemployed_males,
					   total_unemployed_females,
					   cash_rate_target,
					   interbank_cash_rate,
					   total_income,
					   total_savings]).reshape(1, -1)





#Load csv files
gdp = pd.read_csv('GDP.csv')
gdp_bar = pd.read_csv('GDP.csv')
cash_rate = pd.read_csv('CashRate.csv')
population = pd.read_csv('Population.csv')
employment = pd.read_csv('Employment.csv')
economy = pd.read_csv('Economy.csv')
household_income = pd.read_csv('Income.csv')
gdp_new = gdp.rename(columns={"Unnamed: 0": "Year"})

# Get data to create complete table
year = population[["Year"]]
gdp_aus_new = gdp_new[["Australia"]].reset_index(drop=True)

total_population = population[["EstimatedResidentPopulation"]]
total_employed = employment[["TotalEmployed"]]
total_employed_males = employment[["TotalEmployed_M"]]
total_employed_females = employment[["TotalEmployed_F"]]
total_unemployed = employment[["TotalUnemployed"]]
total_unemployed_males = employment[["TotalUnemployed_M"]]
total_unemployed_females = employment[["TotalUnemployed_F"]]

cash_rate_target = cash_rate[["Cash Rate Target"]]
overnight_cash_rate = cash_rate[["Interbank Overnight Cash Rate"]]
household_income_total = household_income[["TotalIncome"]]
household_savings_total = household_income[["TotalSavings"]]

# Create dataframe
correlation_df = pd.concat([gdp_aus_new,
                            total_population,
                            total_employed, 
                            total_employed_males,
                            total_employed_females,
                            total_unemployed,
                            total_unemployed_males,
                            total_unemployed_females,
                            cash_rate_target,
                            overnight_cash_rate,
                            household_income_total,
                            household_savings_total], axis=1)

# Rename to easy convention
correlation_renamed_df = correlation_df.rename(columns={"Australia": "Aus_GDP",
                                                        "EstimatedResidentPopulation": "Pop",
                                                        "TotalEmployed": "Tot Emp",
                                                        "TotalEmployed_M": "Tot Emp_M",
                                                        "TotalEmployed_F": "Tot Emp_F",
                                                        "TotalUnemployed": "Tot Unemp",
                                                        "TotalUnemployed_M": "Tot Unemp_M",
                                                        "TotalUnemployed_F": "Tot Unemp_F"})


# Define x and ay
data = correlation_renamed_df.drop(['Aus_GDP'], axis=1)
target = correlation_renamed_df['Aus_GDP']

# Do train-test split
data_train, data_test, target_train, target_test = train_test_split(data, 
                                                                    target,
                                                                    test_size=0.3,     
                                                                    random_state=101)

# Build Random Forest regressor
random_forest = RandomForestRegressor(random_state=101, 
									  n_estimators=200)

# Build Random Forest model
random_forest.fit(data_train, target_train)

#making a prediction
random_forest_pred = random_forest.predict(user_input) 

st.write('The estimated percent change in the Australian GDP is: ', random_forest_pred)
