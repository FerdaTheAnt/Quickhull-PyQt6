import random

#compute convex hull for a given set of points in 2-D
def beginQuickHull(points):
    hull = set()

    index = points[0].index(min(points[0]))
    first = (points[0][index], points[1][index])
    index = points[0].index(max(points[0]))
    second = (points[0][index], points[1][index])
    hull.add(second)
    hull.add(first)

    S1 = assembleSet(first, second, points)    #left side
    S2 = assembleSet(second, first, points)    #right side

    quickHull(S1, first, second, hull)
    quickHull(S2, second, first, hull)

    return hull

def assembleSet(A, B, points):
    #assemble points from a given set that are on the left side of the line AB
    S = [[], []]
    for i in range(len(points[0])):
        point = (points[0][i], points[1][i])
        if(lineSide(A,B, point) == "Left"):
            S[0].append(point[0])
            S[1].append(point[1])
    return S

def quickHull(S, A, B, hull):
    if(S == [[], []]):
        return
    C = findFurthest(A, B, S) #points a, b, c form a triangle, we assemble points that are inside this triangle
    hull.add(C)
    S1 = assembleSet(A, C, S)
    S2 = assembleSet(C, B, S)
    quickHull(S1, A, C, hull)
    quickHull(S2, C, B, hull)
    return hull

def findFurthest(A, B, S):
    lineVect = (B[0] - A[0], B[1] - A[1])
    pointVect = 0
    area = 0
    furthest = -1
    index = 0
    for i in range(len(S[0])):
        pointVect = (S[0][i] - A[0], S[1][i] - A[1])
        area = lineVect[0]*pointVect[1] - lineVect[1]*pointVect[0] #points "under" line AB should have negative area
        if(area > furthest):
            furthest = area
            index = i
    return (S[0][index], S[1][index])

def lineSide(A, B, point):
    lineVect = (B[0] - A[0], B[1] - A[1])
    pointVect = (point[0] - A[0], point[1] - A[1])
    area = lineVect[0]*pointVect[1] - lineVect[1]*pointVect[0]
    if(area <= 0):
        return "Right"
    return "Left"

if __name__ == "__main__":
    pass