import os
from google.cloud import language_v1
from google.cloud import storage

def analyze_sentiment(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    sentiment = response.document_sentiment
    return f"Text: {text}, Sentiment score: {sentiment.score}, Magnitude: {sentiment.magnitude}"

if __name__ == "__main__":
    # Set the bucket name and file name directly
    bucket_name = "sent-anal-bucket"
    file_name = "sample.csv"
    
    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    # Download the content of the CSV file as text
    content = blob.download_as_text()
    
    # Process the content (skip the header line)
    lines = content.splitlines()
    for line in lines[1:]:  # Skip the header
        print(analyze_sentiment(line))

