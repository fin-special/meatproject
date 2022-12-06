
import json


def predict_price(filepath, column):
    meat_sum = 0
    with open(filepath, 'r') as file:
        data = json.load(file)

    for i in range(7):
        meat_sum += data[i][column]
    meat_price = int(meat_sum/7)
    return meat_price
