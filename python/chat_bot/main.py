import numpy as np
import json
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModel

rubert_tokenizer = AutoTokenizer.from_pretrained("rubert_tokenizer")
rubert_model = TFAutoModel.from_pretrained("rubert_model")

with open("answers.json", "r", encoding="UTF-8") as f:
    answers= json.load(f)
with open("questions.json", "r", encoding="UTF-8") as f:
    questions = json.load(f)

dataset = []
for index in range(min(len(questions), len(answers))):
    embedding_question = rubert_model(**rubert_tokenizer(questions[index:index+1], return_tensors='tf',
                                       padding=True, truncation=True))['last_hidden_state'][:, 0, :].numpy()
    embedding_answer = rubert_model(**rubert_tokenizer(answers[index:index+1], return_tensors='tf',
                                       padding=True, truncation=True))['last_hidden_state'][:, 0, :].numpy()
    dataset.append([embedding_question[0], embedding_answer[0]])
dataset = np.array(dataset)
model = tf.keras.models.load_model("Chatbot.keras")

while True:
    question = [input("Ваш вопрос: ")]
    embedding_question = rubert_model(**rubert_tokenizer(question, return_tensors='tf', padding=True, truncation=True))[
        'last_hidden_state'][:, 0, :].numpy()[0]
    p = []

    for i in range(dataset.shape[0]):
        embedding_answer = dataset[i, 1]
        combined_embedding = np.concatenate(
            [embedding_question, embedding_answer])
        prediction = model.predict(np.expand_dims(
            combined_embedding, axis=0), verbose=False)[0, 0]
        p.append([i, prediction])
    p = np.array(p)
    ans = np.argmax(p[:, 1])
    print("Ответ: ", answers[ans])