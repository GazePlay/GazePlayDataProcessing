import src.dataprocessing as helper


def processData():
    data = helper.readJsonDataFromFile('data/data.json')
    velocityThreshold = helper.readConfig('config/config.json')
    coord = helper.restructureCoordinatesFormat(data)
    distance = helper.computeDistance(coord)
    velocities = helper.computeVelocity(distance)
    fixation = helper.classifyVelocities(velocities, velocityThreshold)
    fixationGroups = list(helper.groupConsecutiveFixation(fixation))
    print("velocityThreshold: ", velocityThreshold)
    print("coordinates: ", coord)
    print("distance: ", distance)
    print("velocities: ", velocities)
    print("fixation: ", fixation)
    print("fixation groups: ", str(fixationGroups))


def main():
    processData()


if __name__ == '__main__':
    main()  # main function keeps variables locally scoped
