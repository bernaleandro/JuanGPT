import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model, model_from_json
from flask import Flask, render_template, request

chatbot = Flask(__name__)

lemmatizer = WordNetLemmatizer()

intents = json.load(open('models/intents.json'))
words = pickle.load(open('pickle/words.pkl', 'rb'))
classes = pickle.load(open('pickle/classes.pkl', 'rb'))

json_file = open('models/chatbot_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("models/chatbot_model.h5")

# Funciones del chatbot
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
                
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.where(res == np.max(res))[0][0]
    category = classes[max_index]
    
    return category

def get_response(tag, intents_json):
    intents_list = intents_json['intents']
    results = ""
    
    for i in intents_list:
        if i["tag"] == tag:
            results = random.choice(i["responses"])
            break
        
    return results

@chatbot.route('/')
def index():
    return render_template('index.html')

# Manejo del formulario de entrada del usuario
@chatbot.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['user-input']
    intent = predict_class(user_message)
    response = get_response(intent, intents)
    return {'user_message': user_message, 'chatbot_response': response}

if __name__ == '__main__':
    chatbot.run(debug = True)