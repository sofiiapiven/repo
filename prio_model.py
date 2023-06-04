import streamlit as st
import pandas as pd

file_url = 'https://drive.google.com/u/0/uc?id=19r_Ueut0RPcWSxGosk2MKNcTCwbokJn0&export=download'

df2 = pd.read_csv(file_url)

st.title('Review Filters')

# Add sliders for selecting filter values
rating_min = st.slider('Minimum Reviewer Score', min_value=0, max_value=10, value=0)
rating_max = st.slider('Maximum Reviewer Score', min_value=0, max_value=10, value=10)
totrev_min = st.slider('Minimum Number of Reviews Reviewer Has Given', min_value=1, max_value=158, value=1)
totrev_max = st.slider('Maximum Number of Reviews Reviewer Has Given', min_value=1, max_value=158, value=158)
rev_min = st.slider('Minimum Reviewer Experience', min_value=0.006329, max_value=1.00, value=0.006329)
rev_max = st.slider('Maximum Reviewer Experience', min_value=0.006329, max_value=1.00, value=1.00)


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

changeable_aspect_min = st.slider('Minimum Important Aspect Sentiment Score', min_value=-0.230769, max_value=0.153846, value=-0.230769)
changeable_aspect_max = st.slider('Maximum Important Aspect Sentiment Score', min_value=-0.230769, max_value=0.153846, value=0.153846)

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
            

# Apply the filter to the DataFrame
df2['Review_Date'] = pd.to_datetime(df2['Review_Date'])
selected_date = st.date_input('Select Date', [df2['Review_Date'].min().date(), df2['Review_Date'].max().date()], key='date_range')

rank_min = st.slider('Minimum Reviewer Ranking Score', min_value=-0.113486, max_value=0.333398, value=-0.113486)
rank_max = st.slider('Maximum Reviewer Ranking Score', min_value=-0.113486, max_value=0.333398, value=0.333398)

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
    (filtered_df['maturity_score'] >= rev_min) &
    (filtered_df['maturity_score'] <= rev_max) &
    (filtered_df['Review_Date'] >= pd.to_datetime(selected_date[0])) &
    (filtered_df['Review_Date'] <= pd.to_datetime(selected_date[1])) &
    (filtered_df['changeable_aspect_sentiment_score'] >= changeable_aspect_min) &
    (filtered_df['changeable_aspect_sentiment_score'] <= changeable_aspect_max) &
    (filtered_df['compound'] >= compound_min) &
    (filtered_df['compound'] <= compound_max) &
    (filtered_df['afinn_score_review'] >= afinn_min) &
    (filtered_df['afinn_score_review'] <= afinn_max) &
    (filtered_df['TextBlob_Polarity'] >= textblob_min) &
    (filtered_df['TextBlob_Polarity'] <= textblob_max) &
    (filtered_df['Spacy_compound'] >= spacy_min) &
    (filtered_df['Spacy_compound'] <= spacy_max) &
    (filtered_df['customer_ranking_score'] >= rank_min) &
    (filtered_df['customer_ranking_score'] <= rank_max) 
]
if selected_tags:
    filtered_df = filtered_df[filtered_df[selected_tags].any(axis=1)]


filtered_df = filtered_df['review']

# Display the filtered results
st.write('Filtered Reviews:')
st.write(filtered_df)
