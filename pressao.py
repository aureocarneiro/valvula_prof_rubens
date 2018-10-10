#!/usr/bin/python
# -*- coding: utf-8 -*-

# Necessary Python modules

import datetime
import math
import os
import pickle
import socket
import struct
import sys
import threading
import time
import logging

# Log File for exceptions

logging.basicConfig(filename='app.log',level=logging.INFO)

# UDP server port

UDP_PORT = int(sys.argv[1])

# Probe configuration
sample = 14400
PROBE_IP = sys.argv[2]
PROBE_PORT = 1000

# Maximum averaging time configuration for simple moving average (s)

MAXIMUM_AVERAGING_TIME = 120.

# Averaging time configuration for simple moving average (s). If there is a configuration file, this
# parameter is loaded from it. Otherwise, it is set to MAXIMUM_AVERAGING_TIME and stored in a new
# configuration file.

CONFIGURATION_FILE = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/Berthold-LB6420.data"

if (os.path.isfile(CONFIGURATION_FILE) == True):
    AVERAGING_TIME = pickle.load(open(CONFIGURATION_FILE, "rb"))
else:
    AVERAGING_TIME = MAXIMUM_AVERAGING_TIME
    pickle.dump(AVERAGING_TIME, open(CONFIGURATION_FILE, "wb"))

# Time series (raw data) for dose rate calculations

date_and_time = []
raw_data = []

# Time series of calculated dose rates

total_dose_rate = [0.0]*sample  # Parameter 19
gamma = [0.0]*sample                   # Parameter 31
total_neutron_rate = [0.0]*sample      # Parameter 34
high_energy_neutrons = [0.0]*sample    # Parameter 33


def time_sec(date_and_time):

    deltatime = (date_and_time[-1] - date_and_time[-2]).total_seconds()
    return deltatime

# Thread for reading data from the Berthold LB 6420 probe

def scanThread():

    # Global variables

    global date_and_time
    global raw_data
    global total_dose_rate
    global gamma
    global total_neutron_rate
    global high_energy_neutrons
    global sample
    global AVERAGING_TIME 

    # This creates a TCP/IP socket for communication to the probe

    # Loop

    while (True):

        try:

            time.sleep(1)

        except Exception as e:

            print(e)
            logging.error("Error occurred" + str(e))
            pass

# This launches the auxiliary thread of the program

auxiliary_thread = threading.Thread(target = scanThread)
auxiliary_thread.setDaemon(True)
auxiliary_thread.start()

# The program will sleep for 5 seconds before listening to requests from the EPICS IOC

time.sleep(5)

# This creates the UDP/IP socket

udp_server_address = ("0.0.0.0", UDP_PORT)
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server_socket.bind(udp_server_address)

# Loop

while (True):

    # Client (EPICS IOC) input data and address

    data, address = udp_server_socket.recvfrom(512)

    # Input processing. There is a simple protocol for communication to the client.

    if (data):

        # This software will not answer to any request until all its buffers are filled
#        print data

        if ((data[:14] == "AVERAGING_TIME") and (data[-1] == "\n")):
            if (len(data[:-1].split(" ")) == 2):
                try:
                    NEW_AVERAGING_TIME = int(data[:-1].split(" ")[1])
                except (ValueError):
                    answer = "INVALID_INPUT\n"
                    udp_server_socket.sendto(answer, address)
                    continue
                if (NEW_AVERAGING_TIME <= 1):
                    AVERAGING_TIME = NEW_AVERAGING_TIME
                    #pickle.dump(AVERAGING_TIME, open(CONFIGURATION_FILE, "wb"))
                    answer = "OK\n"
                else:
                    answer = "INVALID_INPUT\n"
                udp_server_socket.sendto(answer, address)
                continue

        if (data == "AVERAGING_TIME?\n"):
            answer = str(AVERAGING_TIME)
        else:
            answer = "INVALID_INPUT"

        answer += "\n"
        udp_server_socket.sendto(answer, address)
