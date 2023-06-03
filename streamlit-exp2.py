#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import streamlit as st


# Create a file uploader widget
file = st.file_uploader("Upload your file", type=["csv", "xlsx"])

# Check if a file was uploaded
if file is not None:
    # Read the file into a Pandas dataframe
    if file.type == "csv":
        df2 = pd.read_csv(file)
    elif file.type == "xlsx":
        df2 = pd.read_excel(file)
       

st.title('Review Filters')

# Add sliders for selecting filter values
rating_min = st.slider('Minimum Reviewer Score', min_value=0, max_value=10, value=0)
rating_max = st.slider('Maximum Reviewer Score', min_value=0, max_value=10, value=10)
totrev_min = st.slider('Minimum Number of Reviews Reviewer Has Given', min_value=1, max_value=158, value=1)
totrev_max = st.slider('Maximum Number of Reviews Reviewer Has Given', min_value=1, max_value=158, value=158)


# Apply filters to the DataFrame
selected_country = st.selectbox('Select Reviewer\'s Country', ['All'] + sorted(df2['Reviewer_Nationality'].unique()))

# Apply the filter to the DataFrame
selected_sentiments = []
with st.expander("Select Sentiments"):
    with st.container():
        for sentiment_category in ['Positive', 'Neutral', 'Negative']:
            st.write(f"**{sentiment_category}**")
            selected_aspects = st.multiselect(f"Select {sentiment_category} Aspects", df2.columns[4:3219], [])
            selected_sentiments.extend(selected_aspects)

compound_min = st.slider('Minimum Vader Review Score', min_value=-0.9683, max_value=0.9954, value=-0.9683)
compound_max = st.slider('Maximum Vader Review Score', min_value=-0.9683, max_value=0.9954, value=0.9954)

afinn_min = st.slider('Minimum AFINN Review Score', min_value=-20.000, max_value=31.000, value=-20.000)
afinn_max = st.slider('Maximum AFINN Review Score', min_value=-20.000, max_value=31.000, value=31.000)

textblob_min = st.slider('Minimum TextBlob Review Score', min_value=-1.000, max_value=1.000, value=-1.000)
textblob_max = st.slider('Maximum TextBlob Review Score', min_value=-1.000, max_value=1.000, value=1.000)

spacy_min = st.slider('Minimum SpaCy Review Score', min_value=-0.9847, max_value=0.9974, value=-0.9847)
spacy_max = st.slider('Maximum SpaCy Review Score', min_value=0.9847, max_value=0.9974, value=0.9974)

selected_tags = []
with st.expander("Select Tags"):
    with st.container():
        for tag in ['Leisure trip', 'Submitted from a mobile device', 'Couple', 'Stayed 1 night', 'Stayed 2 nights', 'Stayed 3 nights',
                    'Solo traveler', 'Business trip', 'Group', 'Family with young children']:
            if st.checkbox(tag):
                selected_tags.append(tag)

df2['Review_Date'] = pd.to_datetime(df2['Review_Date'])
        
df2.columns = df2.columns.str.strip()
# Apply the filter to the DataFrame
selected_date = st.date_input('Select Date', [df2['Review_Date'].min().date(), df2['Review_Date'].max().date()], key='date_range')
            
filtered_df = df2.copy()
if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['Reviewer_Nationality'] == selected_country]
if selected_sentiments:
    for aspect in selected_sentiments:
        if sentiment_category == 'Positive':
            sentiment = 1
        elif sentiment_category == 'Negative':
            sentiment = -1
        elif sentiment_category == 'Neutral':
            sentiment = 0
        filtered_df = filtered_df[filtered_df[aspect] == sentiment]
if selected_tags:
    filtered_df = filtered_df[filtered_df[selected_tags].any(axis=1)]
filtered_df = filtered_df[
    (filtered_df['Reviewer_Score'] >= rating_min) &
    (filtered_df['Reviewer_Score'] <= rating_max) &
    (filtered_df['Total_Number_of_Reviews_Reviewer_Has_Given'] >= totrev_min) &
    (filtered_df['Total_Number_of_Reviews_Reviewer_Has_Given'] <= totrev_max) &
    (filtered_df['Review_Date'] >= pd.to_datetime(selected_date[0])) &
    (filtered_df['Review_Date'] <= pd.to_datetime(selected_date[1])) &
    (filtered_df['compound'] >= compound_min) &
    (filtered_df['compound'] <= compound_max) &
    (filtered_df['afinn_score_review'] >= afinn_min) &
    (filtered_df['afinn_score_review'] <= afinn_max) &
    (filtered_df['TextBlob_Polarity'] >= textblob_min) &
    (filtered_df['TextBlob_Polarity'] <= textblob_max) &
    (filtered_df['Spacy_compound'] >= spacy_min) &
    (filtered_df['Spacy_compound'] <= spacy_max) 
]
if selected_tags:
    filtered_df = filtered_df[filtered_df[selected_tags].any(axis=1)]


filtered_df = filtered_df['review']

# Display the filtered results
st.write('Filtered Reviews:')
st.write(filtered_df)



