import random # Para respuestas aleatorias
import json 
import pickle # Archivos que se puedan guardar
import numpy as np # Data science

# Para procesar un lenguaje natural
import nltk
from nltk.stem import WordNetLemmatizer 

# Para crear un modelo de red neuronal
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import legacy

lemmantizer = WordNetLemmatizer()
intents = json.loads(open('models/intents.json').read())

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Creamos listas
words = [] 
classes = [] 
documents = [] # Almacena las palabras y sus patrones
ignore_letters = ['?', '¿', ',', '.', '!', '¡']

# Creamos un bucle para que lea las listas de models/intents.json
for intent in intents['intents']:
    for pattern in intent["patterns"]:
        # Tokenizamos el patron: comprende el lenguaje natural
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list) # Agregamos las palabras a la lista 
        documents.append((word_list, intent['tag'])) # Agregamos la lista de palabras junto a su identificador
        
        # Si no se agrego el identificador que lo haga
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            
# Modificamos la palabra a su forma canonica para evitar condusiones y lograr una busqueda mas profunda
words = [lemmantizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

pickle.dump(words, open('pickle/words.pkl', 'wb'))
pickle.dump(classes, open('pickle/classes.pkl', 'wb'))

# Creamos lista para entrenamiento
training = []
output_empty = [0]*len(classes)

# Creamos un bucle por todos los patrones que queremos que reconozca
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmantizer.lemmatize(word.lower()) for word in word_patterns]
    
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0) # 1: la palabra pertence al patron. 0: no pertence al patron
    
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
    
random.shuffle(training)
training = np.array(training, dtype=object)
print(training)

# Uso dos variables para entrenar a la IA
train_x = list(training[:,0])
train_y = list(training[:,1])

# Aplicamos las capas
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation = 'softmax'))

sgd = legacy.SGD(learning_rate = 0.001, decay = 1e-6, momentum = 0.9, nesterov = True)

model.compile(loss = 'categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])
train_process = model.fit(np.array(train_x), np.array(train_y), epochs = 100, batch_size = 5, verbose = 1)
model.save("models/chatbot_model.h5", train_process)
model_json = model.to_json()

with open("models/chatbot_model.json", "w") as json_file:

    json_file.write(model_json)

# serialize weights to HDF5

model.save_weights("models/chatbot_model.h5")

print("Saved model to disk")

"""
model.compile(loss = 'categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])
train_process = model.fit(np.array(train_x), np.array(train_y), epochs = 100, batch_size = 5, verbose = 1)
model.save("chatbot_model.h5", train_process)
"""