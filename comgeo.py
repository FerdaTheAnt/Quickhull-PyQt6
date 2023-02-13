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
        #self.pen.setCapStyle = QtCore.Qt.PenCapStyle.RoundCap
        #self.pixmap = QtGui.QPixmap(self.size())
        self.pixmap = self.grab()
        self.image = QtGui.QImage()

    def paintEvent(self, pe):
        if(self.point):
            painter = QtGui.QPainter(self)
            #painter.setPen(self.pen)
            painter.drawPixmap(0,0,self.pixmap)
    
    def mousePressEvent(self, event):
        if(event.button() == QtCore.Qt.LeftButton):
            self.createPoint(event.position())

    #def resizeEvent(self, re):
     #   pass

    def createPoint(self, pos):
        self.point = QtCore.QPointF(pos)
        painter = QtGui.QPainter(self.pixmap)
        painter.setPen(self.pen)
        painter.drawPoint(self.point)  
        self.update()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())