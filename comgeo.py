import sys
from PySide6 import QtCore, QtWidgets, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.GeoArea = GeoArea()
        self.setCentralWidget(self.GeoArea)


class GeoArea(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.point = None
        self.pen = QtGui.QPen(QtGui.QColor("green"), 5)
        self.brush = QtGui.QBrush(QtGui.QColor("green"), QtCore.Qt.SolidPattern)
        #self.pixmap = self.grab()
        self.image = QtGui.QImage()

    def paintEvent(self, pe):
        #if(not self.image.isNull()):
        painter = QtGui.QPainter(self)
        #painter.setPen(self.pen)
        painter.drawImage(0,0,self.image)
    
    def mousePressEvent(self, event):
        if(event.button() == QtCore.Qt.LeftButton):
            self.createPoint(event.position())

    def resizeEvent(self, re):
        if(self.width() > self.image.width() or self.height() > self.image.height()):
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.resizeImage(self.image, QtCore.QSize(newWidth, newHeight))
            self.update()

    def createPoint(self, pos):
        self.point = QtCore.QPointF(pos)
        painter = QtGui.QPainter(self.image)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawEllipse(self.point, 2, 2)  
        self.update()

    def resizeImage(self, oldImage, newSize):
        if (self.image.size() == newSize):
            return
        
        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.QColor("white"))
        painter = QtGui.QPainter(newImage)
        
        painter.drawImage(0, 0, oldImage)
        self.image = newImage

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())