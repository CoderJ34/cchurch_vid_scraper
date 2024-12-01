from flask import Flask, jsonify, request
from requests_html import AsyncHTMLSession
import asyncio

app = Flask(__name__)

async def fetch_audio_urls(pages):
    """Fetch audio URLs asynchronously from a list of pages."""
    session = AsyncHTMLSession()  # Use AsyncHTMLSession
    tasks = [session.get(page) for page in pages]  # Schedule all requests
    responses = await asyncio.gather(*tasks)  # Wait for all responses

    all_audio_files = []
    for response in responses:
        await response.html.arender()  # Render JavaScript content
        audio_elements = response.html.find('audio.wp-audio-shortcode')

        # Extract and normalize audio URLs
        for audio in audio_elements:
            audio_src = audio.attrs.get('src')
            if audio_src and ".mp3" in audio_src:
                audio_url = audio_src if audio_src.startswith('http') else f'https://carlislechurch.org{audio_src}'
                all_audio_files.append(audio_url)
    return all_audio_files

async def scrape_audio(num_pages):
    """Scrape audio files from multiple pages asynchronously."""
    # Generate the list of URLs to scrape
    scraping_urls = ["https://carlislechurch.org/sermons/"]
    scraping_urls += [
        f"https://carlislechurch.org/sermons/page/{i}/" for i in range(2, num_pages + 1)
    ]

    # Split URLs into chunks of 3
    chunk_size = 3
    chunks = [scraping_urls[i:i + chunk_size] for i in range(0, len(scraping_urls), chunk_size)]

    all_audio_files = []
    for chunk in chunks:
        chunk_results = await fetch_audio_urls(chunk)  # Fetch audio URLs for the current chunk
        all_audio_files.extend(chunk_results)

    return {"audio_files": all_audio_files}

@app.route('/scrape-audio', methods=['GET'])
async def scrape_audio_endpoint():
    """API endpoint to scrape audio files."""
    if request.method == "GET":
        num_pages_to_scrape = request.args.get("pages", default=1, type=int)
        result = await scrape_audio(num_pages_to_scrape)
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
