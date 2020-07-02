import json
import math
from itertools import groupby


def readConfig(file):
    file = open(file, )
    data = getVelocityThreshold(file)
    # Closing file
    file.close()
    return data


def readJsonDataFromFile(file):
    f = open(file, )
    data = getCoordinatesFromJsonFile(f)
    # Closing file
    f.close()
    return data


def getVelocityThreshold(file):
    data = json.load(file)
    velocityThreshold = data["velocity_threshold"]
    return velocityThreshold


def getCoordinatesFromJsonFile(file):
    data = json.load(file)
    coordinates = data["CoordinatesAndTimeStamp"]
    return coordinates


def restructureCoordinatesFormat(coordinates):
    coord = []
    for element in coordinates:
        x = element["X"]
        y = element["Y"]
        time = element["time"]
        coord.append((x, y, time))
    return coord


def groupCoordX(coordinates):
    coordX = []
    for element in coordinates:
        x = element["X"]
        coordX.append(x)
    return coordX


def groupCoordY(coordinates):
    coordY = []
    for element in coordinates:
        y = element["Y"]
        coordY.append(y)
    return coordY


def computeDistance(coordinates):
    data = []
    for i in range(len(coordinates) - 1):
        distanceX = coordinates[i + 1][0] - coordinates[i][0]
        distanceY = coordinates[i + 1][1] - coordinates[i][1]
        rad = math.atan2(distanceY, distanceX)
        degree = rad * (180 / math.pi)

        time = coordinates[i + 1][2] - coordinates[i][2]
        timeInSeconds = time * math.pow(10, -3)
        data.append((degree, timeInSeconds))

    return data


def computeVelocity(data):
    velocities = []
    for i in range(len(data) - 1):
        if data[i][1] != 0:
            time = data[i][1]
            distance = data[i][0]
            velocity = abs(distance) / time
        else:
            velocity = 0.0
        velocities.append(velocity)
    return velocities


def ivtClassifier(data, velocityThreshold):
    classification = []
    for i in range(len(data) - 1):
        if data[i] <= velocityThreshold:
            classification.append((i, 1))
        else:
            classification.append((i, 0))
    return classification


def centroidOfFixation(coordX):
    centroid = []
    for i in range(len(coordX) - 1):
        temp = sum(coordX[i]) / len(coordX), sum(coordX[i + 1]) / len(coordX)
        centroid.append(temp)
    return centroid


def groupConsecutiveFixation(data):
    """
     Collapse consecutive fixation points into fixation groups, remove saccade
    :param data: list of classified coordinates
    :return: list of fixation groups
    """

    fixationGroups = []
    for i in data:
        if i[1] == 1:
            fixationGroups.append(i)
    # res = [list(group) for item, group in groupby(data)]
    # fixationGroups = [i for i in res if i[0] == 1]
    return fixationGroups


# def getFixation(data, consecutiveFixations):
  #  print(len(consecutiveFixations[0]))
