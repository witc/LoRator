import numpy as np
import binascii
import time 
glEndian='big'
crc8tab = []
crc8tab = [
    0x00, 0xD5, 0x7F, 0xAA, 0xFE, 0x2B, 0x81, 0x54, 0x29, 0xFC, 0x56, 0x83, 0xD7, 0x02, 0xA8, 0x7D,
    0x52, 0x87, 0x2D, 0xF8, 0xAC, 0x79, 0xD3, 0x06, 0x7B, 0xAE, 0x04, 0xD1, 0x85, 0x50, 0xFA, 0x2F,
    0xA4, 0x71, 0xDB, 0x0E, 0x5A, 0x8F, 0x25, 0xF0, 0x8D, 0x58, 0xF2, 0x27, 0x73, 0xA6, 0x0C, 0xD9,
    0xF6, 0x23, 0x89, 0x5C, 0x08, 0xDD, 0x77, 0xA2, 0xDF, 0x0A, 0xA0, 0x75, 0x21, 0xF4, 0x5E, 0x8B,
    0x9D, 0x48, 0xE2, 0x37, 0x63, 0xB6, 0x1C, 0xC9, 0xB4, 0x61, 0xCB, 0x1E, 0x4A, 0x9F, 0x35, 0xE0,
    0xCF, 0x1A, 0xB0, 0x65, 0x31, 0xE4, 0x4E, 0x9B, 0xE6, 0x33, 0x99, 0x4C, 0x18, 0xCD, 0x67, 0xB2,
    0x39, 0xEC, 0x46, 0x93, 0xC7, 0x12, 0xB8, 0x6D, 0x10, 0xC5, 0x6F, 0xBA, 0xEE, 0x3B, 0x91, 0x44,
    0x6B, 0xBE, 0x14, 0xC1, 0x95, 0x40, 0xEA, 0x3F, 0x42, 0x97, 0x3D, 0xE8, 0xBC, 0x69, 0xC3, 0x16,
    0xEF, 0x3A, 0x90, 0x45, 0x11, 0xC4, 0x6E, 0xBB, 0xC6, 0x13, 0xB9, 0x6C, 0x38, 0xED, 0x47, 0x92,
    0xBD, 0x68, 0xC2, 0x17, 0x43, 0x96, 0x3C, 0xE9, 0x94, 0x41, 0xEB, 0x3E, 0x6A, 0xBF, 0x15, 0xC0,
    0x4B, 0x9E, 0x34, 0xE1, 0xB5, 0x60, 0xCA, 0x1F, 0x62, 0xB7, 0x1D, 0xC8, 0x9C, 0x49, 0xE3, 0x36,
    0x19, 0xCC, 0x66, 0xB3, 0xE7, 0x32, 0x98, 0x4D, 0x30, 0xE5, 0x4F, 0x9A, 0xCE, 0x1B, 0xB1, 0x64,
    0x72, 0xA7, 0x0D, 0xD8, 0x8C, 0x59, 0xF3, 0x26, 0x5B, 0x8E, 0x24, 0xF1, 0xA5, 0x70, 0xDA, 0x0F,
    0x20, 0xF5, 0x5F, 0x8A, 0xDE, 0x0B, 0xA1, 0x74, 0x09, 0xDC, 0x76, 0xA3, 0xF7, 0x22, 0x88, 0x5D,
    0xD6, 0x03, 0xA9, 0x7C, 0x28, 0xFD, 0x57, 0x82, 0xFF, 0x2A, 0x80, 0x55, 0x01, 0xD4, 0x7E, 0xAB,
    0x84, 0x51, 0xFB, 0x2E, 0x7A, 0xAF, 0x05, 0xD0, 0xAD, 0x78, 0xD2, 0x07, 0x53, 0x86, 0x2C, 0xF9]

uartSyncWord = 0xaabb
uartSyncWordSize = 2
uartHeaderSize = 4
uartCrcSize = 1

