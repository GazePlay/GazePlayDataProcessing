import src.dataprocessing as helper
import matplotlib.pyplot as plt
import PyGazeAnalyser.pygazeanalyser.detectors as pygazeanalyser
import numpy as np


def defineDataFile():
    data = helper.readJsonDataFromFile('data/data-bubble.json')
    return data


def pyGazeClassifierFixation(data):
    coordWithTime = helper.restructureCoordinatesFormat(data)
    coordWithoutTime = helper.restructureCoordinatesFormatWithoutTime(data)
    coordX = helper.groupCoordX(coordWithoutTime)
    coordY = helper.groupCoordY(coordWithoutTime)
    time = helper.groupTime(coordWithTime)
    arrX = np.array(coordX)
    arrY = np.array(coordY)
    arrTime = np.array(time)
    fixation = pygazeanalyser.fixation_detection(arrX, arrY, arrTime)
    return fixation


def pyGazeClassifierSaccade(data):
    coordWithTime = helper.restructureCoordinatesFormat(data)
    coordWithoutTime = helper.restructureCoordinatesFormatWithoutTime(data)
    coordX = helper.groupCoordX(coordWithoutTime)
    coordY = helper.groupCoordY(coordWithoutTime)
    time = helper.groupTime(coordWithTime)
    arrX = np.array(coordX)
    arrY = np.array(coordY)
    arrTime = np.array(time)
    saccadicCoordinates = pygazeanalyser.saccade_detection(arrX, arrY, arrTime)
    return saccadicCoordinates


def preProcessData(data):
    velocityThreshold = helper.readConfig('config/config.json')
    coordWithTime = helper.restructureCoordinatesFormat(data)
    coordWithoutTime = helper.restructureCoordinatesFormatWithoutTime(data)
    print("velocityThreshold: ", velocityThreshold)
    print("coordinates: ", coordWithTime)
    return velocityThreshold, coordWithTime, coordWithoutTime


def displayGraphs(saccadePygazeX, originalCoord, fixation, fixationPyGaze, saccade):
    plt.subplot(2, 3, 1)
    coordX = helper.groupCoordX(originalCoord)
    coordY = helper.groupCoordY(originalCoord)
    plt.scatter(coordX, coordY)
    plt.title("Original Coord")
    plt.tight_layout()

    plt.subplot(2, 3, 2)
    coordEndX = helper.groupCoordX(saccadePygazeX)
    coordEndY = helper.groupCoordY(saccadePygazeX)
    plt.scatter(coordEndX, coordEndY)
    plt.title("PyGaze Saccade")
    plt.tight_layout()

    plt.subplot(2, 3, 3)
    saccadeX = helper.groupCoordX(saccade)
    saccadeY = helper.groupCoordY(saccade)
    plt.scatter(saccadeX, saccadeY)
    plt.title("Saccade")
    plt.tight_layout()

    plt.subplot(2, 3, 4)
    groupFixationX = helper.groupCoordX(fixationPyGaze)
    groupFixationY = helper.groupCoordY(fixationPyGaze)
    plt.scatter(groupFixationX, groupFixationY)
    plt.title("Fixation PyGaze")
    plt.tight_layout()

    plt.subplot(2, 3, 5)
    groupFixationX = helper.groupCoordX(fixation)
    groupFixationY = helper.groupCoordY(fixation)
    plt.scatter(groupFixationX, groupFixationY)
    plt.title("Fixation Maxgap 35")
    plt.tight_layout()

    plt.show()


def processData(velocityThreshold, coordWithTime):
    distance = helper.computeDistance(coordWithTime)
    velocities = helper.computeVelocity(distance)
    classifiedCoord = helper.ivtClassifier(velocities, velocityThreshold)
    fixationGroups = list(helper.groupConsecutiveFixation(classifiedCoord))
    distanceBetweenFixations = helper.getDistanceBetweenFixationPoints(fixationGroups)
    restructureData = helper.separateXAndYCoord(distanceBetweenFixations)
    fixation = helper.centroidOfFixation(restructureData)
    saccadicPoints = helper.groupSaccadicPoints(classifiedCoord)

    print("distance: ", distance)
    print("velocities: ", velocities)
    print("classified Coord: ", classifiedCoord)
    print("fixation groups: ", str(fixationGroups))
    print("Saccades : ", str(saccadicPoints))
    print("res: ", fixation)
    print("distance between fixations: ", distanceBetweenFixations)
    return fixation, saccadicPoints


def exctractFixationFromPyGazeClassifier(efix):
    fixationPyGaze = []
    for i in range(len(efix) - 1):
        fixationPyGaze.append((efix[i][3], efix[i][4]))
    return fixationPyGaze


def extractSaccadeFromPyGazeClassifier(esac):
    saccadePyGazeX = []
    for i in range(len(esac) - 1):
        saccadePyGazeX.append((esac[i][5], esac[i][6]))
    return saccadePyGazeX


def main():
    data = defineDataFile()
    velocityThreshold, coordWithTime, coordWithoutTime = preProcessData(data)
    fixation, saccade = processData(velocityThreshold, coordWithTime)
    sfix, efix = pyGazeClassifierFixation(data)
    ssac, esac = pyGazeClassifierSaccade(data)
    fixationPyGaze = exctractFixationFromPyGazeClassifier(efix)
    saccadePyGazeX = extractSaccadeFromPyGazeClassifier(esac)

    displayGraphs(saccadePyGazeX, coordWithoutTime, fixation, fixationPyGaze, saccade)


if __name__ == '__main__':
    main()  # main function keeps variables locally scoped
