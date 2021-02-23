
RfBW = [7810,10420,15630,20830,31250,41670,62500,125000,250000,500000]
GeneratorNames = ["LoRaUSBStick","LoRaUSBAtten"]
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
    SystemType = 0

def intConstrain(data, min, max):
        num = int(data)
        if num < min:
            return (str(min))
        elif num > max:
            return (str(max))
        else:
           return data
  