#!/usr/bin/env python

import sys
import ftplib
import os
from ftplib import FTP
import time as Timer

def clear():

    if (os.name == 'nt'):    
        os.system('cls')
    else:
        os.system('clear')

def StopWatch(Value):

    ValueD = (((Value/365)/24)/60)
    Days = int (ValueD)

    ValueH = (ValueD-Days)*365
    Hours = int(ValueH)

    ValueM = (ValueH - Hours)*24
    Minutes = int(ValueM)

    ValueS = (ValueM - Minutes)*60
    Seconds = int(ValueS)

    Message = str(Days) + " Days " + str(Hours) + " Hours " + str(Minutes) + " Minutes " + str(Seconds) + " Seconds"

    return Message

def IsFile(FileName):

    Current = ftp.pwd()
    try:
        ftp.cwd(FileName)
    except:
        ftp.cwd(Current)
        return True
    ftp.cwd(Current)
    return False

def Download(Home, Path, Destination):

    print ""
    print "SOURCE:  " + Path.lower()

    try:
        ftp.cwd(Home + Path)
        os.chdir(Destination)
        os.makedirs(Destination[0:len(Destination)-1] + Path)
        print "TARGET:  " + Destination[0:len(Destination)-1].lower() + Path.lower()
    except OSError:
        print "TARGET:  " + Destination[0:len(Destination)-1].lower() + Path.lower()
        pass
    except ftplib.error_perm:
        print ""
        sys.exit("ERROR:   Could not change to " + Path + ".")

    print ""

    FTP_List = ftp.nlst()
    FTP_List.sort(key=lambda x: x.lower())

    Folders = []
    Files = []

    for Item in FTP_List:
        if IsFile(Item):
            Files.append(Item)
        else:
            Folders.append(Item)

    FTP_List = Files + Folders

    for Item in FTP_List:
        try:
            # Check if item is folder.
            ftp.cwd(Home + Path + Item + "/")
            # If yes, explore.
            print "________________________________________________________________________________"
            Download(Home, Path + Item + "/", Destination)
        except ftplib.error_perm:
            # If not, download item.
            os.chdir(Destination[0:len(Destination)-1] + Path)
            try:
                OSFile = open(os.path.join(Destination[0:len(Destination)-1] + Path, Item),"wb")
                ftp.retrbinary("RETR " + Item, OSFile.write)
                print "         " + Item.lower()
            except:
                print 'ERROR:   "' + Path + Item + '" is a folder or unauthorized.'
                OSFile.close()
                os.remove(Destination[0:len(Destination)-1] + Path + Item)

    return 

clear()

Site = sys.argv[1]
User = sys.argv[2]
Password = sys.argv[3]

ftp=FTP(Site)
ftp.login(User,Password)

Home = ftp.pwd()
Source = "/"
Destination = os.getcwd() + "/"

Start = Timer.time()
Download(Home,Source,Destination)
Stop = Timer.time()

print ""
print ""

print StopWatch(Stop-Start)

print ""
print ""
