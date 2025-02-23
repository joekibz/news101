import requests
import streamlit as st

# Function to fetch news
def get_news(api_key, query=None, category=None, country=None, language="en", news_type="top-headlines", pages=1):
    base_url = f"https://newsapi.org/v2/{news_type}"
    articles = []

    for page in range(1, pages + 1):
        params = {
            "apiKey": api_key,
            "language": language,
            "pageSize": 100,  # Max per request
            "page": page
        }

        if news_type == "everything":
            params["q"] = query  # Use query for everything search
        else:
            if category:
                params["category"] = category
            if country:
                params["country"] = country

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "ok":
                articles.extend(data.get("articles", []))
            else:
                st.error(f"NewsAPI error: {data.get('message')}")
                break
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data: {e}")
            break

    return articles

# Streamlit UI
st.set_page_config(page_title="📰 News Dashboard", layout="wide")
st.title("📰 Latest News Dashboard")

api_key = st.text_input("Enter your NewsAPI Key", type="password")

news_type = st.radio("Choose News Type", ["Top Headlines", "Everything"], horizontal=True)

if news_type == "Everything":
    query = st.text_input("Enter your search query:")
    st.caption("Example: AI, Bitcoin, Climate Change, Tesla, Olympics")
    category = None
    country = None
else:
    query = None
    category = st.selectbox("Select Category", [None, "business", "entertainment", "general", "health", "science", "sports", "technology"])
    country = st.selectbox("Select Country", [None, "ae", "ar", "at", "au", "be", "bg", "br", "ca", "ch", "cn", "co", "cu", "cz", "de",
                                               "eg", "fr", "gb", "gr", "hk", "hu", "id", "ie", "il", "in", "it", "jp", "kr", "lt", 
                                               "lv", "ma", "mx", "my", "ng", "nl", "no", "nz", "ph", "pl", "pt", "ro", "rs", "ru",
                                               "sa", "se", "sg", "si", "sk", "th", "tr", "tw", "ua", "us", "ve", "za"])

num_pages = st.slider("Select number of pages to fetch", 1, 5, 1)

if st.button("Fetch News"):
    if api_key:
        news_type_param = "everything" if news_type == "Everything" else "top-headlines"
        articles = get_news(api_key, query, category, country, news_type=news_type_param, pages=num_pages)

        if articles:
            for article in articles:
                st.markdown(
                    f"""
                    <div style="border:1px solid #ddd; padding:10px; border-radius:10px; margin-bottom:10px; background-color:#f9f9f9;">
                        <h3 style="color:#333;">{article['title']}</h3>
                        <p>{article.get('description', 'No description available')}</p>
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
