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

    # Debugging: Print bucket and file name
    print(f"Bucket: {bucket_name}, File: {file_name}")
    
    # Initialize the Google Cloud Storage client
    storage_client = storage.Client()

    # Try to get the bucket and handle errors
    try:
        bucket = storage_client.get_bucket(bucket_name)
        print(f"Successfully accessed the bucket: {bucket_name}")
    except Exception as e:
        print(f"Error accessing bucket: {e}")
        raise

    blob = bucket.blob(file_name)

    # Debugging: Print the blob object
    print(f"Blob object: {blob}")

    # Download the content of the CSV file as text
    try:
        content = blob.download_as_text()
        print(f"File content downloaded successfully.")
    except Exception as e:
        print(f"Error downloading file: {e}")
        raise

    # Process the content (skip the header line)
    lines = content.splitlines()
    for line in lines[1:]:  # Skip the header
        print(analyze_sentiment(line))
