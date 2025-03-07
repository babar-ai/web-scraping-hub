from concurrent.futures import ThreadPoolExecutor
import requests
import json
from dotenv import load_dotenv
import os 

load_dotenv()

#TO load gemni api key
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Define major cities of a specific country (e.g., Denmark)
country = "Denmark"
cities = [
    "Copenhagen", "Aarhus", "Odense", "Aalborg", "Esbjerg", "Randers", "Kolding", "Horsens", "Vejle", "Roskilde"
]

# Define search queries
keywords = [
    "plan room", "construction plan PDFs", "construction plan room pdf"
]

# Function to search using Serper.dev API
def search_google(query, page):
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    data = json.dumps({"q": query + " filetype:pdf", "num": 10, "start": page * 10})
    response = requests.post(url, headers=headers, data=data)
    return response.json() if response.status_code == 200 else None

# Function to process a single search query
def process_query(city, keyword):
    query = f"{keyword} {city} {country} filetype:pdf"
    print(f"Searching: {query}")
    pdf_links = []
    with ThreadPoolExecutor(max_workers=5) as executor:  # Use multithreading for faster searches
        futures = [executor.submit(search_google, query, page) for page in range(10)]  # Limit to 5 pages
        for future in futures:
            search_result = future.result()
            if search_result:
                pdf_links.extend([result["link"] for result in search_result.get("organic", []) if result["link"].endswith(".pdf")])
    return query, pdf_links

# Iterate over cities and keywords using parallel processing
results = {}
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_query, city, keyword) for city in cities for keyword in keywords]
    for future in futures:
        query, pdf_links = future.result()
        results[query] = pdf_links

# Save results to a JSON file
with open("search_results.json", "w") as f:
    json.dump(results, f, indent=4)

print(f"Search complete for {country}. Results saved to search_results.json.")