RadioOpCode = {
    "TxFreq": 1,
    "RxFreq": 2,
    "TxPower": 3,
    "TxSF": 4,
    "RxSF": 5,
    "TxBW": 6,
    "RxBW": 7,
    "TxIQ": 8,
    "RxIQ": 9,
    "TxCR": 10,
    "RxCR": 11,
    "TxHeaderMode": 12,
    "RxHeaderMode": 13,
    "TxCRC": 14,
    "RxCRC": 15,
    "Standby": 16,
    "StartTXCW": 17,
    "PreparePacket": 18,
    "AutoRepeating": 19,
    "SendPacket": 20,
    "StartRx": 21,
}


class RadioCmds:
    
    def __init__(self,port):
        self.port = port

    def setTxFreq(self,actionFlag, freq):
        serialPacket=[RadioOpCode["TxFreq"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian), freq.to_bytes(4,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def setRxFreq(self,actionFlag, freq):
        serialPacket=[RadioOpCode["RxFreq"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),freq.to_bytes(4,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def setTXPower(self,actionFlag, power):
        serialPacket=[RadioOpCode["TxPower"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),power.to_bytes(1,byteorder = glEndian,signed=True)]
        self.wrapPacket((serialPacket))

    def setTXSF(self,actionFlag, sf):
        serialPacket=[RadioOpCode["TxSF"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),sf.to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def setRXSF(self,actionFlag, sf):
        serialPacket=[RadioOpCode["RxSF"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),sf.to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def setTXBW(self,actionFlag, BW):
        serialPacket=[RadioOpCode["TxBW"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),BW.to_bytes(4,byteorder = glEndian)]
        self.wrapPacket(serialPacket)

    def setRXBW(self,actionFlag, BW):
        serialPacket=[RadioOpCode["RxBW"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),BW.to_bytes(4,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def setTXIQ(self,actionFlag, iq):
        serialPacket=[RadioOpCode["TxIQ"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),iq.to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))
    
    def setRXIQ(self, actionFlag, iq):
        serialPacket=[RadioOpCode["RxIQ"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),iq.to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))
    
    def setTXCR(self,actionFlag, cr):
        serialPacket=[RadioOpCode["TxCR"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),cr.to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def setRXCR(self,actionFlag, cr):
        serialPacket=[RadioOpCode["RxCR"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),cr.to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def setHeaderModeTx(self,actionFlag, mode):
        serialPacket=[RadioOpCode["TxHeaderMode"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),mode.to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def setHeaderModeRx(self,actionFlag, mode):
        serialPacket=[RadioOpCode["RxHeaderMode"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),mode.to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def RxCrcCheck(self,actionFlag,crc):
        serialPacket=[RadioOpCode["RxCRC"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),crc.to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))
    
    def setTxCrc(self,actionFlag,crc):
        serialPacket=[RadioOpCode["TxCRC"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),crc.to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def setStandby(self):
        serialPacket=[RadioOpCode["Standby"].to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def startTXCW(self):
        serialPacket=[RadioOpCode["StartTXCW"].to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))
   
    def preparePacket(self,actionFlag,packet):
        array = []
        for i in packet:
            array.append(bytes(i, 'utf-8'))
        serialPacket=[RadioOpCode["PreparePacket"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),len(packet).to_bytes(1,glEndian)]
        serialPacket+=array
        self.wrapPacket((serialPacket))

    def setAutoRepeating(self,actionFlag,repeatPeriod):
        serialPacket=[RadioOpCode["AutoRepeating"].to_bytes(1,byteorder = glEndian),actionFlag.to_bytes(1,byteorder = glEndian),repeatPeriod.to_bytes(4,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def sendPacket(self):
        cmdSendPacket = 19
        serialPacket=[cmdSendPacket.to_bytes(1,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    def startRx(self,timeout):
        cmdStartRx = 21
        serialPacket=[cmdStartRx.to_bytes(1,byteorder = glEndian),timeout.to_bytes(4,byteorder = glEndian)]
        self.wrapPacket((serialPacket))

    ###################################################################################################
    #               D E C O D I N G
    ###################################################################################################
    def saveTxFreq(self,rxData, generator,lorator):       
        frekvence= self.bytesToOrd(rxData[1:],4)
        generator.TXFreq = int.from_bytes(frekvence[0:4],byteorder='little')
        lorator.fillTxFreq(str(generator.TXFreq))
        print("Frekvence TX: {}".format(generator.TXFreq))

    def saveRxFreq(self,rxData, generator, lorator):
        frekvence= self.bytesToOrd(rxData[1:],4)
        generator.RXFreq = int.from_bytes(frekvence[0:4],byteorder='little')
        lorator.setRxFreq(generator.RXFreq)
        print("Frekvence RX: {}".format(generator.RXFreq))

    # def saveTxPower(self,rxData, generator):
    #     power = self.bytesToOrd(rxData[1:],1)
    #     generator.TXPower = int.from_bytes(power,byteorder='little')
    #     print("Tx Power: {}".format(generator.TXPower))

    # def saveTxSf(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.TXSF = int.from_bytes(sf,byteorder='little')
    #     print("TX SF: {}".format(generator.TXSF))

    # def saveRxSf(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.RXSF = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.RXSF))
    
    # def saveTxBW(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.TXBW = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.TXBW))

    # def saveRxBW(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.RXBW = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.RXBW))

    # def saveTxIq(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.TXIQ = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.TXIQ))

    # def saveRxIq(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.RXIQ = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.RXIQ))
 
    # def saveTxCR(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.TXCR = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.TXCR))

    # def saveRxCR(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.RXCR = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.RXCR))


    # def saveHeaderMTx(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.TXHeaderMode = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.TXHeaderMode))

    # def saveHeaderMRx(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.RXHeaderMode = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.RXHeaderMode))

    # def saveRxCRC(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.RXCRC = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.RXCRC))    

    # def saveTxCRC(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.TXCRC = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.TXCRC))    

    # def saveRadioStatus(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],1)
    #     generator.RXCRC = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.RXCRC))                       

    # def saveAutoRepeating(self,rxData, generator):
    #     sf = self.bytesToOrd(rxData[1:],4)
    #     generator.AutoRepeating = int.from_bytes(sf,byteorder='little')
    #     print("RX SF: {}".format(generator.AutoRepeating))        
###################################################################################################
    def wrapPacket(self,payload):
        finalPacket = bytearray()
        #sncWord
        finalPacket=self.listToByteArray([uartSyncWord.to_bytes(uartSyncWordSize,glEndian)])

        #header - spocitame delku payloadu
        bytePacket = bytearray()
        for i in payload:
            bytePacket+=i
        header = len(bytePacket)
        headerBarray = bytearray()
        rfu = 0

        finalPacket.extend(self.listToByteArray([header.to_bytes(1,glEndian)]))
        headerBarray.append(header)
        finalPacket.extend(self.listToByteArray([rfu.to_bytes(1,glEndian)]))
        headerBarray.append(rfu)
        finalPacket.extend(self.listToByteArray([rfu.to_bytes(1,glEndian)]))
        headerBarray.append(rfu)
        crcH=self.crc8(headerBarray,(3))
        finalPacket.extend(crcH.to_bytes(1,glEndian))
        
    
        #payload
        finalPacket.extend(bytePacket)

        crc=self.crc8(finalPacket,len(finalPacket))
        finalPacket+=crc.to_bytes(uartCrcSize,'little')
        #print(binascii.hexlify(finalPacket))

        # odeslu balik na uart
        self.port.ser.write(finalPacket)#bytePacket
        #time.sleep(0.01)

    def crc8(self,data : bytearray, size):
        crc = 0
        for i in range(0,size):
            crc = crc8tab[crc ^ data[i]]        
        return crc

    def listToByteArray(self,inputList):
            bytePacket = bytearray()
            for i in inputList:
                bytePacket+=i

            return bytePacket

    def bytesToOrd(self,data,size):
        prevedeno=[]
        for i in range(size):
            prevedeno.append(ord(data[i]))
        
        return prevedeno