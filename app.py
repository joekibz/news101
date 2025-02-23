import requests
import json
import datetime
import pandas as pd #optional
import streamlit as st

# Function to fetch news
def get_top_headlines(api_key, category=None, country=None, language="en"):
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "language": language,
        "pageSize": 10
    }

    if category:
        params["category"] = category
    if country:
        params["country"] = country

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "ok":
            return data["articles"]
        else:
            st.error(f"NewsAPI error: {data['message']}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="📰 News Dashboard", layout="wide")
st.title("📰 Latest News Headlines")

api_key = st.text_input("Enter your NewsAPI Key", type="password")

category = st.selectbox("Select Category", [None, "business", "technology", "sports", "entertainment"])
country = st.selectbox("Select Country", [None, "us", "gb", "ca", "au"])

if st.button("Fetch News"):
    if api_key:
        articles = get_top_headlines(api_key, category, country)

        if articles:
            for article in articles:
                st.markdown(
                    f"""
                    <div style="border:1px solid #ddd; padding:10px; border-radius:10px; margin-bottom:10px; background-color:#f9f9f9;">
                        <h3 style="color:#333;">{article['title']}</h3>
                        <p>{article['description']}</p>
                        <a href="{article['url']}" target="_blank" style="color:blue; font-weight:bold;">Read more</a>
                        <p style="font-size:12px; color:gray;">Published: {article['publishedAt']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("No articles found.")
    else:
        st.warning("Please enter your API key.")

