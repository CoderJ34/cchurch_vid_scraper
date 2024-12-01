from flask import Flask, jsonify, request
from requests_html import HTMLSession

app = Flask(__name__)

def scrape_audio(pages):
    try:
        # Create a session using requests-html
        session = HTMLSession()
        all_audio_files = []  # Collect all audio files from all pages
        
        # Validate and process the input 'pages'
        if isinstance(pages, list):
            page_numbers = pages
        elif isinstance(pages, int):
            page_numbers = list(range(1, pages + 1))
        else:
            raise ValueError("Invalid 'pages' input. Must be an integer or a list of integers.")

        # Segment pages into chunks of 3 if there are more than 3 pages
        for i in range(0, len(page_numbers), 3):
            chunk = page_numbers[i:i + 3]
            for page in chunk:
                # Generate the URL for the current page
                if page == 1:
                    cur_scraping_url = "https://carlislechurch.org/sermons/"
                else:
                    cur_scraping_url = f"https://carlislechurch.org/sermons/page/{page}/"
                
                # Fetch and parse the page
                response = session.get(cur_scraping_url)
                response.html.render()  # Render JavaScript if needed

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
        # Get 'pages' parameter: can be an int or a list of ints
        pages = request.args.get("pages", default="1", type=str)
        try:
            # Parse pages input
            if pages.isdigit():
                pages = int(pages)
            else:
                pages = eval(pages)  # Unsafe for untrusted inputs, use ast.literal_eval for security
            result = scrape_audio(pages)
            return jsonify(result)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
