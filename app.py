from flask import Flask, render_template, redirect, request

import numpy, pickle
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from tensorflow.keras import utils, models

model = models.load_model("mushroom_model.h5")

app = Flask(__name__)

columns_to_eliminate = [
    17,
    16,
    6,
    2,       
    0
]

def eliminate_columns(columns):
    global columns_to_eliminate
    for col in columns_to_eliminate:
        columns.pop(col)
    return columns

with open("mushroom_weights.json", "rb") as RF:
    weights = pickle.load(RF)

weights = eliminate_columns(weights)

total_length = 23 - len(columns_to_eliminate)

lengths = [  len(weights[index]) for index in range(total_length) ]

#print(lengths)

#print(weights)

def alertformat(message):
    return "document.addEventListener('DOMContentLoaded', () => { setTimeout(() => {  alert(" + f"{message}" + ");  }, 2500); })"

@app.route("/")
def index():
    return render_template("index.html", edibility = "Poisonous/Edible")

@app.route("/<path:requests>", methods = [ "POST", "GET" ])
def predict(requests = None):
    matrix = numpy.zeros(shape = (total_length)).tolist()
    for i in range(0, total_length, 1):
        #print(i)
        matrix[i] = utils.to_categorical(weights[i][request.args.get(f"v{i}")], num_classes = lengths[i])
    #matrix = numpy.concatenate(tuple([ x for x in matrix ]))
    #print(len(matrix))
    #print(matrix)
    #matrix = numpy.expand_dims(numpy.concatenate(tuple([ x for x in matrix ])), axis = 0)
    _prediction = numpy.array(
        model.predict(
            numpy.expand_dims(
                numpy.concatenate(tuple([ x for x in matrix ])), 
                axis = 0
            )
        )
    )[0]
    index = numpy.argmax(_prediction)
    prediction = "Edible" if (index) else "Poisonous"
    _prediction = round(_prediction[index] * 100, 1)
    #print(len(matrix))
    #print(matrix)
    #print(numpy.array(model.predict(matrix)))
    return render_template("index.html", edibility = prediction, confidence = _prediction, alertFlag = 1)

if __name__ == '__main__':
    app.run()