
from PyQt5 import QtGui, QtCore

packetDrawX = 530
packetDrawY = 138
packetDrawWidth = 100

def comboToInt(str,start):
    str = str[start:]
    #[int(str) for str in str.split() if str.isdigit()][0]
    return int(str)

def comboBoolToInt(str):
    if str == 'true':
        return 1
    else:
        return 0

def comNoSlash(str):
    nstr = (str.translate({ord('/'): None}))
    return comboToInt(nstr,0)

def khzTohz(str):
    nstr = float(str)
    nstr *=1000
    return int(nstr)

def comboBoxDisable(cb):
    cb.setEnabled(False)

def comboBoxEnable(cb):
    cb.setEnabled(True)

def editTextDisable(le):
    le.setEnabled(False)

def editTextEnable(le):  
    le.setEnabled(True)

def btnDisable(btn):
    btn.setEnabled(False)

def btnEnable(btn):
    btn.setEnabled(True)

def groupboxDisable(gb):
    gb.setEnabled(False)

def groupboxEnable(gb):
    gb.setEnabled(True)    

def drawLines(self, qp):
      
    pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

    qp.setPen(pen)
    qp.drawLine(20, 40, 250, 40)

    pen.setStyle(QtCore.Qt.DashLine)
    qp.setPen(pen)
    qp.drawLine(20, 80, 250, 80)

    pen.setStyle(QtCore.Qt.DashDotLine)
    qp.setPen(pen)
    qp.drawLine(20, 120, 250, 120)

    pen.setStyle(QtCore.Qt.DotLine)
    qp.setPen(pen)
    qp.drawLine(20, 160, 250, 160)

    pen.setStyle(QtCore.Qt.DashDotDotLine)
    qp.setPen(pen)
    qp.drawLine(20, 200, 250, 200)

    pen.setStyle(QtCore.Qt.CustomDashLine)
    pen.setDashPattern([1, 4, 5, 4])
    qp.setPen(pen)
    qp.drawLine(20, 240, 250, 240)