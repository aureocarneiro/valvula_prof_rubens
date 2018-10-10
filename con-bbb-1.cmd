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

# Port for the conec

drvAsynIPPortConfigure("IPPort1", "127.0.0.1:17000 UDP")

# Records of the conec

cd ${IOC}
dbLoadRecords("database/pressao1.db", "PORT = IPPort1, PREFIX = VAC")

# Effectively initializes the IOC

cd iocBoot
iocInit
