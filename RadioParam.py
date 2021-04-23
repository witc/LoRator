import math

RfBW = [7810,10420,15630,20830,31250,41670,62500,125000,250000,500000]
GeneratorNames = ["LoRaUSBStick ","LoRaGenerator "]
radioMinFreq = 150000000
radioMaxFreq = 960000000
radioMinPower = -9
radioMaxPower = 22

actionFlagSet = 1
actionFlagSetGet = 2
actionFlagGet = 3

class RadioParam:
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
    TargetName = ''
    TargetMCU = ''
    TargetRadio = ''
    TargetMinPower = ''
    TargetMaxPower = ''
    SystemType = 0
    SystemID = 0

def intConstrain(data, min, max):
        num = int(data)
        if num < min:
            return (str(min))
        elif num > max:
            return (str(max))
        else:
           return str(int(data))

def calcNOfSymbol(crc,preambleSize, payloadSize, sf, header,cr):

    if crc == 1:
        NbitCrc = 16
    else:
        NbitCrc = 0

    if header == 1:
        NsymbolHeader = 20
    else:
        NsymbolHeader = 0

    if cr == 45:
        crN = 1
    elif cr == 46:
        crN = 2
    elif cr == 47:
        crN = 3
    elif cr == 48:
        crN = 4

    if sf == 5 or sf == 6:
        Nsymbol = preambleSize + 6.25 + 8 + math.ceil(((max(8*payloadSize+NbitCrc -4*sf + NsymbolHeader,0)/(4*sf))))*(crN+4)

    else:
        Nsymbol = preambleSize + 4.25 + 8 + math.ceil(((max(8*payloadSize+NbitCrc -4*sf + NsymbolHeader,0)/(4*sf))))*(crN+4)

    return Nsymbol

def getTOA( sf,bw, cr, header,crc,preambleSize, payloadSize):
        #sf,bw,cr,header,crc,preamble,payload
        preambleSize +=4.25
        TOA = ((2**sf)/bw) * calcNOfSymbol(crc,preambleSize, payloadSize, sf, header,cr)
        
        return TOA*1000