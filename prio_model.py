#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import streamlit as st

file_url = 'https://drive.google.com/u/0/uc?id=19r_Ueut0RPcWSxGosk2MKNcTCwbokJn0&export=download'

df2 = pd.read_csv(file_url)

df2['Review_Date'] = pd.to_datetime(df2['Review_Date'])
st.title('Review Filters (Including Prioritisation Model)')

# Add sliders for selecting filter values
rating_range = st.slider('Reviewer Score Range', min_value=0, max_value=10, value=(0, 10))
totrev_range = st.slider('Number of Reviews Reviewer Has Given', min_value=1, max_value=158, value=(1, 158))
rev_range = st.slider('Review Experience', min_value=0.006329, max_value=1.00, value=(0.006329, 1.00))

# Apply filters to the DataFrame
selected_country = st.selectbox('Select Reviewer\'s Country', ['All'] + sorted(df2['Reviewer_Nationality'].unique()))

# Apply the filter to the DataFrame
selected_sentiments = []
with st.expander("Select Sentiments"):
    with st.container():
        for sentiment_category in ['Positive', 'Negative']:
            st.write(f"**{sentiment_category}**")
            selected_aspects = st.multiselect(f"Select {sentiment_category} Aspects", df2.columns[4:3219], [])
            selected_sentiments.extend(selected_aspects)

changeable_aspect_range = st.slider('Important Aspect Sentiment Score', min_value=-0.230769, max_value=0.153846, value=(-0.230769, 0.153846))

compound_range = st.slider('Vader Review Score', min_value=-0.9683, max_value=0.9954, value=(-0.9683, 0.9954))

afinn_range = st.slider('AFINN Review Score', min_value=-20.000, max_value=31.000, value=(-20.000, 31.000))

textblob_range = st.slider('TextBlob Review Score', min_value=-1.000, max_value=1.000, value=(-1.000, 1.000))

spacy_range = st.slider('SpaCy Review Score', min_value=-0.9847, max_value=0.9974, value=(-0.9847, 0.9974))


selected_tags = []
with st.expander("Select Tags"):
    with st.container():
        for tag in ['Leisure trip', 'Submitted from a mobile device', 'Couple', 'Stayed 1 night', 'Stayed 2 nights', 'Stayed 3 nights',
                    'Solo traveler', 'Business trip', 'Group', 'Family with young children']:
            if st.checkbox(tag):
                selected_tags.append(tag)

df2.columns = df2.columns.str.strip()



# Apply the filter to the DataFrame
selected_date = st.date_input('Select Date', [df2['Review_Date'].min().date(), df2['Review_Date'].max().date()], key='date_range')

rank_range = st.slider('Reviewer Ranking Score', min_value=-0.113486, max_value=0.333398, value=(-0.113486, 0.333398))

filtered_df = df2.copy()
if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['Reviewer_Nationality'] == selected_country]
if selected_sentiments:
    for aspect in selected_sentiments:
        if sentiment_category == 'Positive':
            sentiment = 1
        elif sentiment_category == 'Negative':
            sentiment = -1
        filtered_df = filtered_df[filtered_df[aspect] == sentiment]
if selected_tags:
    filtered_df = filtered_df[filtered_df[selected_tags].any(axis=1)]
filtered_df = filtered_df[
    (filtered_df['Reviewer_Score'] >= rating_range[0]) &
    (filtered_df['Reviewer_Score'] <= rating_range[1]) &
    (filtered_df['Total_Number_of_Reviews_Reviewer_Has_Given'] >= totrev_range[0]) &
    (filtered_df['Total_Number_of_Reviews_Reviewer_Has_Given'] <= totrev_range[1]) &
    (filtered_df['maturity_score'] >= rev_range[0]) &
    (filtered_df['maturity_score'] <= rev_range[1]) &
    (filtered_df['Review_Date'] >= pd.to_datetime(selected_date[0])) &
    (filtered_df['Review_Date'] <= pd.to_datetime(selected_date[1])) &
    (filtered_df['changeable_aspect_sentiment_score'] >= changeable_aspect_range[0]) &
    (filtered_df['changeable_aspect_sentiment_score'] <= changeable_aspect_range[1]) &
    (filtered_df['compound'] >= compound_range[0]) &
    (filtered_df['compound'] <= compound_range[1]) &
    (filtered_df['afinn_score_review'] >= afinn_range[0]) &
    (filtered_df['afinn_score_review'] <= afinn_range[1]) &
    (filtered_df['TextBlob_Polarity'] >= textblob_range[0]) &
    (filtered_df['TextBlob_Polarity'] <= textblob_range[1]) &
    (filtered_df['Spacy_compound'] >= spacy_range[0]) &
    (filtered_df['Spacy_compound'] <= spacy_range[1]) &
    (filtered_df['customer_ranking_score'] >= rank_range[0]) &
    (filtered_df['customer_ranking_score'] <= rank_range[1])    
]
    
if selected_tags:
    filtered_df = filtered_df[filtered_df[selected_tags].any(axis=1)]


filtered_df = filtered_df['review']

# Display the filtered results
st.write('Filtered Reviews:')
st.write(filtered_df)


# In[ ]:




