from flask import Flask, render_template, request
from google.cloud import language_v1

app = Flask(__name__)

def analyze_sentiment(text):
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_sentiment(document=document)
    sentiment = response.document_sentiment

    return sentiment.score, sentiment.magnitude

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        # Use a library like `requests` to fetch the text content from the URL
        import requests
        response = requests.get(url)
        text = response.text

        sentiment_score, sentiment_magnitude = analyze_sentiment(text)
        return render_template('index.html', sentiment_score=sentiment_score, sentiment_magnitude=sentiment_magnitude)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
