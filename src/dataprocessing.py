import json
import math


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


def restructureCoordinatesFormatWithoutTime(coordinates):
    coord = []
    for element in coordinates:
        x = element["X"]
        y = element["Y"]
        coord.append((x, y))
    return coord


def groupCoordX(coordinates):
    coordX = []
    for element in coordinates:
        x = element[0]
        coordX.append(x)
    return coordX


def groupCoordY(coordinates):
    coordY = []
    for element in coordinates:
        y = element[1]
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


def centroidOfFixation(data):
    centroid = []
    for element in data:
        temp = sum(element[0]) / len(element[0]), sum(element[1]) / len(element[1])
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
    return fixationGroups


def mapCoordinatesToFixationGroups(data, consecutiveFixations):
    temp = []
    for index in range(len(data) - 1):
        for i in consecutiveFixations:
            if i[0] == index:
                temp.append((index, data[index]))

    res = list(groupConsecutiveFixationCoord(temp, 2))
    return res


def groupConsecutiveFixationCoord(li, maxgap):
    out = []
    last = li[0][0]
    for x in li:
        if x[0] - last > maxgap:
            yield out
            out = []
        out.append(x[1])
        last = x[0]
    yield out


def separateXAndYCoord(data):
    res = []
    for i in range(len(data) - 1):
        coordX = groupCoordX(data[i])
        coordY = groupCoordY(data[i])
        res.append((coordX, coordY))
    return res
