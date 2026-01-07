import requests
import json

def test_wikipedia_api():
    query = "Python (programming language)"
    WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": 10,
        "srprop": "snippet"
    }

    headers = {
        'User-Agent': 'MyCoolSearchApp/1.0 (https://example.com/contact)'
    }

    try:
        response = requests.get(WIKIPEDIA_API_URL, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        print(json.dumps(data, indent=2))

        search_results = data.get("query", {}).get("search", [])
        if not search_results:
            print("No search results found in the response.")
            return

        formatted_results = {
            "results": [
                {
                    "title": result["title"],
                    "snippet": result["snippet"],
                    "url": f"https://en.wikipedia.org/wiki/{result['title'].replace(' ', '_')}"
                }
                for result in search_results
            ]
        }
        print("\nFormatted results:")
        print(json.dumps(formatted_results, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    test_wikipedia_api()
