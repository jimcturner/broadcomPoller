#!/usr/bin/env python

#       Title: OID extractor for Broadcom PIPA C211 audio codecs - Queries the remote codec and generates the OIDs dynamically
#       Author: James Turner
#       Version: 001
#       Last Updated: 02/02/2021 but based on code written 19/07/2019
#       Notes: These OIDs are tested on FW SR1.5.2
import sys

# An object to hold the device connection parameters
class Config(object):
    def __init__(self, hostName, community, version=2, retries=0, timeout=5):
        self.hostName = hostName
        self.community = community
        self.version = version
        self.retries = retries
        self.timeout = timeout


def parsedSNMPBulkGet(snmp_session, oid):
    try:
        get_bulkResponse = snmp_session.get_bulk(oid)
        # Session.get_bulk() sometimes iterates beyond the specified oid tree, so need to check the oid of the object
        # returned is actually what we were asking for.

        # Trim leading '.1' from pattern because returned OID contains 'iso.' in it's place
        # We want to match against bit of the oid that follows the leading .1
        # Eg this will turn the string '.1.3.6.1.4.1.22425.10.5.3.5.1.2' into '.3.6.1.4.1.22425.10.5.3.5.1.2'
        trimmedOID = oid.strip('.1')

        # Create a search pattern containing the truncated version of the oid
        pattern = re.compile(trimmedOID)

        # create array to hold the 'pruned' response to bulk_get which will include only the oid tree we've requested
        prunedBulkResponse = []

        for item in get_bulkResponse:

            # Is this an OID we're interested in?
            if pattern.search(item.oid):
                # print "   oid matched: ", item.oid,": ",item.value
                # If item.oid has the correct oid, and to the new clean list
                prunedBulkResponse.append(item)

            # Return the oid tree object
        return prunedBulkResponse
    except Exception as e:
        raise Exception(f"parsedSNMPBulkGet(),  {e}")


# Polls the supplied device and returns a dictionary of OIDS
def getBroadcomOIDs(config):
    # OID templates as specified by the Broadcom specification
    sample_OID_LABELS = {
        'unitName': '.1.3.6.1.4.1.22425.10.4.5.0',
        'RxStream1DroppedPacketCount': '.1.3.6.1.4.1.22425.10.5.3.5.1.22.0',    # Packet arrived/lost outside of buffer window
        'RxStream2DroppedPacketCount': '.1.3.6.1.4.1.22425.10.5.3.5.1.22.1',
        'RxStreamCombinedDroppedPacketCount': '.1.3.6.1.4.1.22425.10.5.3.5.1.22.2',
        'RxStream1LossOfConnectionCount': '.1.3.6.1.4.1.22425.10.5.3.5.1.23.0',  # (buffer underrun/hole in the audio)
        'RxStream2LossOfConnectionCount': '.1.3.6.1.4.1.22425.10.5.3.5.1.23.1',
        'RxStreamCombinedLossOfConnectionCount': '.1.3.6.1.4.1.22425.10.5.3.5.1.23.2',
        'RxStream1PacketsReceived': '.1.3.6.1.4.1.22425.10.5.3.5.1.16.0',
        'RxStream2PacketsReceived': '.1.3.6.1.4.1.22425.10.5.3.5.1.16.1',
        'RxStreamCombinedPacketsReceived': '.1.3.6.1.4.1.22425.10.5.3.5.1.16.2',
    }

    # These are the templates for the dynamically generated OIDs
    # They are missing a final .x value that corresponds to an audio stream
    enabledStreamOID = '.1.3.6.1.4.1.22425.10.5.3.5.1.2'
    streamsStreamNameOID = '.1.3.6.1.4.1.22425.10.5.3.5.1.3'
    streamsDestinationIPAddressOID = '.1.3.6.1.4.1.22425.10.5.3.5.1.12'

    # Create an SNMP session to be used for our requests to the broadcom
    self.snmp_session = Session(
        hostname=config.hostName,
        community=config.community,
        version=config.version,
        retries=config.retries,
        timeout=config.timeout
    )

    ############# Get list of all streams (those that are enabled and disabled)

    # Do bulk get to get a list of the OIDs corresponding to the *enabled* streams
    enabledStreamsOIDList = parsedSNMPBulkGet(snmp_session, enabledStreamOID)
    return enabledStreamsOIDList

def main(argv):
    if len(argv) == 2:
        try:
            # Create Config object for the supplied device
            targetDevice = Config(argv[0], argv[1]) # Pass in ip address and community string
            broadcomOIDs = getBroadcomOIDs(targetDevice)
            print(f"{broadcomOIDs}")
        except Exception as e:
            print(f"Fatal error {e}")

    else:
        print("usage: python __main.__.py [ip address of host] [snmp community string]")


# Invoke main() method (entry point for Python script)
if __name__ == "__main__":
    # Call main and pass command line args to it (but ignore the first argument)
    main(sys.argv[1:])