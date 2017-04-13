import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.representative = y



def persistence(pointArray):
    answerArray = []
    copy = list(pointArray)

    previousLowestY = Point(0, -1000000000)
    for i in range(0, len(pointArray)):
        lowestY = copy[0]
        for point in copy:
            if point.y < lowestY.y:
                lowestY = point

        copy.remove(lowestY)
        print(lowestY.y)

        index = pointArray.index(lowestY)
        # for beginning and end: only check the one that is there, if it is higher then no death, if it is lower then death.
        if index == 0:
            if pointArray[index + 1].representative < lowestY.representative:
                lowestY.representative = pointArray[index + 1].representative
                answerArray.append((lowestY.y, lowestY.y))
                continue

        if index == len(pointArray) - 1:
            if pointArray[index - 1].representative < lowestY.representative:
                lowestY.representative = pointArray[index - 1].representative
                answerArray.append((lowestY.y, lowestY.y))
                continue

        left = pointArray[index - 1]
        right = pointArray[index + 1]

        if left.representative < lowestY.representative and right.representative > lowestY.representative:
            lowestY.representative = left.representative
            answerArray.append((lowestY.y, lowestY.y))

        if left.representative > lowestY.representative and right.representative < lowestY.representative:
            lowestY.representative = right.representative
            answerArray.append((lowestY.y, lowestY.y))

        if left.representative < lowestY.representative and right.representative < lowestY.representative:
            if left.representative > right.representative:
                lowestY.representative = right.representative
                answerArray.append((left.representative, lowestY.y))
                left.representative = right.representative

            if left.representative < right.representative:
                lowestY.representative = left.representative
                answerArray.append((right.representative, lowestY.y))
                right.representative = left.representative

        previousLowestY = lowestY

    return answerArray

def sample():
    pointList = [Point(x, 0.1 * x ** 3 + 2.3 *  x ** 2 + 0.7 * x + 0.6) for x in range(-25, 10)]

    persistencePoints = persistence(pointList)
    print(persistencePoints)
    x = [i[0] for i in persistencePoints]
    y = [i[1] for i in persistencePoints]

    plt.plot(x, y, "o")
    plt.show()


sample()

