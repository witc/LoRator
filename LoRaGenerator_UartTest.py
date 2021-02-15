import threading
from USB2Uart import USBSerialLink
from RadioFunctions import RadioCmds
import time
import argparse
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from LoRator import Ui_MainWindow



RfBW = [7810,10420,15630,20830,31250,41670,62500,125000,250000,500000]
actionFlagSet = 1
actionFlagSetGet = 2
actionFlagGet = 3

class USBRfLinkStruct:
    TXFreq = 0
    RXFreq = 0
    TXPower = 0
    TXSF  = 0
    RXSF = 0
    TXBW = 0
    RXBW = 0
    TXIQ = 0
    RXIQ = 0
    TXCR = 0
    RXCR = 0
    PreparedPacket = ""
    AutoRepeating = 0xFFFFFFFF  # nikdy
    RXCRC = False
    TXCRC = False
    TXHeaderMode = False
    RxHeaderMode = False
    RadioStatus = 0

Generator1 = USBRfLinkStruct()

USBLink = USBSerialLink()
if USBLink.openUSBRfLink() != "False":
    print("USB Generator connected")
Radio = RadioCmds(USBLink)


RadioOpCodeSwitcher = {
        1: Radio.saveTxFreq,
        2: Radio.saveRxFreq,
        # 3: Radio.saveTxPower,
        # 4: Radio.saveTxSf,
        # 5: Radio.saveRxSf,
        # 6: Radio.saveTxBW,
        # 7: Radio.saveRxBW,
        # 8: Radio.saveTxIq,
        # 9: Radio.saveRxIq,
        # 10: Radio.saveTxCR,
        # 11: Radio.saveRxCR,
        # 12: Radio.saveHeaderMTx,
        # 13: Radio.saveHeaderMRx,
        # 14: Radio.saveTxCRC,
        # 15: Radio.saveRxCRC,
        # 16: Radio.saveRadioStatus,
        # 17: Radio.saveRadioStatus,
        # #18: Radio.savePreparedPacket,
        # 19: Radio.saveAutoRepeating,
        # 20: Radio.saveRadioStatus,
        # 21: Radio.saveRadioStatus,
    }

class LoRator(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,radio, generator ,parent=None):
        super(LoRator, self).__init__(parent)
        self.setupUi(self)
        self.Radio = radio
        self.Generator = generator

        self.pushButton.clicked.connect(self.CallbackReadRadio)
        self.pushButton_2.clicked.connect(self.CallbackWriteRadio)
        self.pushButton_3.clicked.connect(self.CallbackSetStandby)
        self.pushButton_5.clicked.connect(self.CallbackStartTX)
        
    def CallbackWriteRadio(self):
        Radio.setTxFreq(actionFlagSetGet,int(self.lineEdit.text()))
      #n  Radio.setRxFreq(actionFlagSet,int(self.lineEdit_2.setText(str(freq))))
       # Radio.setRXSF(actionFlagSet,860222333)
       # Radio.setTXSF(actionFlagSet,860222333)
        
       
    def CallbackReadRadio(self):
        Radio.setTxFreq(actionFlagGet,0)
        Radio.setRxFreq(actionFlagGet,0)
        

    def CallbackSetStandby(self):
        self.Radio.setStandby()

    def CallbackStartTX(self):   
        self.Radio.startTXCW()

    
    def fillTxFreq(self,freq):
        self.lineEdit.setText(freq)

    
def CallbackUartRx(rxData):
  
    cmd = ord(rxData[0])
    RadioOpCodeSwitcher.get(cmd)(rxData,Generator1,LoRator)
   
     
def TaskRxUart(name):

    while True: 
        #cnt+=869525000
        rxData = bytearray()
        result,rxData = USBLink.rxUSBRFLink(rxData,0)    
        
        if result == "answerOk":
            #TODO make a dictionary
            CallbackUartRx(rxData)

def AppWindow():

    app = QApplication(sys.argv)
    win = LoRator(Radio, Generator1)

    x = threading.Thread(target=TaskRxUart, args=(1,), daemon = True)  #daemon True - ukonci task jakmile zkonci main
    x.start()

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
