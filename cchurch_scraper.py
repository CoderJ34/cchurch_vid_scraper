from flask import Flask, jsonify, request
from requests_html import HTMLSession

app = Flask(__name__)

def scrape_audio(num_pages):
    try:
        # Use a single session
        session = HTMLSession()
        all_audio_files = []
        base_url = "https://carlislechurch.org/sermons"

        # Loop through pages with a single session
        for i in range(1, num_pages + 1):
            url = f"{base_url}/page/{i}/" if i > 1 else base_url
            response = session.get(url, timeout=10)  # Set timeout
            try:
                # Render JavaScript only if needed
                response.html.render(timeout=20, sleep=2)  
            except Exception as render_error:
                print(f"Render failed for {url}: {render_error}")
                continue

            # Find audio elements
            audio_elements = response.html.find('audio.wp-audio-shortcode')
            for audio in audio_elements:
                audio_src = audio.attrs.get('src')
                if audio_src and ".mp3" in audio_src:
                    # Normalize the URL
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
        # Get the number of pages from query parameters
        num_pages_to_scrape = request.args.get("pages", default=1, type=int)
        if num_pages_to_scrape < 1:
            return jsonify({"status": "error", "message": "Invalid number of pages."}), 400

        result = scrape_audio(num_pages_to_scrape)
        return jsonify(result)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
