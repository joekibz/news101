import requests
import streamlit as st

# Function to fetch news
def fetch_news(api_key, search_query=None, category=None, country=None, language="en", use_everything=False):
    base_url = "https://newsapi.org/v2/everything" if use_everything else "https://newsapi.org/v2/top-headlines"
    
    params = {
        "apiKey": api_key,
        "language": language,
        "pageSize": 10,
    }
    
    if use_everything:
        if not search_query:
            st.error("Please enter a search query for Everything search.")
            return None
        params["q"] = search_query
    else:
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
st.title("📰 Latest News Dashboard")

api_key = st.text_input("Enter your NewsAPI Key", type="password")

# Tabs for Everything & Top Headlines
tab1, tab2 = st.tabs(["Everything Search", "Top Headlines"])

# "Everything" Search Tab
with tab1:
    st.subheader("🔎 Search Any News Topic")
    search_query = st.text_input("Enter search keywords")
    if st.button("Search News"):
        if api_key and search_query:
            articles = fetch_news(api_key, search_query=search_query, use_everything=True)
            if articles:
                for article in articles:
                    st.markdown(
                        f"""
                        <div style="border:1px solid #ddd; padding:10px; border-radius:10px; margin-bottom:10px; background-color:#f9f9f9;">
                            <h3 style="color:#333;">{article['title']}</h3>
                            <p>{article.get('description', 'No description available.')}</p>
                            <a href="{article['url']}" target="_blank" style="color:blue; font-weight:bold;">Read more</a>
                            <p style="font-size:12px; color:gray;">Published: {article['publishedAt']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.warning("No articles found.")
        else:
            st.warning("Please enter your API key and search query.")

# "Top Headlines" Tab
with tab2:
    st.subheader("📢 Get Latest Headlines")
    categories = [None, "business", "entertainment", "general", "health", "science", "sports", "technology"]
    countries = [
        None, "ae", "ar", "at", "au", "be", "bg", "br", "ca", "ch", "cn", "co", "cu", "cz", "de", "eg", "fr", "gb", "gr", "hk", "hu", "id", "ie", "il", "in", "it", "jp", "kr", "lt", "lv", "ma", "mx", "my", "ng", "nl", "no", "nz", "ph", "pl", "pt", "ro", "rs", "ru", "sa", "se", "sg", "si", "sk", "th", "tr", "tw", "ua", "us", "ve", "za"
    ]
    
    category = st.selectbox("Select Category", categories)
    country = st.selectbox("Select Country", countries)
    
    if st.button("Fetch Headlines"):
        if api_key:
            articles = fetch_news(api_key, category=category, country=country, use_everything=False)
            if articles:
                for article in articles:
                    st.markdown(
                        f"""
                        <div style="border:1px solid #ddd; padding:10px; border-radius:10px; margin-bottom:10px; background-color:#f9f9f9;">
                            <h3 style="color:#333;">{article['title']}</h3>
                            <p>{article.get('description', 'No description available.')}</p>
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
