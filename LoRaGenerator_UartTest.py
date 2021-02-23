import threading
from USB2Uart import USBSerialLink
from RadioFunctions import RadioCmds
import time
import argparse
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, QRegExp
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
#from QtGui  import QPainter, QBrush, QPen
from LoRatorGui import Ui_MainWindow
import  RadioParam
import ptvsd
import GuiManager
import binascii

Generator1 = RadioParam.RadioParam ()
 
USBLink = USBSerialLink()
#if USBLink.openUSBRfLink() != "False":
#    print("USB Generator connected")
Radio = RadioCmds(USBLink)


RadioOpCodeSwitcher = {
        1: Radio.saveTxFreq,
        2: Radio.saveRxFreq,
        3: Radio.saveTxPower,
        4: Radio.saveTxSf,
        5: Radio.saveRxSf,
        6: Radio.saveTxBW,
        7: Radio.saveRxBW,
        8: Radio.saveTxIq,
        9: Radio.saveRxIq,
        10: Radio.saveTxCR,
        11: Radio.saveRxCR,
        12: Radio.saveHeaderMTx,
        13: Radio.saveHeaderMRx,
        14: Radio.saveTxCRC,
        15: Radio.saveRxCRC,
        16: Radio.saveRadioStatus,
        17: Radio.saveRadioStatus,
        #18: Radio.savePreparedPacket,
        19: Radio.saveAutoRepeating,
        20: Radio.saveRadioStatus,
        21: Radio.saveRadioStatus,
        253: Radio.saveTargetName,
        254:Radio.saveSystemType,
    }

