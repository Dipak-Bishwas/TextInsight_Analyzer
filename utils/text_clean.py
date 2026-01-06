# utils/text_clean.py

import re
import spacy
import subprocess
import sys

# Load spaCy model safely once
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Download the model if not found
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    """
    Basic text cleaning: lowercase, remove URLs, HTML tags, emails, punctuation, hashtags, mentions, 
    repeated characters, non-ASCII, extra spaces.
    """
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)  # Remove URLs
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'\S+@\S+\.\S+', '', text)  # Remove emails
    text = re.sub(r'#', '', text)  # Remove hashtags
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII
    text = re.sub(r'[^a-z\s]', '', text)  # Remove special characters and punctuation
    text = re.sub(r'(.)\1{2,}', r'\1', text)  # Reduce repeated characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

def clean_text_spacy(text: str) -> list[str]:
    """
    Use spaCy to tokenize and lemmatize text, removing stopwords and punctuations.
    """
    doc = nlp(text)
    words = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return words
