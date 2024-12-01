from flask import Flask, jsonify, request
from requests_html import HTMLSession
import threading
import time

app = Flask(__name__)

def fetch_page(session, url, audio_files, lock):
    try:
        response = session.get(url, timeout=10)  # Set timeout for each page
        try:
            # Render JavaScript if needed
            response.html.render(timeout=20, sleep=1)
        except Exception as e:
            print(f"Rendering failed for {url}: {e}")

        # Find audio elements
        audio_elements = response.html.find('audio.wp-audio-shortcode')
        with lock:  # Use a lock to safely append to shared list
            for audio in audio_elements:
                audio_src = audio.attrs.get('src')
                if audio_src and ".mp3" in audio_src:
                    audio_url = audio_src if audio_src.startswith('http') else f'https://carlislechurch.org{audio_src}'
                    audio_files.append(audio_url)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

def scrape_audio(num_pages):
    try:
        session = HTMLSession()
        base_url = "https://carlislechurch.org/sermons"
        audio_files = []
        lock = threading.Lock()  # Lock for thread safety

        threads = []
        for i in range(1, num_pages + 1):
            url = f"{base_url}/page/{i}/" if i > 1 else base_url
            thread = threading.Thread(target=fetch_page, args=(session, url, audio_files, lock))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        session.close()  # Properly close the session
        return {"audio_files": audio_files}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/scrape-audio', methods=['GET'])
def scrape_audio_endpoint():
    """API endpoint to scrape audio files."""
    if request.method == "GET":
        num_pages_to_scrape = request.args.get("pages", default=1, type=int)
        if num_pages_to_scrape < 1:
            return jsonify({"status": "error", "message": "Invalid number of pages."}), 400

        result = scrape_audio(num_pages_to_scrape)
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
