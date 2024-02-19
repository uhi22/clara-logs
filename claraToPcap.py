
# ClaraToPcap

# This script reads clara log files and converts the contained Ethernet traffic into
# a pcap file. Afterwards they can be inspected e.g. in WireShark, and further
# converted e.g. with https://github.com/uhi22/pyPLC/blob/master/pcapConverter.py

# Example file: 2024-02-18_clara_alpi_lightbulb_ok.claralog
# [20] ETH will transmit: ffffffffffff02353069204388e10000a000b05200000000000000000000000000000000000000000000000000000000000000000000000000000000
# [1070] ETH rx HP: 023530692043046565ffffff88e10001a000b0520022254d41432d514341373030352d312e312e302e3733302d30342d32303134303831352d435300cccccccccccccccccc00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

# Precondition: Scapy is installed
# pip install scapy

from scapy.all import raw, wrpcap, Ether

# The list of packets:
allpackets = []



def twoCharHex(b):
    strHex = "%0.2X" % b
    return strHex


def prettyHexMessage(mybytearray, description=""):
    packetlength = len(mybytearray)
    strHex = ""
    for i in range(0, packetlength):
        strHex = strHex + twoCharHex(mybytearray[i]) + " "
    return description + "(" + str(packetlength) + "bytes) = " + strHex



def readClaraLog(inputFileName):
    with open(inputFileName) as file:
        for line in file:
            #print(line.strip())
            framedata = []
            if (line.find("ETH rx")>0) or (line.find("ETH will transmit")>0):
                #print(line.strip())
                elementList = line.strip().split(":")
                if (len(elementList)==2):
                    #print("ok, two elements")
                    strFirst = elementList[0].replace("]", "[")
                    timeElementList = strFirst.split("[")
                    if (len(timeElementList)==3):
                        #print("ok, 3 elements")
                        strTime = timeElementList[1]
                        t = float(strTime)/1000 # The time in the log is in milliseconds. We want seconds in the pcap.
                        strEthData = elementList[1].strip()
                        #print(strTime)
                        #print(strEthData)
                        for i in range(int(len(strEthData)/2)):
                            strByte = "0x" + strEthData[2*i:2*i+2]
                            #print(strByte)
                            databyte = int(strByte, 0) # convert string like "0xAA" into number
                            framedata.append(databyte)
                        print("frame " + prettyHexMessage(framedata))
                        packet = Ether(raw(framedata)) # create a scapy packet from the byte list
                        packet.time = t # set the time stamp of the scapy packet
                        allpackets.append(packet) # add to the list of packets
                        packet.show() 
                        

strClaraLogFileName = "2024-02-18_clara_TeslaV3_lightbulb_ok_at_second_try.claralog"
# parse the log file and collect the network packets
readClaraLog(strClaraLogFileName)
# write the collected packets into pcap file
wrpcap(strClaraLogFileName + ".pcap", allpackets)
print("Done. " + strClaraLogFileName + ".pcap written.")
