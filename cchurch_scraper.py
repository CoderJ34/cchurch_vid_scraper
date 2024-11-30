from flask import Flask, jsonify, request
from requests_html import HTMLSession

app = Flask(__name__)

def scrape_audio(num_pages):
    try:
        # Create a session using requests-html
        session = HTMLSession()
        all_audio_files = []  # Collect all audio files from all pages
        
        # List of URLs to scrape
        scraping_urls = ["https://carlislechurch.org/sermons/"]
        
        # Generate URLs for additional pages
        for i in range(2, (1 + num_pages)):  # start from page 2
            new_scraping_url = f"https://carlislechurch.org/sermons/page/{i}/"
            scraping_urls.append(new_scraping_url)

        # Loop through all pages
        for cur_scraping_url in scraping_urls:
            response = session.get(cur_scraping_url)
            # Render JavaScript (if necessary)
            response.html.render()

            # Find all audio elements with the class 'wp-audio-shortcode'
            audio_elements = response.html.find('audio.wp-audio-shortcode')
            
            # Extract and normalize the audio URLs
            for audio in audio_elements:
                audio_src = audio.attrs.get('src')
                if audio_src and ".mp3" in audio_src:
                    # Normalize the audio URL
                    audio_url = audio_src if audio_src.startswith('http') else f'https://carlislechurch.org{audio_src}'
                    all_audio_files.append(audio_url)

        return {"audio_files": all_audio_files}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/scrape-audio', methods=['GET'])
def scrape_audio_endpoint():
    """API endpoint to scrape audio files."""
    if request.method == "GET":
        # Get number of pages to scrape from query parameter 'pages'
        num_pages_to_scrape = request.args.get("pages", default=1, type=int)
        result = scrape_audio(num_pages_to_scrape)
        return jsonify(result)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
