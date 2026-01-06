import re
import spacy
import subprocess
import sys

# Load spaCy model safely once
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = text.lower()   # Lowercase
    text = re.sub(r'http\S+|www\S+|https\S+', '', text) # URL removal
    text = re.sub(r'<.*?>', '', text) # HTML tags
    text = re.sub(r'[^a-z\s]', '', text) # Special characters
    text = re.sub(r'\s+', ' ', text).strip() # Extra spaces
    text = re.sub(r'\S+@\S+\.\S+', '', text) # Email removal
    text = re.sub(r'[^\w\s]', '', text) # Punctuation
    text = re.sub(r'(.)\1{2,}', r'\1', text) # Repeated characters
    text = re.sub(r'#', '', text) # Hashtags
    text = re.sub(r'@\w+', '', text) # Mentions
    text = re.sub(r'[^\x00-\x7F]+', '', text) # Non-ASCII characters
    return text

def clean_text_spacy(text):
    # Use the pre-loaded nlp object
    doc = nlp(text)
    words = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return words
