from flask import Flask, jsonify, request
from requests_html import HTMLSession

app = Flask(__name__)

def scrape_audio(num_pages):
    try:
        # Create a session using requests-html
        session = HTMLSession()
        all_audio_files = []  # Collect all audio files from all pages

        # Base URL for the site
        base_url = "https://carlislechurch.org/sermons"

        # Loop through the specified number of pages
        for page_num in range(1, num_pages + 1):
            # Construct URL for each page
            url = f"{base_url}/page/{page_num}/" if page_num > 1 else base_url
            response = session.get(url, timeout=10)  # Set a timeout for the request

            try:
                # Render JavaScript only if necessary
                response.html.render(timeout=20, sleep=1)
            except Exception as e:
                print(f"Rendering failed for {url}: {e}")
                continue

            # Debug: Log fetched HTML (optional, remove in production)
            print(f"Fetched HTML for {url}:\n{response.html.html[:500]}")  # Log first 500 characters

            # Find all audio elements (adjust selector as needed)
            audio_elements = response.html.find('audio')  # General selector for <audio> tags
            for audio in audio_elements:
                audio_src = audio.attrs.get('src')
                if audio_src and ".mp3" in audio_src:
                    # Normalize the audio URL
                    audio_url = audio_src if audio_src.startswith('http') else f'https://carlislechurch.org{audio_src}'
                    all_audio_files.append(audio_url)

        session.close()  # Always close the session
        return {"audio_files": all_audio_files}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/scrape-audio', methods=['GET'])
def scrape_audio_endpoint():
    """API endpoint to scrape audio files."""
    if request.method == "GET":
        # Get number of pages to scrape from query parameter 'pages'
        num_pages_to_scrape = request.args.get("pages", default=1, type=int)
        if num_pages_to_scrape < 1:
            return jsonify({"status": "error", "message": "Invalid number of pages."}), 400

        result = scrape_audio(num_pages_to_scrape)
        return jsonify(result)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
