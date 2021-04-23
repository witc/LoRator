
from PyQt5 import QtGui, QtCore

packetDrawX = 530
packetTXDrawY = 118
packetRXDrawY = 216
packetDrawWidth = 100

class  GuiManager():

    def __init__(self, mainwindow, parent = None):
        #super(ThreadClass,self).__init__(parent)
        self.mainWin = mainwindow


    def getTXFreq(self):
        return int(self.mainWin.leTXFreq.text())

    def getRXFreq(self):
        return int(self.mainWin.leRXFreq.text())

    def getTXSF(self):
        return self.comboToInt(self.mainWin.cbTXSF.currentText(),2)

    def getRXSF(self):
        return self.comboToInt(self.mainWin.cbRXSF.currentText(),2)

    def getTXBW(self):
        return self.khzTohz(self.mainWin.cbTXBW.currentText())

    def getRXBW(self):
        return self.khzTohz(self.mainWin.cbRXBW.currentText())

    def getTXIQ(self):
        return self.comboBoolToInt(self.mainWin.cbTXIQ.currentText())

    def getRXIQ(self):
        return self.comboBoolToInt(self.mainWin.cbRXIQ.currentText())

    def getTXCR(self):
        return self.comNoSlash(self.mainWin.cbTXCR.currentText())

    def getRXCR(self):
        return self.comNoSlash(self.mainWin.cbRXCR.currentText())

    def getTXHead(self):
        return self.comboBoolToInt(self.mainWin.cbTXHeader.currentText())

    def getRXHead(self):
        return self.comboBoolToInt(self.mainWin.cbRXHeader.currentText())

    def getTXCrc(self):
        return self.comboBoolToInt(self.mainWin.cbTXCrc.currentText())

    def getRXCrc(self):
        return self.comboBoolToInt(self.mainWin.cbRXCrc.currentText())

    def getTXPower(self):
        return int(self.mainWin.leTXPower.text())


    def updatePacketDrawing(self,e):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
        painter.eraseRect(60, 650, 500,40)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.darkGreen, QtCore.Qt.Dense4Pattern ))

        next = packetDrawX
        nextRX = packetDrawX
        
        #Preamble
        painter.drawRect(next, packetTXDrawY, packetDrawWidth,40)
        painter.drawRect(next, packetRXDrawY, packetDrawWidth,40)
        self.lblTXPream.setText("Preamble")
        self.lblRXPream.setText("Preamble")
        next+=packetDrawWidth
        nextRX+=packetDrawWidth
        #TX Header
        if self.cbTXHeader.currentText() == "Enabled":
            painter.setBrush(QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.Dense4Pattern))
            painter.drawRect(next, packetTXDrawY, packetDrawWidth,40)
            self.lblTXHeader.setText("Header")
            next+=packetDrawWidth
            self.lblTXPayload.setGeometry(packetDrawWidth+self.lblTXHeader.x(), self.lblTXHeader.y(), self.lblTXHeader.width(), self.lblTXHeader.height()) 
            self.lblTXCRC.setGeometry(packetDrawWidth+self.lblTXPayload.x(), self.lblTXPayload.y(), self.lblTXPayload.width(), self.lblTXPayload.height()) 
        else:
            self.lblTXHeader.setText("")
            self.lblTXPayload.setGeometry(self.lblTXHeader.x(), self.lblTXHeader.y(), self.lblTXHeader.width(), self.lblTXHeader.height()) 
            self.lblTXCRC.setGeometry(packetDrawWidth+self.lblTXPayload.x(), self.lblTXPayload.y(), self.lblTXPayload.width(), self.lblTXPayload.height()) 

        #RX Header
        if self.cbRXHeader.currentText() == "Enabled":
            painter.setBrush(QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.Dense4Pattern))
            painter.drawRect(nextRX, packetRXDrawY, packetDrawWidth,40)
            self.lblRXHeader.setText("Header")
            nextRX+=packetDrawWidth
            self.lblRXPayload.setGeometry(packetDrawWidth+self.lblRXHeader.x(), self.lblRXHeader.y(), self.lblRXHeader.width(), self.lblRXHeader.height()) 
            self.lblRXCRC.setGeometry(packetDrawWidth+self.lblRXPayload.x(), self.lblRXPayload.y(), self.lblRXPayload.width(), self.lblRXPayload.height()) 
        else:
            self.lblRXHeader.setText("")
            self.lblRXPayload.setGeometry(self.lblRXHeader.x(), self.lblRXHeader.y(), self.lblRXHeader.width(), self.lblRXHeader.height()) 
            self.lblRXCRC.setGeometry(packetDrawWidth+self.lblRXPayload.x(), self.lblRXPayload.y(), self.lblRXPayload.width(), self.lblRXPayload.height()) 


        #TX Payload
        painter.setBrush(QtGui.QBrush(QtCore.Qt.cyan, QtCore.Qt.Dense4Pattern))
        painter.drawRect(next, packetTXDrawY, packetDrawWidth,40)
        self.lblTXPayload.setText("Payload")
        next+=packetDrawWidth

        #RX Payload
        painter.setBrush(QtGui.QBrush(QtCore.Qt.cyan, QtCore.Qt.Dense4Pattern))
        painter.drawRect(nextRX, GuiManager.packetRXDrawY, GuiManager.packetDrawWidth,40)
        self.lblRXPayload.setText("Payload")
        nextRX+=GuiManager.packetDrawWidth
        
        

    def comboToInt(self,str,start):
        str = str[start:]
        #[int(str) for str in str.split() if str.isdigit()][0]
        return int(str)

    def comboBoolToInt(self,str):
        if str == 'true' or str == 'Enabled':
            return 1
        else:
            return 0

    def comNoSlash(self, str):
        nstr = (str.translate({ord('/'): None}))
        return self.comboToInt(nstr,0)

    def khzTohz(self,str):
        nstr = float(str)
        nstr *=1000
        return int(nstr)

    def comboBoxDisable(self,cb):
        cb.setEnabled(False)

    def comboBoxEnable(self,cb):
        cb.setEnabled(True)

    def editTextDisable(self,le):
        le.setEnabled(False)

    def editTextEnable(self,le):  
        le.setEnabled(True)

    def btnDisable(self,btn):
        btn.setEnabled(False)

    def btnEnable(self,btn):
        btn.setEnabled(True)

    def groupboxDisable(self,gb):
        gb.setEnabled(False)

    def groupboxEnable(self,gb):
        gb.setEnabled(True)    

    def dissableAppWidgets(self):
        self.groupboxDisable(self.mainWin.groupBox)
        self.groupboxDisable(self.mainWin.groupBox_4)

    def enableAppWidgets(self):
        self.groupboxEnable(self.mainWin.groupBox)
        self.groupboxEnable(self.mainWin.groupBox_4)
        # GuiManager.editTextEnable(self.leTXFreq)
        # GuiManager.editTextEnable(self.leRXFreq)
        # GuiManager.comboBoxEnable(self.cbTXSF)
        # GuiManager.comboBoxEnable(self.cbRXSF)
        # GuiManager.comboBoxEnable(self.cbTXBW)
        # GuiManager.comboBoxEnable(self.cbRXBW)
        # GuiManager.comboBoxEnable(self.cbTXIQ)
        # GuiManager.comboBoxEnable(self.cbRXIQ)
        # GuiManager.comboBoxEnable(self.cbTXCR)
        # GuiManager.comboBoxEnable(self.cbRXCR)
        # GuiManager.comboBoxEnable(self.cbTXHeader)
        # GuiManager.comboBoxEnable(self.cbRXHeader)
        # GuiManager.comboBoxEnable(self.cbTXCrc)
        # GuiManager.comboBoxEnable(self.cbRXCrc)
        # GuiManager.editTextEnable(self.leTXPower)
        # GuiManager.btnEnable(self.buttonWriteRadio)
        # GuiManager.btnEnable(self.buttonReadRadio)
        # GuiManager.btnEnable(self.btnStandby)
        # GuiManager.btnEnable(self.btnTXCW)
        
