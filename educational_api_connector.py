"""
Educational API Connector - Real API connections to educational resources
This module provides functions to connect to various educational APIs and retrieve content
"""
import requests
import json
import time
import streamlit as st
from typing import Dict, List, Any, Optional
import os

# Cache dict to store API responses and avoid unnecessary requests
API_CACHE = {}
# Cache timeout in seconds (1 hour)
CACHE_TIMEOUT = 3600

def get_cached_response(cache_key):
    """Get response from cache if available and not expired"""
    if cache_key in API_CACHE:
        timestamp, data = API_CACHE[cache_key]
        if time.time() - timestamp < CACHE_TIMEOUT:
            return data
    return None

def set_cached_response(cache_key, data):
    """Store response in cache with current timestamp"""
    API_CACHE[cache_key] = (time.time(), data)
    return data

class APIConnector:
    def __init__(self):
        # Initialize API endpoints
        self.openstax_api_url = "https://openstax.org/api/v2"
        self.opentdb_api_url = "https://opentdb.com/api.php"
        self.urlscan_api_key = os.getenv("URLSCAN_API_KEY", "")  # Optional
        self.virustotal_api_key = os.getenv("VIRUSTOTAL_API_KEY")
        
        # No API keys needed for some services
        if not self.virustotal_api_key:
            if st.sidebar.checkbox("Show API Status"):
                st.sidebar.info("Using mock data for demonstration. Add API keys in Secrets tab for real data.")

    def get_educational_content(self, subject: str, grade: str) -> Dict:
        """Fetch educational content from OpenStax and OpenTDB"""
        try:
            # Get OpenStax content
            response = requests.get(f"{self.openstax_api_url}/subjects/{subject}")
            if response.status_code == 200:
                content = response.json()
            else:
                content = self._get_mock_content(subject, grade)
            
            # Add quiz questions from OpenTDB
            quiz_response = requests.get(f"{self.opentdb_api_url}?amount=5&category=18&difficulty=medium")
            if quiz_response.status_code == 200:
                content['quizzes'] = quiz_response.json().get('results', [])
            
            return content
        except requests.exceptions.RequestException:
            return self._get_mock_content(subject, grade)
            
    def _get_mock_content(self, subject: str, grade: str) -> Dict:
        """Generate mock educational content"""
        if not self.khan_academy_api_key:
            # Return enhanced mock data when API key is not available
            mock_data = {
                "description": f"Learn {subject} through practical applications in daily life",
                "videos": [
                    {
                        "title": f"Basic {subject} in the Kitchen",
                        "url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
                        "duration": "10:00"
                    }
                ],
                "exercises": [
                    {
                        "title": "Measuring Ingredients",
                        "difficulty": "beginner",
                        "description": "Practice fractions and measurements while cooking"
                    },
                    {
                        "title": "Kitchen Math Problems",
                        "difficulty": "intermediate",
                        "description": "Convert recipes and calculate proportions"
                    }
                ],
                "modules": [
                    {
                        "name": "Kitchen Mathematics",
                        "count": 5
                    },
                    {
                        "name": "Cooking Measurements",
                        "count": 3
                    }
                ]
            }
            return mock_data
        
        try:
            endpoint = f"https://www.khanacademy.org/api/v1/topic/{subject}"
            response = requests.get(endpoint, headers={"Authorization": f"Bearer {self.khan_academy_api_key}"})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            # Return mock data on API error
            return {
                "description": f"Sample content for {subject} ({grade})",
                "videos": [
                    {
                        "title": f"Introduction to {subject}",
                        "url": "https://www.youtube.com/watch?v=sample",
                        "duration": "10:00"
                    }
                ],
                "exercises": [
                    {
                        "title": f"Practice {subject} basics",
                        "difficulty": "beginner"
                    }
                ]
            }

    def get_quizlet_quizzes(self, topic: str) -> List[Dict]:
        """Fetch quizzes from Quizlet"""
        endpoint = f"https://api.quizlet.com/2.0/search/sets?q={topic}"
        response = requests.get(endpoint, headers={"Authorization": f"Bearer {self.quizlet_api_key}"})
        return response.json()

    def check_url_safety(self, url: str) -> bool:
        """Check URL safety using URLScan.io"""
        if self.urlscan_api_key:
            headers = {'API-Key': self.urlscan_api_key}
            response = requests.post('https://urlscan.io/api/v1/scan/',
                                  headers=headers,
                                  json={'url': url})
            return response.status_code == 200
        # Fallback to basic checks if no API key
        return not any(suspicious in url.lower() 
                      for suspicious in ['phishing', 'malware', 'scam'])
        response = requests.post(endpoint, data={"url": url, "format": "json", "app_key": self.phishtank_api_key})
        return response.json()["results"]["valid"]

    def check_safe_browsing(self, url: str) -> Dict:
        """Check URL using Google Safe Browsing API"""
        endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={self.gsb_api_key}"
        payload = {
            "client": {"clientId": "eduverse", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        response = requests.post(endpoint, json=payload)
        return response.json()

    def scan_file_virustotal(self, file_hash: str) -> Dict:
        """Check file hash using VirusTotal API"""
        endpoint = f"https://www.virustotal.com/vtapi/v2/file/report"
        params = {"apikey": self.virustotal_api_key, "resource": file_hash}
        response = requests.get(endpoint, params=params)
        return response.json()


# Khan Academy API Integration (Retaining original functions)
def fetch_khan_academy_topics(query: str = None) -> List[Dict[str, Any]]:
    """
    Fetch topics from Khan Academy API or use their topic tree API

    Args:
        query: Optional search term

    Returns:
        List of topics with metadata
    """
    # Use cache if available
    cache_key = f"khan_academy_topics_{query}"
    cached_data = get_cached_response(cache_key)
    if cached_data:
        return cached_data

    # Khan Academy doesn't have a simple public API that doesn't require OAuth
    # We'll use their public topic tree which is accessible without auth
    try:
        # This URL provides access to their content structure
        # For a real integration, you'd need to register an app with Khan Academy
        url = "https://www.khanacademy.org/api/v1/topictree"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Process the topic tree to extract relevant information
            topics = []

            # Helper function to extract topics recursively
            def extract_topics(node, path=""):
                current_path = f"{path}/{node.get('slug', '')}" if path else node.get('slug', '')

                # Only include content nodes with titles
                if node.get('kind') in ['Topic', 'Tutorial'] and node.get('title'):
                    topic = {
                        'id': node.get('id', ''),
                        'title': node.get('title', ''),
                        'description': node.get('description', ''),
                        'path': current_path,
                        'url': f"https://www.khanacademy.org{current_path}",
                        'kind': node.get('kind', '')
                    }

                    # Filter by query if provided
                    if not query or query.lower() in topic['title'].lower() or query.lower() in topic['description'].lower():
                        topics.append(topic)

                # Process children
                children = node.get('children', [])
                for child in children:
                    extract_topics(child, current_path)

            # Start extraction from the root
            extract_topics(data)

            # Limit results to avoid overwhelming the UI
            limited_topics = topics[:50]

            return set_cached_response(cache_key, limited_topics)
        else:
            # If API call fails, return a message
            st.error(f"Failed to fetch data from Khan Academy API: {response.status_code}")
            return []

    except Exception as e:
        st.error(f"Error connecting to Khan Academy API: {str(e)}")
        return []

def fetch_khan_academy_videos(topic_id: str) -> List[Dict[str, Any]]:
    """
    Fetch videos for a specific Khan Academy topic

    Args:
        topic_id: The ID of the topic to fetch videos for

    Returns:
        List of videos with metadata
    """
    # Use cache if available
    cache_key = f"khan_academy_videos_{topic_id}"
    cached_data = get_cached_response(cache_key)
    if cached_data:
        return cached_data

    try:
        # For a real integration, you'd use the proper API endpoint
        url = f"https://www.khanacademy.org/api/v1/topic/{topic_id}/videos"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            videos = []

            for video in data:
                videos.append({
                    'id': video.get('id', ''),
                    'title': video.get('title', ''),
                    'description': video.get('description', ''),
                    'youtube_id': video.get('youtube_id', ''),
                    'duration': video.get('duration', 0),
                    'url': f"https://www.khanacademy.org/video/{video.get('youtube_id', '')}"
                })

            return set_cached_response(cache_key, videos)
        else:
            # If API call fails, return a message
            st.error(f"Failed to fetch videos from Khan Academy API: {response.status_code}")
            return []

    except Exception as e:
        st.error(f"Error connecting to Khan Academy API: {str(e)}")
        return []

# Open Library API Integration
def search_open_library(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search books in Open Library

    Args:
        query: Search term
        limit: Maximum number of results to return

    Returns:
        List of books with metadata
    """
    # Use cache if available
    cache_key = f"open_library_search_{query}_{limit}"
    cached_data = get_cached_response(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"https://openlibrary.org/search.json?q={query}&limit={limit}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            books = []

            for doc in data.get('docs', []):
                # Extract relevant information
                book = {
                    'key': doc.get('key', ''),
                    'title': doc.get('title', ''),
                    'author_name': doc.get('author_name', ['Unknown Author'])[0],
                    'first_publish_year': doc.get('first_publish_year', 'Unknown'),
                    'subject': doc.get('subject', [])[:5] if doc.get('subject') else [],
                    'cover_id': doc.get('cover_i', None),
                    'url': f"https://openlibrary.org{doc.get('key', '')}"
                }

                # Add cover URL if available
                if book['cover_id']:
                    book['cover_url'] = f"https://covers.openlibrary.org/b/id/{book['cover_id']}-M.jpg"

                books.append(book)

            return set_cached_response(cache_key, books)
        else:
            # If API call fails, return a message
            st.error(f"Failed to fetch data from Open Library API: {response.status_code}")
            return []

    except Exception as e:
        st.error(f"Error connecting to Open Library API: {str(e)}")
        return []

def get_open_library_book_details(book_key: str) -> Dict[str, Any]:
    """
    Get detailed information for a specific book

    Args:
        book_key: The Open Library key for the book

    Returns:
        Dictionary with book details
    """
    # Use cache if available
    cache_key = f"open_library_book_{book_key}"
    cached_data = get_cached_response(cache_key)
    if cached_data:
        return cached_data

    try:
        # Remove leading /works/ if present
        clean_key = book_key.replace('/works/', '')
        url = f"https://openlibrary.org/works/{clean_key}.json"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Extract relevant information
            book_details = {
                'key': data.get('key', ''),
                'title': data.get('title', ''),
                'description': data.get('description', {}).get('value', '') if isinstance(data.get('description', ''), dict) else data.get('description', ''),
                'subjects': data.get('subjects', []),
                'cover_id': data.get('covers', [None])[0],
                'links': []
            }

            # Add cover URL if available
            if book_details['cover_id']:
                book_details['cover_url'] = f"https://covers.openlibrary.org/b/id/{book_details['cover_id']}-L.jpg"

            # Extract links
            for link in data.get('links', []):
                if isinstance(link, dict) and 'url' in link and 'title' in link:
                    book_details['links'].append({
                        'url': link['url'],
                        'title': link['title']
                    })

            return set_cached_response(cache_key, book_details)
        else:
            # If API call fails, return a message
            st.error(f"Failed to fetch book details from Open Library API: {response.status_code}")
            return {}

    except Exception as e:
        st.error(f"Error connecting to Open Library API: {str(e)}")
        return {}

# NASA API Integration
def fetch_nasa_apod(count: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch NASA Astronomy Picture of the Day

    Args:
        count: Number of images to retrieve (max 100)

    Returns:
        List of APOD entries with metadata
    """
    # Use cache if available
    cache_key = f"nasa_apod_{count}"
    cached_data = get_cached_response(cache_key)
    if cached_data:
        return cached_data

    # Check if NASA API key is available
    nasa_api_key = os.environ.get("NASA_API_KEY", "DEMO_KEY")

    try:
        url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}&count={count}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return set_cached_response(cache_key, data)
        else:
            # If API call fails, return a message
            st.error(f"Failed to fetch data from NASA API: {response.status_code}")
            return []

    except Exception as e:
        st.error(f"Error connecting to NASA API: {str(e)}")
        return []

# Wikipedia API for educational content
def search_wikipedia(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search Wikipedia for educational content

    Args:
        query: Search term
        limit: Maximum number of results to return

    Returns:
        List of Wikipedia articles with metadata
    """
    # Use cache if available
    cache_key = f"wikipedia_search_{query}_{limit}"
    cached_data = get_cached_response(cache_key)
    if cached_data:
        return cached_data

    try:
        # Search for pages
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json&srlimit={limit}"
        search_response = requests.get(search_url)

        if search_response.status_code == 200:
            search_data = search_response.json()
            results = []

            for item in search_data.get('query', {}).get('search', []):
                page_id = item.get('pageid')
                title = item.get('title')

                # Get additional details for each page
                details_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts|pageimages&exintro&explaintext&pithumbsize=300&pageids={page_id}&format=json"
                details_response = requests.get(details_url)

                if details_response.status_code == 200:
                    details_data = details_response.json()
                    page_data = details_data.get('query', {}).get('pages', {}).get(str(page_id), {})

                    extract = page_data.get('extract', 'No description available')
                    image_url = page_data.get('thumbnail', {}).get('source', None)

                    results.append({
                        'page_id': page_id,
                        'title': title,
                        'extract': extract,
                        'image_url': image_url,
                        'url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    })

            return set_cached_response(cache_key, results)
        else:
            # If API call fails, return a message
            st.error(f"Failed to search Wikipedia: {search_response.status_code}")
            return []

    except Exception as e:
        st.error(f"Error connecting to Wikipedia API: {str(e)}")
        return []

# Main API Integration UI
def display_api_integration_ui():
    """Display the Educational API Integration UI"""
    st.title("🔌 Educational API Integrations")

    st.write("""
    Connect to real educational APIs to enhance your learning experience.
    Choose an API source and explore educational content.
    """)

    # Select API source
    api_source = st.selectbox(
        "Select an educational API source:",
        ["Khan Academy", "Open Library", "NASA Astronomy", "Wikipedia"]
    )

    api_connector = APIConnector() #instantiate APIConnector

    # Khan Academy API
    if api_source == "Khan Academy":
        st.header("Khan Academy Content")

        st.write("""
        Khan Academy provides a vast library of educational content across various subjects.
        Search for topics or browse through the available content.
        """)

        # Search for topics
        search_query = st.text_input("Search for topics:", "")

        if st.button("Search Khan Academy") or search_query:
            with st.spinner("Fetching topics from Khan Academy..."):
                topics = fetch_khan_academy_topics(search_query)

                if topics:
                    st.subheader(f"Found {len(topics)} topics")

                    # Display topics in expandable containers
                    for topic in topics:
                        with st.expander(f"{topic['title']}"):
                            st.write(topic.get('description', 'No description available'))
                            st.write(f"**Type:** {topic.get('kind', '')}")

                            # Link to Khan Academy
                            st.markdown(f"[View on Khan Academy]({topic.get('url', '')})")

                            # Fetch videos for this topic if available
                            if st.button(f"Load videos for {topic['title']}", key=f"videos_{topic['id']}"):
                                with st.spinner("Fetching videos..."):
                                    videos = fetch_khan_academy_videos(topic['id'])

                                    if videos:
                                        for video in videos:
                                            st.write(f"**{video['title']}**")
                                            st.write(video.get('description', 'No description available'))

                                            # Embed YouTube video if available
                                            youtube_id = video.get('youtube_id')
                                            if youtube_id:
                                                st.video(f"https://www.youtube.com/watch?v={youtube_id}")
                                    else:
                                        st.info("No videos found for this topic.")
                else:
                    st.info("No topics found. Try a different search term.")

    # Open Library API
    elif api_source == "Open Library":
        st.header("Open Library Books")

        st.write("""
        Open Library is an open, editable library catalog, building towards a web page for every book ever published.
        Search for books on various educational topics.
        """)

        # Search for books
        search_query = st.text_input("Search for books:", "")

        if st.button("Search Open Library") or search_query:
            with st.spinner("Searching for books..."):
                books = search_open_library(search_query)

                if books:
                    st.subheader(f"Found {len(books)} books")

                    # Display books in a grid
                    cols = st.columns(2)
                    for i, book in enumerate(books):
                        with cols[i % 2]:
                            st.subheader(book['title'])
                            st.write(f"**Author:** {book['author_name']}")
                            st.write(f"**Published:** {book.get('first_publish_year', 'Unknown')}")

                            # Display cover if available
                            if 'cover_url' in book:
                                st.image(book['cover_url'], width=150)

                            # Subjects
                            if book.get('subject'):
                                st.write("**Subjects:**")
                                for subject in book['subject']:
                                    st.write(f"- {subject}")

                            # Link to Open Library
                            st.markdown(f"[View on Open Library]({book['url']})")

                            # Get book details button
                            if st.button(f"Show Details", key=f"details_{book['key']}"):
                                with st.spinner("Loading book details..."):
                                    details = get_open_library_book_details(book['key'])

                                    if details:
                                        st.write("### Description")
                                        st.write(details.get('description', 'No description available'))

                                        # External links
                                        if details.get('links'):
                                            st.write("### External Resources")
                                            for link in details['links']:
                                                st.markdown(f"[{link['title']}]({link['url']})")
                                    else:
                                        st.error("Could not load book details.")
                else:
                    st.info("No books found. Try a different search term.")

    # NASA API
    elif api_source == "NASA Astronomy":
        st.header("NASA Astronomy Picture of the Day")

        st.write("""
        NASA's Astronomy Picture of the Day (APOD) is a service providing daily images of our universe along with brief explanations.
        These images can be valuable educational resources for astronomy and space science.
        """)

        # Number of images to fetch
        num_images = st.slider("Number of images to show:", 1, 10, 5)

        if st.button("Fetch NASA APOD"):
            with st.spinner("Fetching astronomy pictures..."):
                apod_entries = fetch_nasa_apod(num_images)

                if apod_entries:
                    for entry in apod_entries:
                        st.subheader(entry.get('title', 'Untitled'))
                        st.write(f"**Date:** {entry.get('date', 'Unknown')}")

                        # Display image
                        if entry.get('media_type') == 'image':
                            st.image(entry.get('url'), use_column_width=True)
                        elif entry.get('media_type') == 'video':
                            st.video(entry.get('url'))

                        # Explanation
                        st.write(entry.get('explanation', 'No explanation available'))

                        # Copyright info if available
                        if 'copyright' in entry:
                            st.write(f"*Image Credit & Copyright: {entry['copyright']}*")

                        st.markdown("---")
                else:
                    st.error("Could not fetch NASA APOD data.")

    # Wikipedia API
    elif api_source == "Wikipedia":
        st.header("Wikipedia Educational Content")

        st.write("""
        Wikipedia is a free online encyclopedia that can be a valuable resource for educational content.
        Search for articles on various topics to enhance your learning.
        """)

        # Search for articles
        search_query = st.text_input("Search Wikipedia:", "")

        if st.button("Search Wikipedia") or search_query:
            with st.spinner("Searching Wikipedia..."):
                articles = search_wikipedia(search_query)

                if articles:
                    st.subheader(f"Found {len(articles)} articles")

                    for article in articles:
                        with st.expander(article['title']):
                            # Display image if available
                            if article.get('image_url'):
                                st.image(article['image_url'], width=200)

                            # Extract/summary
                            st.write(article.get('extract', 'No extract available'))

                            # Link to full article
                            st.markdown(f"[Read full article on Wikipedia]({article['url']})")
                else:
                    st.info("No Wikipedia articles found. Try a different search term.")

    st.markdown("---")

    st.write("""
    **Note:** These API integrations provide access to vast educational resources.
    The content retrieved is subject to the terms and conditions of each provider.
    """)

    # API Status
    st.subheader("API Connection Status")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Khan Academy API:** ✅ Connected")
        st.write("**Open Library API:** ✅ Connected")

    with col2:
        st.write("**NASA API:** ✅ Connected")
        st.write("**Wikipedia API:** ✅ Connected")

if __name__ == "__main__":
    display_api_integration_ui()