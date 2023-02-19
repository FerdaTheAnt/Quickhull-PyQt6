import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.GeoArea = GeoArea()
        self.setCentralWidget(self.GeoArea)
        self.toolBar = QtWidgets.QToolBar()
        randomAction = QtGui.QAction("Random set", self)
        randomAction.triggered.connect(self.randomAct)
        self.toolBar.addAction(randomAction)
        self.addToolBar(self.toolBar)

    def randomAct(self):
        self.GeoArea.randomSet()

class GeoArea(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.pointsX = []
        self.pointsY = []
        self.lastPoint = None
        self.pointCounter = 0
        self.MAX_POINTS = 100
        self.pen = QtGui.QPen(QtGui.QColor("green"), 5)
        self.brush = QtGui.QBrush(QtGui.QColor("green"), QtCore.Qt.SolidPattern)
        self.image = QtGui.QImage()

    def paintEvent(self, pe):
        painter = QtGui.QPainter(self)
        painter.drawImage(0,0,self.image)
    
    def mousePressEvent(self, event):
        if(event.button() == QtCore.Qt.LeftButton):
            pos = event.position()
            self.createPoint(pos.x(), pos.y())

    def resizeEvent(self, re):
        if(self.width() > self.image.width() or self.height() > self.image.height()):
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.resizeImage(self.image, QtCore.QSize(newWidth, newHeight))
            self.update()

    def createPoint(self, x, y):
        if(not self.image.isNull() and self.pointCounter < self.MAX_POINTS):
            self.pointCounter += 1
            self.lastPoint = (x,y)
            self.pointsX.append(self.lastPoint[0])
            self.pointsY.append(self.lastPoint[1])
            painter = QtGui.QPainter(self.image)
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
            painter.drawEllipse(x, y, 2, 2)  
            self.update()

    def randomSet(self):
        self.pointsX.clear()
        self.pointsY.clear()
        self.pointCounter = 0
        self.image.fill(QtGui.QColor("white"))
        for _ in range(self.MAX_POINTS):
            temp_x = random.uniform(10, self.width()-10)
            temp_y = random.uniform(10, self.height()-10)
            self.createPoint(temp_x, temp_y)

    def resizeImage(self, oldImage, newSize):
        if (self.image.size() == newSize):
            return
        
        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.QColor("white"))
        painter = QtGui.QPainter(newImage)
        
        painter.drawImage(0, 0, oldImage)
        self.image = newImage

    def quickHull(self):
        hull = set()

        index = self.pointsX.index(min(self.pointsX))
        first = (self.pointsX[index], self.pointsY[index])
        index = self.pointsX.index(max(self.pointsX))
        second = (self.pointsX[index], self.pointsY[index])
        hull.add(first, second)

        self.assembleSet(first, second)
        self.assembleSet(second, first)

    def assembleSet(self, A, B):
        C = self.findFurthest(A, B) #points a, b, c form a triangle, we assemble points that are inside this triangle
        for i in range(self.pointCounter):
            point = (self.pointsX[i], self.pointsY[i])
            if(self.insideTriangle(A, B, C, point)):
                #remove point from list of points
                pass

    def findFurthest(self, A, B):
        lineVect = (B[0] - A[0], B[1] - A[1])
        pointVect = 0
        area = 0
        furthest = -1
        index = 0
        for i in range(self.pointCounter):
            pointVect = (self.pointsX[i] - A[0], self.pointsY[i] - A[1])
            area = lineVect[0]*pointVect[1] - lineVect[1]*pointVect[0] #points "under" line AB should have negative area
            if(area > furthest):
                furthest = area
                index = i
        return (self.pointsX[index], self.pointsY[index])
    
    def insideTriangle(self, A, B, C, point):
        if(not self.lineSide(A, B, point)): return False
        if(not self.lineSide(B, C, point)): return False
        if(not self.lineSide(C, A, point)): return False
        return True
    
    def lineSide(self, A, B, point):
        lineVect = (B[0] - A[0], B[1] - A[1])
        pointVect = (point[0] - A[0], point[1] - A[1])
        area = lineVect[0]*pointVect[1] - lineVect[1]*pointVect[0]
        if(area <= 0):
            return False
        return True

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())