class MainUIClass(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,radio,usblink, generator ,parent=None):
        #super(MainUIClass, self).__init__(parent)   #nebo ekvivalent super.__init() first param is a subclass coz je MainUIClass
        super().__init__()
        self.setupUi(self)
        self.Radio = radio
        self.USBLink = usblink
        self.Generator = generator
        self.addedChar = False
        
        # scan Serial ports
        self.comboBox.clear() 
        self.USBLink.scanUSBRfLink()
        self.comboBox.addItems(self.USBLink.getPossibleComs())
        self.btnComConnect.clicked.connect(self.CallbackCom)
        
        self.onlyInt = QtGui.QIntValidator()
        self.onlyHex = QtGui.QRegExpValidator(QRegExp("[0-9A-Fa-f]{1,100}"))
        self.leTXFreq.setValidator(self.onlyInt)
        self.leHexInput.setValidator(self.onlyHex)
        self.leHexInput.textChanged.connect(self.CallbackHexInChanged)
        self.leStringInput.textChanged.connect(self.CallbackStringInpu)
        self.cbTXHeader.currentTextChanged.connect(self.CallbackRadioParChange)
        self.cbTXCrc.currentTextChanged.connect(self.CallbackRadioParChange)
        
        self.dissableAppWidgets()
        self.buttonWriteRadio.clicked.connect(self.CallbackWriteRadio)
        self.buttonReadRadio.clicked.connect(self.CallbackReadRadio)
        self.btnStandby.clicked.connect(self.CallbackSetStandby)
        self.btnTXCW.clicked.connect(self.CallbackStartTX)
        self.pushButton_6.clicked.connect(self.CallbackSendPacket)       

    def paintEvent(self,e):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
        painter.eraseRect(60, 650, 500,40)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.darkGreen, QtCore.Qt.DiagCrossPattern ))

        next = GuiManager.packetDrawX
        #Preamble
        painter.drawRect(next, GuiManager.packetDrawY, GuiManager.packetDrawWidth,40)
        self.lblTXPream.setText("Preamble")
        next+=GuiManager.packetDrawWidth
        
        #Header
        if self.cbTXHeader.currentText() == "Enabled":
            painter.setBrush(QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.DiagCrossPattern))
            painter.drawRect(next, GuiManager.packetDrawY, GuiManager.packetDrawWidth,40)
            self.lblTXHeader.setText("Header")
            next+=GuiManager.packetDrawWidth
            self.lblTXPayload.setGeometry(GuiManager.packetDrawWidth+self.lblTXHeader.x(), self.lblTXHeader.y(), self.lblTXHeader.width(), self.lblTXHeader.height()) 
            self.lblTXCRC.setGeometry(GuiManager.packetDrawWidth+self.lblTXPayload.x(), self.lblTXPayload.y(), self.lblTXPayload.width(), self.lblTXPayload.height()) 
        else:
            self.lblTXHeader.setText("")
            self.lblTXPayload.setGeometry(self.lblTXHeader.x(), self.lblTXHeader.y(), self.lblTXHeader.width(), self.lblTXHeader.height()) 
            self.lblTXCRC.setGeometry(GuiManager.packetDrawWidth+self.lblTXPayload.x(), self.lblTXPayload.y(), self.lblTXPayload.width(), self.lblTXPayload.height()) 

        #Payload
        #painter.setBrush(QtGui.QBrush(QtCore.Qt.cyan, QtCore.Qt.Dense6Pattern))
        painter.drawRect(next, GuiManager.packetDrawY, GuiManager.packetDrawWidth,40)
        self.lblTXPayload.setText("Payload")
        next+=GuiManager.packetDrawWidth
        
        
        #CRC
        if self.cbTXCrc.currentText() == "true":
            painter.setBrush(QtGui.QBrush(QtCore.Qt.magenta, QtCore.Qt.DiagCrossPattern))
            painter.drawRect(next, GuiManager.packetDrawY, GuiManager.packetDrawWidth,40)
            self.lblTXCRC.setText("CRC")
            next+=GuiManager.packetDrawWidth
        else:
              self.lblTXCRC.setText("")


    def CallbackRadioParChange(self):
        self.update()

    def CallbackCom(self):
        if self.USBLink.isPortOpen() == True:
            self.USBLink.closePort()
            self.btnComConnect.setText("Connect")

        else:
            self.btnComConnect.setText("Connecting")
            if self.USBLink.openPort(self.comboBox.currentText()) != True:
                self.btnComConnect.setText("Connect")
                return False

        #now port is open  
        self.threadclass = ThreadClass(self)
        self.threadclass.start()
        
        self.Radio.WhatIsYourName()
        time.sleep(0.5)
        
        if any(self.Generator.TargetName in s for s in RadioParam.GeneratorNames):
            self.btnComConnect.setText("Disconnect")
            self.CallbackReadRadio()
            self.enableAppWidgets()
        else:
            self.USBLink.closePort()
            self.btnComConnect.setText("Connect")
    
    def CallbackStringInpu(self):
        text = self.leStringInput.text().encode()
        self.leHexInput.clear()
        self.leHexInput.setText(binascii.hexlify(text).decode())
        #pass

    def CallbackHexInChanged(self):
        
        # tempText = self.leHexInput.text() #bytes.fromhex(self.leHexInput.text())
        # lenText = len(tempText)
        # if lenText%2:
        #      bckp = tempText[-1]
        #      tempText = tempText[:(lenText-1)]
        #      tempText+="0"
        #      tempText+=bckp
        #      self.addedChar = True
        
        # bytes_object = bytes.fromhex(tempText)
        # ascii_string = bytes_object.decode("ASCII")

        #self.leHexInput.setText(tempText)
        #newText = binascii.a2b_hex(tempText)
        #self.leStringInput.setText( ascii_string)
        pass

    def CallbackWriteRadio(self):
        self.leTXFreq.setText(RadioParam.intConstrain(self.leTXFreq.text(),RadioParam.radioMinFreq, RadioParam.radioMaxFreq))
        self.leRXFreq.setText(RadioParam.intConstrain(self.leRXFreq.text(),RadioParam.radioMinFreq, RadioParam.radioMaxFreq))
        self.leTXPower.setText(RadioParam.intConstrain(self.leTXPower.text(),RadioParam.radioMinPower,RadioParam.radioMaxPower))
        Radio.setTxFreq(RadioParam.actionFlagSetGet,int(self.leTXFreq.text()))
        Radio.setTXSF(RadioParam.actionFlagSetGet,GuiManager.comboToInt(self.cbTXSF.currentText(),2))
        Radio.setTXBW(RadioParam.actionFlagSetGet,GuiManager.khzTohz(self.cbTXBW.currentText()))
        Radio.setTXIQ(RadioParam.actionFlagSetGet,GuiManager.comboBoolToInt(self.cbTXIQ.currentText()))
        Radio.setTXCR(RadioParam.actionFlagSetGet,GuiManager.comNoSlash(self.cbTXCR.currentText()))
        Radio.setTXHeaderMode(RadioParam.actionFlagSetGet,GuiManager.comboBoolToInt(self.cbTXHeader.currentText()))
        Radio.setTxCrc(RadioParam.actionFlagSetGet,GuiManager.comboBoolToInt(self.cbTXCrc.currentText()))
        Radio.setTXPower(RadioParam.actionFlagSetGet,int(self.leTXPower.text()))
        
        Radio.setRxFreq(RadioParam.actionFlagSetGet,int(self.leRXFreq.text()))
        Radio.setRXSF(RadioParam.actionFlagSetGet,GuiManager.comboToInt(self.cbRXSF.currentText(),2))
        Radio.setRXBW(RadioParam.actionFlagSetGet,GuiManager.khzTohz(self.cbRXBW.currentText()))
        Radio.setRXIQ(RadioParam.actionFlagSetGet,GuiManager.comboBoolToInt(self.cbRXIQ.currentText()))
        Radio.setRXCR(RadioParam.actionFlagSetGet,GuiManager.comNoSlash(self.cbRXCR.currentText()))
        Radio.setRXHeaderMode(RadioParam.actionFlagSetGet,GuiManager.comboBoolToInt(self.cbRXHeader.currentText()))
        Radio.RxCrcCheck(RadioParam.actionFlagSetGet,GuiManager.comboBoolToInt(self.cbRXCrc.currentText()))
       #ż Radio.setRXPower(RadioParam.actionFlagSetGet,int(self.leRxPower.text()))
       
    
    def CallbackReadRadio(self):
        Radio.setTxFreq(RadioParam.actionFlagGet,0)
        Radio.setTXSF(RadioParam.actionFlagGet,0)
        Radio.setTXBW(RadioParam.actionFlagGet,0)
        Radio.setTXIQ(RadioParam.actionFlagGet,0)
        Radio.setTXCR(RadioParam.actionFlagGet,0)
        Radio.setTXHeaderMode(RadioParam.actionFlagGet,0)
        Radio.setTxCrc(RadioParam.actionFlagGet,0)
        Radio.setTXPower(RadioParam.actionFlagGet,0)

        Radio.setRxFreq(RadioParam.actionFlagGet,0)
        Radio.setRXSF(RadioParam.actionFlagGet,0)
        Radio.setRXBW(RadioParam.actionFlagGet,0)
        Radio.setRXIQ(RadioParam.actionFlagGet,0)
        Radio.setRXCR(RadioParam.actionFlagGet,0)
        Radio.setRXHeaderMode(RadioParam.actionFlagGet,0)
        Radio.RxCrcCheck(RadioParam.actionFlagGet,0)

    def CallbackSetStandby(self):
        self.Radio.setStandby()

    def CallbackStartTX(self):   
        self.Radio.startTXCW()

    def CallbackSendPacket(self):
        self.CallbackWriteRadio()
        self.Radio.preparePacket(RadioParam.actionFlagSet,self.leHexInput.text())
        self.Radio.sendPacket()
    
    def fillTxFreq(self,freq):
        self.leTXFreq.setText(freq)

    def dissableAppWidgets(self):
        GuiManager.groupboxDisable(self.groupBox)
        # GuiManager.editTextDisable(self.leTXFreq)
        # GuiManager.editTextDisable(self.leRXFreq)
        # GuiManager.comboBoxDisable(self.cbTXSF)
        # GuiManager.comboBoxDisable(self.cbRXSF)
        # GuiManager.comboBoxDisable(self.cbTXBW)
        # GuiManager.comboBoxDisable(self.cbRXBW)
        # GuiManager.comboBoxDisable(self.cbTXIQ)
        # GuiManager.comboBoxDisable(self.cbRXIQ)
        # GuiManager.comboBoxDisable(self.cbTXCR)
        # GuiManager.comboBoxDisable(self.cbRXCR)
        # GuiManager.comboBoxDisable(self.cbTXHeader)
        # GuiManager.comboBoxDisable(self.cbRXHeader)
        # GuiManager.comboBoxDisable(self.cbTXCrc)
        # GuiManager.comboBoxDisable(self.cbRXCrc)
        # GuiManager.editTextDisable(self.leTXPower)
        # GuiManager.btnDisable(self.buttonWriteRadio)
        # GuiManager.btnDisable(self.buttonReadRadio)
        # GuiManager.btnDisable(self.btnStandby)
        # GuiManager.btnDisable(self.btnTXCW)

    def enableAppWidgets(self):
        GuiManager.groupboxEnable(self.groupBox)
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
        

    def isInt(self,str):
        try: 
            int(str)
            return True
        except ValueError:
            return False
       

