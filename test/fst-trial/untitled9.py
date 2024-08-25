# -*- coding: utf-8 -*-
"""Chatbot with Streamlit and NLTK"""

import streamlit as st
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Step 1: Ensure NLTK Resources are Downloaded
@st.cache_resource  # This caches the download operation to avoid re-downloading
def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('stopwords')

# Download resources
download_nltk_resources()

# Step 2: Load and Preprocess Data
def preprocess_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return ' '.join(filtered_tokens)

# Load CSV file
try:
    data = pd.read_csv('RTU_University-queries.csv')
except FileNotFoundError:
    st.error("CSV file not found. Please ensure the file is in the correct directory.")
    st.stop()

# Verify if 'Query' and 'Intent' columns exist
if 'Query' not in data.columns or 'Intent' not in data.columns:
    st.error("Required columns 'Query' and 'Intent' are not found in the CSV file.")
    st.stop()

# Ensure column names match those in the CSV file
data['processed_query'] = data['Query'].apply(preprocess_text)
data['intent'] = data['Intent']

# Step 3: Prepare Training Data
X = data['processed_query']
y = data['intent']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the Model
model = make_pipeline(CountVectorizer(), MultinomialNB())
model.fit(X_train, y_train)

# Step 5: Implement Chatbot Response Generation
def get_response(user_input):
    processed_input = preprocess_text(user_input)
    intent = model.predict([processed_input])[0]
    responses = {
        "Courses Offered": "RTU Kota offers undergraduate programs in various disciplines including Engineering, Computer Science, Electrical Engineering, Mechanical Engineering, Civil Engineering, and more.",
        "Postgraduate Programs": "Postgraduate programs at RTU Kota include M.Tech, M.Sc., MBA, and M.A. in various fields such as Engineering, Science, Management, and Humanities."
    }
    return responses.get(intent, "Sorry, I didn't understand that.")

# Streamlit UI
st.title('RTU University Chatbot')

# Text input for user query
user_input = st.text_input("You: ")

# Button to get response
if st.button('Send'):
    if user_input:
        response = get_response(user_input)
        st.text_area("Bot:", value=response, height=100, max_chars=None, key=None)
    else:
        st.text_area("Bot:", value="Please enter a query.", height=100, max_chars=None, key=None)
