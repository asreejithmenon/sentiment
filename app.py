from flask import Flask, request, jsonify
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from google.cloud import storage
import os

nltk.download('vader_lexicon')

app = Flask(__name__)
sia = SentimentIntensityAnalyzer()

def download_nltk_data():
    bucket_name = os.environ.get("BUCKET_NAME")
    if bucket_name:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('nltk_data.zip')
        blob.download_to_filename('/tmp/nltk_data.zip')
        import zipfile
        with zipfile.ZipFile('/tmp/nltk_data.zip', 'r') as zip_ref:
            zip_ref.extractall('/tmp/')
        nltk.data.path.append('/tmp/nltk_data')

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    download_nltk_data()
    text = request.get_json().get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    scores = sia.polarity_scores(text)
    return jsonify(scores)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