class ThreadClass(QtCore.QThread):
    def __init__(self, mainwindow, parent = None):
        super(ThreadClass,self).__init__(parent)
        self.mainWin = mainwindow

    def run(self):
        #ptvsd.debug_this_thread()
        while True: 
            rxData = bytearray()
            result,rxData = USBLink.rxUSBRFLink(rxData,0)    
            #self.mainWin.leTXFreq.setText("uvodime")
    
            if result == "answerOk":
                #TODO make a dictionary
                self.CallbackUartRx(rxData) 
               # print("prijata data")
            
            #self.Radio.WhatIsYourName()

    def CallbackUartRx(self,rxData):
    
        cmd = ord(rxData[0])
        RadioOpCodeSwitcher.get(cmd)(rxData,Generator1,self.mainWin)


def AppWindow():

    app = QApplication(sys.argv)
    win = MainUIClass(Radio,USBLink, Generator1)

   # x = threading.Thread(target=TaskRxUart, args=(1,), daemon = True)  #daemon True - ukonci task jakmile zkonci main
   # x.start()

    win.show()
   
    sys.exit(app.exec_())


def TaskDataView(name):
    
    while True:
        time.sleep(.2)
        #print

# def main():
#     text = '### Program communicates with LoRa generator ###'
#     parser = argparse.ArgumentParser(description=text)
#     parser.add_argument("--op","-openPort", help="open serial COM port [x]")
#     parser.add_argument("--cp","-closePort", help="close serial COM port [x]")
#     parser.add_argument("--set", "--color","-color","--width","-width", help="nastavuji barvu")
#     parser.add_argument('integers', metavar='N', type=int, nargs='+',help='an integer for the accumulator')
#     parser.add_argument('--sum', dest='accumulate', action='store_const',const=sum, default=max,help='sum the integers (default: find the max)')

#     #parser.add_argument("--set", "--width","-color", help="nastavuji barvu")#
#     args = parser.parse_args()
    
#     if args.sum:
#         print(args.accumulate(args.integers))

#     if args.set:
#         print("Closing COM[%s]" % args.cp) 

#     if args.op:
#         print("Opening COM[%s]" % args.op)
    
#     if args.cp:
#         print("Closing COM[%s]" % args.cp)

if __name__ == "__main__":
   # main()
   
    AppWindow()

    #y =  threading.Thread(target=TaskDataView, args=(1,), daemon = True)  #daemon True - ukonci task jakmile zkonci main
    
    #x.join() # main zde vycka dokud nebude x dokonceno

    print("Main ends")
