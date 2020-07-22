import src.dataprocessing as helper
import matplotlib.pyplot as plt
import PyGazeAnalyser.pygazeanalyser.detectors as pygazeanalyser
import numpy as np


def pyGazeClassifier():
    data = helper.readJsonDataFromFile('data/memory-data.json')
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


def preProcessData():
    data = helper.readJsonDataFromFile('data/memory-data.json')
    velocityThreshold = helper.readConfig('config/config.json')
    coordWithTime = helper.restructureCoordinatesFormat(data)
    coordWithoutTime = helper.restructureCoordinatesFormatWithoutTime(data)
    print("velocityThreshold: ", velocityThreshold)
    print("coordinates: ", coordWithTime)
    return velocityThreshold, coordWithTime, coordWithoutTime


def displayGraphs(coordWithoutTime, fixation, fixationMaxGap, fixationPyGaze):
    plt.subplot(2, 2, 1)
    coordX = helper.groupCoordX(coordWithoutTime)
    coordY = helper.groupCoordY(coordWithoutTime)
    plt.scatter(coordX, coordY)
    plt.title("coordinates figure")
    plt.tight_layout()

    plt.subplot(2, 2, 2)
    groupFixationX = helper.groupCoordX(fixation)
    groupFixationY = helper.groupCoordY(fixation)
    plt.scatter(groupFixationX, groupFixationY)
    plt.title("fixation maxgap 2 figure")
    plt.tight_layout()

    plt.subplot(2, 2, 3)
    groupFixationX = helper.groupCoordX(fixationPyGaze)
    groupFixationY = helper.groupCoordY(fixationPyGaze)
    plt.scatter(groupFixationX, groupFixationY)
    plt.title("fixation PyGaze figure")
    plt.tight_layout()

    plt.subplot(2, 2, 4)
    groupFixationX = helper.groupCoordX(fixationMaxGap)
    groupFixationY = helper.groupCoordY(fixationMaxGap)
    plt.scatter(groupFixationX, groupFixationY)
    plt.title("fixation maxgap 1 figure")
    plt.tight_layout()
    plt.show()


def processData(velocityThreshold, coordWithTime, coordWithoutTime, maxgap):
    distance = helper.computeDistance(coordWithTime)
    velocities = helper.computeVelocity(distance)
    classifiedCoord = helper.ivtClassifier(velocities, velocityThreshold)
    fixationGroups = list(helper.groupConsecutiveFixation(classifiedCoord))
    mappedCoordToFixation = helper.mapCoordinatesToFixationGroups(coordWithoutTime, fixationGroups, maxgap)
    restructuredMappedCoordToFixation = helper.separateXAndYCoord(mappedCoordToFixation)  # format [x,....x][y,....y]
    fixation = helper.centroidOfFixation(restructuredMappedCoordToFixation)

    print("distance: ", distance)
    print("velocities: ", velocities)
    print("classified Coord: ", classifiedCoord)
    print("fixation groups: ", str(fixationGroups))
    print("res: ", mappedCoordToFixation)
    print("res after restructure: ", restructuredMappedCoordToFixation)
    print("fixation: ", fixation)
    return fixation


def main():
    velocityThreshold, coordWithTime, coordWithoutTime = preProcessData()
    fixationMaxGap1 = processData(velocityThreshold, coordWithTime, coordWithoutTime, 2)
    fixationMaxGap2 = processData(velocityThreshold, coordWithTime, coordWithoutTime, 1)
    sfix, efix = pyGazeClassifier()
    print("sfix :", sfix)
    fixationPyGaze = []
    for i in range(len(efix) - 1):
        fixationPyGaze.append((efix[i][3], efix[i][4]))

    displayGraphs(coordWithoutTime, fixationMaxGap1, fixationMaxGap2, fixationPyGaze)


if __name__ == '__main__':
    main()  # main function keeps variables locally scoped
