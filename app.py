import requests
import json
import datetime
import pandas as pd #optional

def get_top_headlines(api_key, category=None, country=None, language="en"):
    """
    Fetches top headlines from NewsAPI.org.
    Args:
        api_key: Your NewsAPI.org API key.
        category: News category (e.g., "world", "business", "technology"). Optional.
        country: Country code (e.g., "us", "gb"). Optional.
        language: Language code (e.g., "en", "es"). Defaults to "en".
    Returns:
        A list of dictionaries representing the articles, or None if an error occurs.
    """
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "language": language,
        "pageSize": 100  # Maximum allowed by NewsAPI
    }

    if category:
        params["category"] = category
    if country:
        params["country"] = country

    try:
        response = requests.get(base_url, params=params)
        print("Request URL:", response.url)  # Debugging output
        response.raise_for_status()
        data = response.json()
        print("Response Data:", data)  # Debugging output

        if data["status"] == "ok":
            return data["articles"]
        else:
            print(f"NewsAPI error: {data['message']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

# Example usage:
api_key = "573f2f6a79e642ac8d319f73939171ed"  # Replace with your API key
category = "business"  # Choose a category or set to None
country = "None"  # Choose a country code or set to None

articles = get_top_headlines(api_key, category=category)

if articles:
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}")
        print(f"Published At: {article['publishedAt']}")
        print("-" * 20)
else:
    print("Failed to retrieve news articles.")
