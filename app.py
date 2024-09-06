from flask import Flask, request, jsonify
from instagrapi import Client
import json

from instagrapi.exceptions import (
    ClientLoginRequired,
    LoginRequired,
    MediaNotFound,
    StoryNotFound,
)

app = Flask(__name__)

def process_instagram_url(sessionId, url):
    response = {}
    try:
        cl = Client()

        if sessionId and sessionId.strip():
            cl.login_by_sessionid(sessionId)

        if "story" in url or "stories" in url:
            if sessionId and sessionId.strip():
                storypk = cl.story_pk_from_url(url)
                try:
                    storyInf = cl.story_info(storypk)
                    response = storyInf.json() 
                except StoryNotFound as snfe:
                    response = {"error": f"Error retrieving story information: {snfe}"}
            else:
                response = {"error": "Error Login Required"}
        elif "highlight" in url or "highlights" in url:
            highlight_pk = cl.highlight_pk_from_url(url)
            try:
                hInfo = cl.highlight_info(highlight_pk)
                response = hInfo.json()
            except:
                response = {"error": f"Error retrieving highlight information"}
        else:
            media_pk = cl.media_pk_from_url(url)
            try:
                mediaInfo = cl.media_info(media_pk)
                response = mediaInfo.json()  # Convert to dictionary
            except MediaNotFound as mnfe:
                response = {"error": f"Error retrieving media information: {mnfe}"}

    except (ClientLoginRequired, LoginRequired) as cle:
        response = {"error": f"Error during login: {cle}"}
    except Exception as e:
        response = {"error": f"An unexpected error occurred: {e}"}
    
    return response

@app.route('/process_instagram_url', methods=['POST'])
def process_instagram_url_api():
    data = request.get_json()  # Get the request body as JSON
    sessionId = data.get('sessionId', "")
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    response = process_instagram_url(sessionId, url)
    return jsonify(response)  # Return the response as JSON

@app.route('/')
def process_instagram_url_api():
    return "server running" 
