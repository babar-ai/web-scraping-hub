import requests
import json
import streamlit as st
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from dotenv import load_dotenv
import os 

load_dotenv()

# Load Serper API key
SERPER_API_KEY = os.getenv("SERPER_API_KEY_1")

if not SERPER_API_KEY:
    st.error("API Key not found. Check your .env file.")
    st.stop()

# Function to search using Serper.dev API
def search_google(query, page):
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    data = json.dumps({"q": query, "num": 10, "start": page * 10})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        return None
    return response.json()

# Function to process a search query
def process_query(city, keyword, country):
    query = f"{keyword} {city} {country} filetype:pdf"
    pdf_links = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(search_google, query, page) for page in range(10)]
        for future in futures:
            search_result = future.result()
            if search_result:
                pdf_links.extend([result["link"] for result in search_result.get("organic", []) if result["link"].endswith(".pdf")])
    return city, query, pdf_links

# Streamlit App
st.title("Construction Plan PDF Search")

# User input for country
country = st.text_input("Enter country name", "Denmark")

# User input for major cities
cities_input = st.text_area(
    "Enter major cities (comma-separated)", 
    "Copenhagen, Aarhus, Odense, Aalborg, Esbjerg, Randers, Kolding, Horsens, Vejle, Roskilde"
)
cities = [city.strip() for city in cities_input.split(",") if city.strip()]

# Define search queries
# keywords = ["plan room", "construction plan PDFs", "room", "room architectural drawing"]
keywords = [
    "room and floor construction drawing PDFs",
    "construction drawing PDFs",
    "room and floor architectural drawing",
    "architectural floor plan drawing PDFs",
]

print(keywords)


if st.button("Search PDFs"):
    if not cities:
        st.error("Please enter at least one city.")
    else:
        st.write(f"Searching PDFs for cities in {country}...")
        
        results = {}
        all_links = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_query = {
                executor.submit(process_query, city, keyword, country): city
                for city in cities for keyword in keywords
            }

            for future in future_to_query:
                city, query, pdf_links = future.result()
                if city not in results:
                    results[city] = []
                results[city].extend(pdf_links)
                for link in pdf_links:
                    all_links.append([city, query, link])
        
        # Display results in dropdowns
        for city, links in results.items():
            with st.expander(f"Construction Plan PDF Links for {city}, {country}"):
                if not links:
                    st.warning(f"No PDFs found for {city}.")
                else:
                    for i, link in enumerate(links, 1):
                        st.markdown(f"{i}. [PDF Link]({link})")
        
        # Convert results to a DataFrame for CSV download
        df = pd.DataFrame(all_links, columns=["City", "Search Query", "PDF URL"])
        
        # Download button for CSV
        if not df.empty:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download PDF URLs",
                data=csv,
                file_name="pdf_search_results.csv",
                mime="text/csv"
            )
