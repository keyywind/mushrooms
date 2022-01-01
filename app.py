from flask import Flask, render_template, redirect, request

import numpy, pickle

from tensorflow.keras import utils, models

model = models.load_model("mushroom_model.h5")

app = Flask(__name__)

with open("mushroom_weights.json", "rb") as RF:
    weights = pickle.load(RF)

weights.pop(0)

weights.pop(15)

lengths = [  len(weights[index]) for index in range(21) ]

print(lengths)

print(weights)

def alertformat(message):
    return "document.addEventListener('DOMContentLoaded', () => { setTimeout(() => {  alert(" + f"{message}" + ");  }, 2500); })"

@app.route("/")
def index():
    return render_template("index.html", edibility = "Poisonous/Edible")

@app.route("/request/", methods = [ "POST", "GET" ])
def predict():
    matrix = numpy.zeros(shape = (21)).tolist()
    for i in range(0, 21, 1):
        print(i)
        matrix[i] = utils.to_categorical(weights[i][request.args.get(f"v{i}")], num_classes = lengths[i])
    #matrix = numpy.concatenate(tuple([ x for x in matrix ]))
    #print(len(matrix))
    #print(matrix)
    #matrix = numpy.expand_dims(numpy.concatenate(tuple([ x for x in matrix ])), axis = 0)
    prediction = numpy.argmax(
        numpy.array(
            model.predict(
                numpy.expand_dims(
                    numpy.concatenate(tuple([ x for x in matrix ])), 
                    axis = 0
                )
            )
        )[0]
    )
    prediction = "Edible" if (prediction) else "Poisonous"
    #print(len(matrix))
    #print(matrix)
    #print(numpy.array(model.predict(matrix)))
    return render_template("index.html", edibility = prediction, alertFlag = 1)
    
app.run()