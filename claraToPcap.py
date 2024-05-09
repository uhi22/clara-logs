
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
import os

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
    with open(inputFileName, encoding="Latin-1") as file:
        for line in file:
            print(line.strip())
            error=0
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
                        try:
                            t = float(strTime)/1000 # The time in the log is in milliseconds. We want seconds in the pcap.
                        except:
                            print("invalid time stamp " + strTime)
                            error += 1
                        strEthData = elementList[1].strip()
                        #print(strTime)
                        #print(strEthData)
                        for i in range(int(len(strEthData)/2)):
                            strByte = "0x" + strEthData[2*i:2*i+2]
                            #print(strByte)
                            try:
                                databyte = int(strByte, 0) # convert string like "0xAA" into number
                            except:
                                databyte = 0
                                print("invalid formatted hex number" + strByte)
                                error += 1
                            framedata.append(databyte)
                        if (error == 0):
                            print(strTime + " frame " + prettyHexMessage(framedata))
                            packet = Ether(raw(framedata)) # create a scapy packet from the byte list
                            packet.time = t # set the time stamp of the scapy packet
                            allpackets.append(packet) # add to the list of packets
                            packet.show()
                        else:
                            print("Ignoring this packet due to formatting error")
                        


# e.g. strClaraLogFileName = "2024-04-11_clara_PhiPhong_doug.claralog"
directory = "."
# iterate over files in the directory
for filename in os.listdir(directory):
    strClaraLogFileName = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(strClaraLogFileName):
        print(strClaraLogFileName)
        # check the file extension:
        if (strClaraLogFileName[-9:]==".claralog"):
            print("Will decode " + strClaraLogFileName)
            if (os.path.isfile(strClaraLogFileName + ".pcap")):
                print("output file " + strClaraLogFileName + ".pcap already exists. Nothing to do.")
            else:
                allpackets = [] # empty packet list at the beginning
                # parse the log file and collect the network packets
                readClaraLog(strClaraLogFileName)
                # write the collected packets into pcap file
                wrpcap(strClaraLogFileName + ".pcap", allpackets)
                print("Done. " + strClaraLogFileName + ".pcap written.")
