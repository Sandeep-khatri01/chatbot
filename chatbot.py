import json
import random
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer

print("Downloading NLTK resources...")
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
print("Downloads complete.")

lemmatizer = WordNetLemmatizer()

with open('E:\\Chatbot\\intents.json') as file:
    data = json.load(file)

training_sentences = []
training_labels = []
labels = []
responses_for_tag = {}

print("Processing data...")

for intent in data['intents']:
    tag = intent['tag']
    if tag not in labels:
        labels.append(tag)

    responses_for_tag[tag] = intent['responses']

    for pattern in intent['patterns']:

        words = nltk.word_tokenize(pattern)
        lemmatized_words = [lemmatizer.lemmatize(w.lower()) for w in words]
        processed_sentence = ' '.join(lemmatized_words)
        
        training_sentences.append(processed_sentence)
        training_labels.append(tag)

print(f"Processed {len(training_sentences)} patterns.")

print("Creating Bag-of-Words and training the model...")

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(training_sentences)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, training_labels)

print("Model trained! The chatbot is now ready.")

def get_bot_response(user_input):
    words = nltk.word_tokenize(user_input)
    lemmatized_words = [lemmatizer.lemmatize(w.lower()) for w in words]
    processed_input = ' '.join(lemmatized_words)

    input_vector = vectorizer.transform([processed_input])

    predicted_tag = model.predict(input_vector)[0]
    
    probabilities = model.predict_proba(input_vector)
    confidence = np.max(probabilities)

    CONFIDENCE_THRESHOLD = 0.4
    
    if confidence > CONFIDENCE_THRESHOLD:
        response = random.choice(responses_for_tag[predicted_tag])
    else:
        response = "I'm sorry, I don't understand that. Can you rephrase? I can help with admissions, courses, fees, and timings."
        
    return response

print("\n--- College Support Chatbot ---")
print("Type 'quit' to exit.")

while True:
    user_input = input("> You: ")
    if user_input.lower() == 'quit':
        print("> Bot: Goodbye! We wish you the best in your studies.")
        break
    
    bot_response = get_bot_response(user_input)
    print(f"> Bot: {bot_response}")