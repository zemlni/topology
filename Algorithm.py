import matplotlib.pyplot as plt
import random
import math
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.representative = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.representative == other.representative

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y, self.representative))


class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.weight = p1.y if p1.y > p2.y else p2.y

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2 and self.weight == other.weight

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.p1, self.p2, self.weight))
    def getPoints(self):
        return {self.p1, self.p2}


class Triangle:
    def __init__(self, e1, e2, e3):
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
        self.weight = max([x.weight for x in [self.e1, self.e2, self.e3]])

    def __eq__(self, other):
        return self.e1 == other.e1 and self.e2 == other.e2 and self.e3 == other.e3 and self.weight == other.weight

    def __ne__(self, other):
        return not self.__eq__(other)

    def getEdges(self):
        return {self.e1, self.e2, self.e3}

    def __hash__(self):
        return hash((self.e1, self.e2, self.e3, self.weight))


def linePersistence(pointArray):
    answerArray = []
    copy = list(pointArray)

    previousLowestY = Point(0, -1000000000)
    for i in range(0, len(pointArray)):
        lowestY = copy[0]
        for point in copy:
            if point.y < lowestY.y:
                lowestY = point

        copy.remove(lowestY)

        index = pointArray.index(lowestY)
        # for beginning and end: only check the one that is there, if it is higher then no death, if it is lower then death.
        if index + 1 >= len(pointArray) or index < 0:
            continue

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


def getPoints(point, pointArray):
    answer = []
    x, y = point.x, point.y
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if not (i == x and j == y):
                try:
                    newPoint = pointArray[i][j]
                    if newPoint.z < point.z:
                        answer.append(pointArray[i][j])
                except:
                    continue
    return answer


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.representative = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.representative == other.representative

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.representative))

def getEdge(edgeList, p1, p2):
    for edge in edgeList:
        if p1 in edge.getPoints() and p2 in edge.getPoints():
            return edge
    return Edge(p1, p2)

def oneDPersistence(pointArray):
    oDAnswer = []
    oneDAnswer = []
    # find the lowestY
    copy = [item for sublist in pointArray for item in sublist]

    edgesList = []
    trianglesList = []
    num = len(copy)
    previousLowestY = Point3D(0, 0, -1000000000)
    for i in range(0, num):

        lowestZ = copy[0]
        # for array in copy:
        for point in copy:
            if point.z < lowestZ.z:
                lowestZ = point

        copy.remove(lowestZ)
        surrounding = getPoints(lowestZ, pointArray)

        # OD persistence
        if len(surrounding) < 1:
            continue

        lowestRep = surrounding[0]
        for point in surrounding:
            if point.representative < lowestRep.representative:
                lowestRep = point

        lowestZ.representative = lowestRep.representative

        for point in surrounding:
            if point.representative != lowestZ.representative:
                oDAnswer.append((point.representative, lowestZ.z))

            point.representative = lowestZ.representative

        # 1D persistence
        sameReps = {}
        for point in surrounding:
            if point.representative not in sameReps.keys():
                sameReps[point.representative] = []
            sameReps[point.representative].append(point)

        for k, v in sameReps.items():
            if len(v) > 1:
                for i in range(1, len(v)):
                    edge = Edge(lowestZ, v[i])
                    '''
                    edgesDict[edge] = numEdges
                    edgesDictReverse[numEdges] = edge
                    numEdges += 1
                    '''
                    edgesList.append(edge)

                    p1, p2 = edge.p1, edge.p2
                    intersection = set(getPoints(p1, pointArray)).intersection(set(getPoints(p2, pointArray)))

                    for point in intersection:
                        e2 = getEdge(edgesList, point, p1)
                        if e2 not in edgesList: edgesList.append(e2)
                        e3 = getEdge(edgesList, point, p2)
                        if e3 not in edgesList: edgesList.append(e3)
                        triangle = Triangle(edge, e2, e3)
                        '''
                        trianglesDict[triangle] = numTriangles
                        trianglesDictReverse[numTriangles] = triangle
                        numTriangles += 1
                        '''
                        trianglesList.append(triangle)

        # make matrix
        matrix = []
        for i in range(0, len(trianglesList)):
            tempList = []
            for j in range(0, len(edgesList)):
                tempList.append([])
            matrix.append(tempList)

        for i in range(0, len(trianglesList)):
            triangle = trianglesList[i]
            for edge in triangle.getEdges():
                matrix[i][edgesList.index(edge)] = 1

        # matrix reduction
        for i in range(0, len(matrix)):
            for j in range(0, i):
                if getLowestOne(matrix[j]) == getLowestOne(matrix[i]):
                    matrix[i] = [x + y if x + y < 2 else 0 for x, y in zip(matrix[i], matrix[j])]

        for i in range(0, len(matrix)):
            lowest1 = getLowestOne(matrix[i])
            edge = edgesList[lowest1]
            triangle = trianglesList[i]
            oneDAnswer.append((edge.weight, triangle.weight))

    return oDAnswer, oneDAnswer


def getLowestOne(array):
    return len(array) - list(reversed(array)).index(1) - 1


'''
def linePersistence(pointArray):
    #
    # while there are still points remaining:
    #
    # find current lowest point:
    # get list of points around the center point
    # check all points around it, retain the ones that are lower than the height of the center point
    # change the reps of the lower points to the rep of the lowest point
    # add coordinates to the persistance diagram for every point whose representative you change as (old representative, current height)


    return answerArray
'''


def lineSample():
    with open("output.txt", "w+") as output:
        for col in range(1, 60):
            pointList = []
            with open("Harv_transects", 'r') as file:
                i = 0
                for line in file:

                    lineSplit = line.split(",")
                    if i != 0 and str(lineSplit[col]) != "NA":
                        try:
                            num = float(lineSplit[col])
                        except:
                            continue
                        if num == 0:
                            num += random.random() / 100000
                        pointList.append(Point(i, num))
                    i += 1

            # pointList = [Point(x, 0.1 * x ** 3 + 2.3 *  x ** 2 + 0.7 * x + 0.6) for x in range(-25, 10)]
            persistencePoints = linePersistence(pointList)
            output.write(str(persistencePoints) + "\n")

        '''
        x = [i[0] for i in persistencePoints]
        y = [i[1] for i in persistencePoints]

        plt.plot(x, y, "o")
        plt.show()
        '''


def starSample():
    pointList = [[Point3D(x, y, (-x ** 2 - y ** 2) + random.random() / 100000) for x in range(-10, 10)] for y in
                 range(-10, 10)]
    persistencePoints = oneDPersistence(pointList)
    print(persistencePoints)
    x = [i[0] for i in persistencePoints[0]]
    y = [i[1] for i in persistencePoints[0]]

    plt.plot(x, y, "o")
    #x = np.linspace(-100, 100)
    #plt.plot(x, x, '-')
    plt.show()
    # print(pointList)


starSample()
# lineSample()
