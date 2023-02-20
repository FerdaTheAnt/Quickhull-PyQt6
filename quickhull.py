import random

#compute convex hull for a given set of points in 2-D
def beginQuickHull(points):
    hull = set()
    first = list(points)[0]
    second = first
    for point in points:
        if(point[0] < first[0]):
            first = point
        if(point[0] > second[0]):
            second = point

    hull.add(second)
    hull.add(first)

    S1 = assembleSet(first, second, points)    #left side
    S2 = assembleSet(second, first, points)    #right side

    quickHull(S1, first, second, hull)
    quickHull(S2, second, first, hull)

    return hull

def assembleSet(A, B, points):
    #assemble points from a given set that are on the left side of the line AB
    S = set()
    for point in points:
        if(lineSide(A,B, point) == "Left"):
            S.add(point)
    return S

def quickHull(S, A, B, hull):
    if(not S):
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
    max_dist = -1
    furthest = None
    for point in S:
        pointVect = (point[0] - A[0], point[1] - A[1])
        area = lineVect[0]*pointVect[1] - lineVect[1]*pointVect[0] #points "under" line AB should have negative area
        if(area > max_dist):
            max_dist = area
            furthest = point
    return furthest

def lineSide(A, B, point):
    lineVect = (B[0] - A[0], B[1] - A[1])
    pointVect = (point[0] - A[0], point[1] - A[1])
    area = lineVect[0]*pointVect[1] - lineVect[1]*pointVect[0]
    if(area <= 0):
        return "Right"
    return "Left"

if __name__ == "__main__":
    pass