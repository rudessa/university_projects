from transformers import AutoTokenizer, TFAutoModel
import numpy as np
import tensorflow as tf
import json

with open("questions.json", "r", encoding="UTF-8") as f:
    questions = json.load(f)

with open("answers.json", "r", encoding="UTF-8") as f:
    answers = json.load(f)

rubert_tokenizer = AutoTokenizer.from_pretrained("rubert_tokenizer")
rubert_model = TFAutoModel.from_pretrained("rubert_model")

dataset = []
for index in range(min(len(questions), len(answers))):
    question_embedding = rubert_model(**rubert_tokenizer(questions[index:index+1], return_tensors='tf',
                                       padding=True, truncation=True))['last_hidden_state'][:, 0, :].numpy()
    answer_embedding = rubert_model(**rubert_tokenizer(answers[index:index+1], return_tensors='tf',
                                       padding=True, truncation=True))['last_hidden_state'][:, 0, :].numpy()
    dataset.append([question_embedding[0], answer_embedding[0]])
dataset = np.array(dataset)

X, Y = [], []
for i in range(dataset.shape[0]):
    for j in range(dataset.shape[0]):
        X.append(np.concatenate([dataset[i, 0, :], dataset[j, 1, :]], axis=0))
        Y.append(1 if i == j else 0)
X = np.array(X)
Y = np.array(Y)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.InputLayer(input_shape=(X.shape[1],)))
model.add(tf.keras.layers.Dense(100, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), loss='binary_crossentropy',
              metrics=[tf.keras.metrics.AUC(curve='pr', name='auc')])
model.fit(X, Y, epochs=1000, class_weight={0: 1, 1: np.sqrt(Y.shape[0])-1})
model.save("Chatbot.keras")