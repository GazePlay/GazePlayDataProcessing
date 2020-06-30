import json
import math
import more_itertools as mit


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


def classifyVelocities(data, velocityThreshold):
    fixation = []
    saccade = []
    for i in range(len(data) - 1):
        if data[i] < velocityThreshold:
            fixation.append(data[i])
        else:
            saccade.append(data[i])
    return fixation


def groupConsecutiveFixation(iterable):
    """Yield range of consecutive numbers."""
    for group in mit.consecutive_groups(iterable):
        group = list(group)
        if len(group) == 1:
            yield group[0]
        else:
            yield group[0], group[-1]
