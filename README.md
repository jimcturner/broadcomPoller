# broadcomPoller
James Turner 02/02/21
broadcom PIPAC211 snmp poller

A python script to query the Broadcom at the supplied URL for it's currently active Rx Streams. It will then take the supplied oid prefix and convert this into a 'complete' oid with a friendly name that can used (with the normal snmp_get commands) for each of the active streams
        
usage: 
	
	python broadcomSnmpOidGenerator [ip address of host] [snmp community string] [name of snmp parameter] [oid prefix]

	eg. broadcomSnmpOidGenerator "61.247.179.243" "abcdef" "DroppedPacketCount", ".1.3.6.1.4.1.22425.10.5.3.5.1.22"

might yield the following 

	{'Dhaka-W1-comb-Rx_DroppedPacketCount,': '.1.3.6.1.4.1.22425.10.5.3.5.1.22.2',
 	'Dhaka-W1-eth0-Rx_DroppedPacketCount,': '.1.3.6.1.4.1.22425.10.5.3.5.1.22.0',
 	'Dhaka-W1-eth1-Rx_DroppedPacketCount,': '.1.3.6.1.4.1.22425.10.5.3.5.1.22.1'}

To get the dropped packet count for stream Dhaka-W1-eth1-Rx, you could then run:

	snmpget 61.247.179.243 -v2c -c ib3oot3am .1.3.6.1.4.1.22425.10.5.3.5.1.22.1

which might return:

	iso.3.6.1.4.1.22425.10.5.3.5.1.22.1 = INTEGER: 40966

	(i.e 40966 packets lost)

Some other current known oid prefixes (for PIPA C211 SR 1.5.2 Firmware are:

	'unitName': '.1.3.6.1.4.1.22425.10.4.5',
	'DroppedPacketCount': '.1.3.6.1.4.1.22425.10.5.3.5.1.22',  # Packet arrived/lost outside of buffer window
	'LossOfConnectionCount': '.1.3.6.1.4.1.22425.10.5.3.5.1.23',  # (buffer underrun/hole in the audio)
	'PacketsReceived': '.1.3.6.1.4.1.22425.10.5.3.5.1.16'
        
Remember, these oids have to be suffixed with a .n where n is the stream no. to make them 'complete' - that's the purpose of broadcomPoller"

Prerequisites/dependancies:

	Python3
	sudo apt-get install libsnmp-dev snmp-mibs-downloader
	easysnmp (if this isn't installed, add it using pip3 install easysnmp)
              
