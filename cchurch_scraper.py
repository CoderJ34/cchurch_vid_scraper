from flask import Flask, jsonify, request
from requests_html import AsyncHTMLSession
import asyncio
import threading

app = Flask(__name__)

async def scrape_audio_for_pages_async(pages_to_scrape, all_audio_files):
    """Async function to scrape audio for a list of pages."""
    session = AsyncHTMLSession()  # Use AsyncHTMLSession for async requests

    tasks = []
    for page in pages_to_scrape:
        tasks.append(session.get(page))  # Schedule all page requests

    responses = await asyncio.gather(*tasks)  # Wait for all requests to complete

    for response in responses:
        await response.html.arender()  # Render JavaScript asynchronously
        audio_elements = response.html.find('audio.wp-audio-shortcode')

        # Extract and normalize the audio URLs
        for audio in audio_elements:
            audio_src = audio.attrs.get('src')
            if audio_src and ".mp3" in audio_src:
                audio_url = audio_src if audio_src.startswith('http') else f'https://carlislechurch.org{audio_src}'
                all_audio_files.append(audio_url)

def scrape_audio_for_pages(pages_to_scrape, all_audio_files):
    """Wrapper to run the async function in a thread."""
    asyncio.run(scrape_audio_for_pages_async(pages_to_scrape, all_audio_files))

def scrape_audio(num_pages):
    try:
        all_audio_files = []  # Collect all audio files from all pages
        
        # List of URLs to scrape
        scraping_urls = ["https://carlislechurch.org/sermons/"]
        
        # Generate URLs for additional pages
        for i in range(2, num_pages + 1):
            new_scraping_url = f"https://carlislechurch.org/sermons/page/{i}/"
            scraping_urls.append(new_scraping_url)

        # Split the URLs into chunks of 3 pages
        chunk_size = 3
        chunks = [scraping_urls[i:i + chunk_size] for i in range(0, len(scraping_urls), chunk_size)]

        # Create threads for each chunk of pages
        threads = []
        for chunk in chunks:
            thread = threading.Thread(target=scrape_audio_for_pages, args=(chunk, all_audio_files))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

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
