import src.util as helper


def main():
    data = helper.readJsonDataFromFile("/home/christophe/PycharmProjects/gazePlayDataProcessing/data/data.json")
    print(data)


if __name__ == '__main__':
    main()  # main function keeps variables locally scoped
