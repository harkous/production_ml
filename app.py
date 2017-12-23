from flask import Flask
from flask import request
from keras.models import load_model
from keras.datasets import reuters
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from flask import jsonify
import os

MODEL_DIR = './models'

max_words = 1000

app = Flask(__name__)

print("Loading model")
model = load_model(os.path.join(MODEL_DIR, 'reuters_model.hdf5'))
# we need the word index to map words to indices
word_index = reuters.get_word_index()
tokenizer = Tokenizer(num_words=max_words)


def preprocess_text(text):
    word_sequence = text_to_word_sequence(text)
    indices_sequence = [[word_index[word] if word in word_index else 0 for word in word_sequence]]
    x = tokenizer.sequences_to_matrix(indices_sequence, mode='binary')
    return x


@app.route('/predict', methods=['GET'])
def predict():
    try:
        text = request.args.get('text')
        x = preprocess_text(text)
        y = model.predict(x)
        predicted_class = y[0].argmax(axis=-1)
        print(predicted_class)
        return jsonify({'prediction': str(predicted_class)})
    except:
        response = jsonify({'error': 'problem predicting'})
        response.status_code = 400
        return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4444)
