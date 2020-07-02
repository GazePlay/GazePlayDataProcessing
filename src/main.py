import src.dataprocessing as helper
import matplotlib.pyplot as plt


def processData():
    data = helper.readJsonDataFromFile('data/data.json')
    velocityThreshold = helper.readConfig('config/config.json')
    coordX = helper.groupCoordX(data)
    coordY = helper.groupCoordY(data)
    coordAfterSeparation = [coordX, coordY]
    coordWithTime = helper.restructureCoordinatesFormat(data)
    distance = helper.computeDistance(coordWithTime)
    velocities = helper.computeVelocity(distance)
    classifiedCoord = helper.ivtClassifier(velocities, velocityThreshold)
    fixationGroups = list(helper.groupConsecutiveFixation(classifiedCoord))
    # helper.getFixation(coordWithTime, fixationGroups)
    # centroidOfFixation = helper.centroidOfFixation(coordAfterSeparation)

    print("velocityThreshold: ", velocityThreshold)
    print("coordinates: ", coordWithTime)
    print("distance: ", distance)
    print("velocities: ", velocities)
    print("classified Coord: ", classifiedCoord)
    print("fixation groups: ", str(fixationGroups))
    # print("centroid of fixation: ", centroidOfFixation)
    plt.scatter(coordX, coordY)
    plt.title("Coordinates figure")
    plt.show()


def main():
    processData()


if __name__ == '__main__':
    main()  # main function keeps variables locally scoped
