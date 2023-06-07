import streamlit as st
import pandas as pd

file_url = 'https://drive.google.com/u/0/uc?id=19r_Ueut0RPcWSxGosk2MKNcTCwbokJn0&export=download'

df2 = pd.read_csv(file_url) 

st.title('Customer Prioritisation Model')

# Create sliders for adjusting column weights
weights = {}
columns = ['room', 'bathroom', 'bedroom', 'bed', 'tv', 'balcony', 'ac', 'air_conditioning',
           'tee_coffee', 'service', 'staff', 'reception', 'receptionist', 'food', 'restaurant',
           'breakfast', 'location', 'noise', 'maintenance']
for column in columns:  
    weights[column] = st.slider(f'Weight for {column}', min_value=0.0, max_value=1.0, value=0.0, step=0.01)

columns_2 = ['Reviewer_Score', 'Total_Number_of_Reviews_Reviewer_Has_Given']

for column in columns_2:  
    weights[column] = st.slider(f'Weight for {column}', min_value=0.0, max_value=1.0, value=0.0, step=0.01)

df2 = df2.fillna(0)
df3 = df2[['room', 'bathroom', 'bedroom', 'bed', 'tv', 'balcony', 'ac', 'air_conditioning',
           'tee_coffee', 'service', 'staff', 'reception', 'receptionist', 'food', 'restaurant',
           'breakfast', 'location', 'noise', 'maintenance']]

# Calculate the weighted rank
df2['Weighted_Rank'] = (-df3 * pd.Series(weights)).sum(axis=1) + (df2[['Reviewer_Score', 'Total_Number_of_Reviews_Reviewer_Has_Given']] * pd.Series(weights)).sum(axis=1)
df2['Review_Date'] = pd.to_datetime(df2['Review_Date'])
selected_date = st.date_input('Select Date', [df2['Review_Date'].min().date(), df2['Review_Date'].max().date()], key='date_range')

filtered_df = df2.copy()
filtered_df = filtered_df[
    (filtered_df['Review_Date'] >= pd.to_datetime(selected_date[0])) &
    (filtered_df['Review_Date'] <= pd.to_datetime(selected_date[1])) 
]

# Sort DataFrame by weighted rank in descending order
df2 = filtered_df.sort_values('Weighted_Rank', ascending=False)

# Display the sorted DataFrame
st.write('Ranked Reviews:')
st.write(df2[['review', 'Weighted_Rank']])

