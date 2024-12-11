import os
from google.cloud import language_v1

def analyze_sentiment(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    sentiment = response.document_sentiment
    return f"Text: {text}, Sentiment score: {sentiment.score}, Magnitude: {sentiment.magnitude}"

if __name__ == "__main__":
    bucket_name = os.getenv("BUCKET_NAME")
    file_name = "sample_data.csv"
    client = language_v1.LanguageServiceClient()

    # Read data from GCS
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()

    lines = content.splitlines()
    for line in lines[1:]:  # Skip header
        print(analyze_sentiment(line))
