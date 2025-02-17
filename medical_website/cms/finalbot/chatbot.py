import json
import random
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK resources
nltk.download("punkt")

# Load intents from JSON
with open("cms/finalbot/intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)

# Extract training data from intents
patterns = []
tags = []
responses = {}

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(pattern)
        tags.append(intent["tag"])
    responses[intent["tag"]] = intent["responses"]

# Convert text to vector representation
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(patterns)

def get_response(user_input):
    """Match user input with the best intent using cosine similarity."""
    user_vector = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vector, X)
    
    best_match = similarities.argmax()
    
    # If similarity score is high enough, return the matched response
    if similarities[0, best_match] > 0.2:  # Confidence threshold
        tag = tags[best_match]
        return random.choice(responses[tag])
    
    return "I'm sorry, I don't understand."