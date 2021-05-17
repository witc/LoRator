from intelhex import IntelHex

#def writeImage(filename):

ih = IntelHex()  
ih.loadhex("STM32L071BootLoader.hex")
print("saddr :"+ str(ih.minaddr()), "endadr : " +str(ih.maxaddr()))

addr = ih.minaddr()
content = ih.todict()
abort = False
resend = 0

while addr <= ih.maxaddr():
 if not resend:
     data = []
     saddr = addr
     for i in range(16):
         try:
             data.append(content[addr])
         except KeyError:
             #if the HEX file doesn't contain a value for the given address
             #we "pad" it with 0xFF, which corresponds to the erase value
             data.append(0xFF)
         addr+=1
 try:
     if resend >= 3:
             abort = True
             break

#     self.serial.flushInput()
#     self.serial.write(self._create_cmd_message([CMD_WRITE] + map(ord, struct.pack("I", saddr))))
#     ret = self.serial.read(1)
#     if len(ret) == 1:
#         if struct.unpack("b", ret)[0] != ACK:
#             raise ProgramModeError("Write abort")
#     else:
#         raise TimeoutError("Timeout error")

#     encdata = self._encryptMessage(data)
#     self.serial.flushInput()
#     self.serial.write(encdata)
#     ret = self.serial.read(1)
#     if len(ret) == 1:
#         if struct.unpack("b", ret)[0] != ACK:
#             raise ProgramModeError("Write abort")
#     else:
#         raise TimeoutError("Timeout error")

#     yield {"loc": saddr, "resend": resend}
#     resend = 0
# except (TimeoutError, ProgramModeError):
#     resend +=1

#writeImage("STM32L071BootLoader.hex")
#ih = IntelHex()  
#ih.loadhex("STM32L071BootLoader.hex")
#print("saddr :"+ str(ih.minaddr()), "endadr : " +str(ih.maxaddr()))
#print("size: "+ str(ih.maxaddr()-ih.minaddr()))



    