#!/home/aureo/github/stream-ioc/bin/linux-x86_64/streamApp

# con-bbb-1.cmd

# Environment variables

epicsEnvSet("STREAMDEVICE", "/home/aureo/github/stream-ioc")
epicsEnvSet("IOC", "/home/aureo/github/stream-ioc")
epicsEnvSet("STREAM_PROTOCOL_PATH", "/home/aureo/github/stream-ioc/protocol")

# Database definition file

cd ${STREAMDEVICE}
dbLoadDatabase("dbd/streamApp.dbd")
streamApp_registerRecordDeviceDriver(pdbbase)

# Port for conc

drvAsynIPPortConfigure("IPPort2", "127.0.0.1:17001 UDP")

# Records of coc

cd ${IOC}
dbLoadRecords("database/pressao2.db", "PORT = IPPort2, PREFIX = VAC")

# Effectively initializes the IOC

cd iocBoot
iocInit

