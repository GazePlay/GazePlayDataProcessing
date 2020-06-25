import json


def readJsonDataFromFile(file):
    f = open(file, )
    data = getCoordinatesFromJsonFile(f)
    # Closing file
    f.close()
    return data


def getCoordinatesFromJsonFile(file):
    data = json.load(file)
    coordinates = data["coordinates"]
    return coordinates
