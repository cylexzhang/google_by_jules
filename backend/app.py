from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import requests
import os

app = Flask(__name__)

# --- Database Setup ---
DB_FILE = "search_history.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE search (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

# --- Routes ---

# Serve frontend files
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

# Search API
@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "A search query is required."}), 400

    # 1. Record the search query in the database
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO search (query) VALUES (?)", (query,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

    # 2. Call the Wikipedia API
    try:
        WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": 10,  # Get the top 10 results
            "srprop": "snippet"
        }
        headers = {
            'User-Agent': 'MyCoolSearchApp/1.0 (https://example.com/contact)'
        }
        response = requests.get(WIKIPEDIA_API_URL, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        # 3. Format the results
        search_results = data.get("query", {}).get("search", [])
        formatted_results = {
            "results": [
                {
                    "title": result["title"],
                    "snippet": result["snippet"].replace('<span class="searchmatch">', '').replace('</span>', ''), # sanitize snippet
                    "url": f"https://en.wikipedia.org/wiki/{result['title'].replace(' ', '_')}"
                }
                for result in search_results
            ]
        }
        return jsonify(formatted_results)

    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return jsonify({"error": "Failed to fetch search results."}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
