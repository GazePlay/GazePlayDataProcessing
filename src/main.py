import src.dataprocessing as helper
import matplotlib.pyplot as plt


def preProcessData():
    data = helper.readJsonDataFromFile('data/data.json')
    velocityThreshold = helper.readConfig('config/config.json')
    coordWithTime = helper.restructureCoordinatesFormat(data)
    coordWithoutTime = helper.restructureCoordinatesFormatWithoutTime(data)
    print("velocityThreshold: ", velocityThreshold)
    print("coordinates: ", coordWithTime)
    return velocityThreshold, coordWithTime, coordWithoutTime


def displayGraphs(coordWithoutTime, fixation):
    plt.subplot(1, 2, 1)
    coordX = helper.groupCoordX(coordWithoutTime)
    coordY = helper.groupCoordY(coordWithoutTime)
    plt.scatter(coordX, coordY)
    plt.title("coordinates figure")
    plt.tight_layout()

    plt.subplot(1, 2, 2)
    groupFixationX = helper.groupCoordX(fixation)
    groupFixationY = helper.groupCoordY(fixation)
    plt.scatter(groupFixationX, groupFixationY)
    plt.title("fixation figure")
    plt.tight_layout()
    plt.show()


def processData(velocityThreshold, coordWithTime, coordWithoutTime):
    distance = helper.computeDistance(coordWithTime)
    velocities = helper.computeVelocity(distance)
    classifiedCoord = helper.ivtClassifier(velocities, velocityThreshold)
    fixationGroups = list(helper.groupConsecutiveFixation(classifiedCoord))
    mappedCoordToFixation = helper.mapCoordinatesToFixationGroups(coordWithoutTime, fixationGroups)
    restructuredMappedCoordToFixation = helper.separateXAndYCoord(mappedCoordToFixation)  # format [x,....x][y,....y]
    fixation = helper.centroidOfFixation(restructuredMappedCoordToFixation)

    print("distance: ", distance)
    print("velocities: ", velocities)
    print("classified Coord: ", classifiedCoord)
    print("fixation groups: ", str(fixationGroups))
    print("res: ", mappedCoordToFixation)
    print("res after restructure: ", restructuredMappedCoordToFixation)
    print("fixation: ", fixation)
    displayGraphs(coordWithoutTime, fixation)


def main():
    velocityThreshold, coordWithTime, coordWithoutTime = preProcessData()
    processData(velocityThreshold, coordWithTime, coordWithoutTime)


if __name__ == '__main__':
    main()  # main function keeps variables locally scoped
