#!/usr/bin/python

import os, argparse

parser = argparse.ArgumentParser(prog='python PiStation.py', description='Broadcasts WAV/MP3 file over FM using RPI GPIO #4 pin.')
parser.add_argument("source")
parser.add_argument("-f", "--frequency", help="Set TX frequency. Acceptable range 87.1-108.2", type=float)
arg = parser.parse_args()

def main():
    os.system('clear')
    frequency = 0
    #frequency=freq()	
    print ("Welcome to PiStation!  \nVersion 1.0 \nGPLv3 License\n")    
    #This block is for setting default values for frequency in case argument is not provided
    if arg.frequency is None:
        frequency = raw_input("Enter the frequency (press Enter to set default frequency of 103.3 MHz) : ")
        if frequency == "":
            frequency = '103.3'
    elif 87.1 >= arg.frequency >= 108.2:
        print "Frequency argument out of range.";exit()
    else:
	frequency = str(arg.frequency)
    print frequency
    try:
        if ".mp3" in arg.source.lower():
            os.system("sox "+arg.source+" -r 22050 -c 1 -b 16 -t wav - | sudo ./fm_transmitter -f "+frequency+" - ")
        elif ".wav" in arg.source.lower():	    
	    os.system("sudo ./fm_transmitter -f "+frequency+" "+arg.source)
	elif "/" in arg.source:
	    for file in os.listdir(arg.source):
		if ".mp3" in file.lower():
		    os.system("sox "+arg.source+file+" -r 22050 -c 1 -b 16 -t wav - | sudo ./fm_transmitter -f "+frequency+" - ")
		elif ".wav" in file.lower():
		    os.system("sudo ./fm_transmitter -f "+frequency+" "+arg.source+file)
	elif "line" in arg.source:
	    os.system("arecord -D plughw:1,0 -c1 -d 0 -r 22050 -f S16_LE | sudo ./fm_transmitter -f "+frequency+" - ")
	else:
            print "That file extension is not supported."
            print "File name provided: %s" %arg.source
            raise IOError
    except Exception:
        print "Something went wrong. Halting."; exit()
    except IOError:
        print "There was an error regarding file selection. Halting."; exit()
    
if __name__ == '__main__':
    main()
