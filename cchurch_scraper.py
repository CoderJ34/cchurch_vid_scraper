from flask import Flask, jsonify, request
from requests_html import AsyncHTMLSession
import asyncio

app = Flask(__name__)

async def scrape_audio_for_pages(pages_to_scrape):
    """Async function to scrape audio for a list of pages."""
    session = AsyncHTMLSession()  # Use AsyncHTMLSession for async requests
    all_audio_files = []

    # Schedule all page requests
    tasks = [session.get(page) for page in pages_to_scrape]
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

    return all_audio_files

async def scrape_audio(num_pages):
    """Async function to scrape audio files across multiple pages."""
    # Generate the list of URLs to scrape
    scraping_urls = ["https://carlislechurch.org/sermons/"]
    scraping_urls += [
        f"https://carlislechurch.org/sermons/page/{i}/" for i in range(2, num_pages + 1)
    ]

    # Split the URLs into chunks of 3 pages
    chunk_size = 3
    chunks = [scraping_urls[i:i + chunk_size] for i in range(0, len(scraping_urls), chunk_size)]

    all_audio_files = []
    for chunk in chunks:
        # Scrape each chunk and collect results
        chunk_results = await scrape_audio_for_pages(chunk)
        all_audio_files.extend(chunk_results)

    return {"audio_files": all_audio_files}

@app.route('/scrape-audio', methods=['GET'])
async def scrape_audio_endpoint():
    """API endpoint to scrape audio files."""
    if request.method == "GET":
        # Get number of pages to scrape from query parameter 'pages'
        num_pages_to_scrape = request.args.get("pages", default=1, type=int)
        result = await scrape_audio(num_pages_to_scrape)
        return jsonify(result)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
