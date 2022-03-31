import nltk
import random
import numpy as np
import json
import pickle
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model


class ChatBot():

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.words = pickle.load(open('./medi_bot_api/chatbot/words.pkl', 'rb'))
        self.classes = pickle.load(open('./medi_bot_api/chatbot/classes.pkl', 'rb'))
        self.model = load_model('./medi_bot_api/chatbot/chatbotmodel.h5')
        self.json_file = open('./medi_bot_api/chatbot/intents.json')
        self.intents = json.load(self.json_file)

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []

        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
        return return_list

    def get_response(self, intents_list, intents_json):
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']

        # print(tag)

        result = 'N/A'

        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result

# while True:
#     message = input("")
#
#     chat_bot = ChatBot()
#
#     ints = chat_bot.predict_class(message)
#     # print('predicted: ', ints)
#     res = chat_bot.get_response(ints, chat_bot.intents)
#     print(res)