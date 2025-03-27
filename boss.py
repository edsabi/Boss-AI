# app.py

from flask import Flask, render_template, request, jsonify
import openai
import re
import requests

# Load OpenAI API key
with open('file.txt','r') as f:
    openai.api_key = f.read().strip()

app = Flask(__name__)

# Giphy config
GIPHY_API_KEY = ""
GIPHY_ENDPOINT = "https://api.giphy.com/v1/gifs/random"

# AI completion function
def get_completion(prompt, model="gpt-4-turbo"):
    with open('ai_config2', 'r') as f:
        ai_config2 = f.read()
    with open('ai_config3', 'r') as f:
        ai_config3 = f.read()

    system_prompt = f"{ai_config2}\n{ai_config3}"

    message_stack = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=message_stack,
        temperature=1,
    )

    return response.choices[0].message["content"]

# Extract first hashtag from a message
def extract_hashtag(text):
    match = re.search(r"#(\w+)", text)
    return match.group(1) if match else None

# Call Giphy API with the tag
def get_gif_url_for_tag(tag):
    params = {
        "api_key": GIPHY_API_KEY,
        "tag": tag,
        "rating": "g"
    }
    response = requests.get(GIPHY_ENDPOINT, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["data"]["images"]["original"]["url"]
    return None

@app.route("/")
def home():
    return render_template("index3.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    with open("Chatlogs", "a") as i:
        i.write(userText + '\n')

    ai_response = get_completion(userText)

    with open("Chatlogs", "a") as i:
        i.write('\n' + ai_response + '\n')

    tag = extract_hashtag(ai_response)
    gif_url = get_gif_url_for_tag(tag) if tag else None

    return jsonify({
        "text": ai_response,
        "gif": gif_url
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=50054)
