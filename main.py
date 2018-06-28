##############################################################
##              PTV Visum -> BusMezzo importer              ##
##############################################################
#
# version 1.0 (beta), released: June 2018
# (c) Department of Transportation Systems, Cracow University of Technology, 2018
# (c) Department of Transport and Planning, Delft University of Technology, 2018
# Arkadiusz Drabicki, Rafal Kucharski, Oded Cats
# adrabicki [at] pk.edu.pl, rkucharski [at] pk.edu.pl, o.cats [at] tudelft.nl
# http://www.kst.pk.edu.pl, https://www.tudelft.nl/en/ceg/about-faculty/departments/transport-planning/
#
# feel free to use however you want, the software is provided as-is, without warranty of any kind
#
# for Visum see: http://vision-traffic.ptvgroup.com/en-us/products/ptv-visum/
# for BusMezzo see: https://odedcats.weblog.tudelft.nl/busmezzo/
# or contact the main BusMezzo developer:
# Dr Oded Cats - http://www.citg.tudelft.nl/en/about-faculty/departments/transport-and-planning/staff-information/dr-oded-cats/
#
#
#########################################
##               usage:                ##
#########################################
#
# run the script in Visum (drag & drop).
# BusMezzo files (.dat) will be created in the Version Project Directory of Visum (%MYDOCUMENTS% by default)
#
#
###############################################################
##     Before using the script, please read the following    ##
##     - VISUM INPUT NETWORK (.ver file) REQUIREMENTS:       ##
##     (otherwise the BM export will NOT work properly!)     ##
###############################################################
#
## LINKS:
# - Bidirectional LINKS can be used in Visum for intermediate LINEROUTE segments.
# - !! BUT !! - First and last STOPPOINTS (LINEROUTE segments) should always be placed on separate, unidirectional LINKS!
# - (This is to comply with the Mezzo representation of in/out {links} as an exit from / entry to the PuT depot.)
#
## LINKTYPES:
# - Visum LINKTYPE data -> mapped into the BM {sdfuncs} data.
# - BM {sdfunc} max. speed assumed from the v0_PrT_max parameter in Visum.
#
## ZONES / CONNECTORS:
# - ZONES will be imported as additional {stops} into BusMezzo.
# - CONNECTORS should be pinned directly to ACCESSNODES - these will be imported as additional {stop_distances}.
#
## STOPS / STOPAREAS / STOPPOINTS:
# - BusMezzo {stops} will be imported from the STOPAREA level - therefore, each STOPPOINT should be preferably assigned
#   to an individual STOPAREA (actually - that's highly recommended, otherwise BusMezzo network might not work properly).
# - STOPPOINTS in Visum should be defined as directed, on LINKS.
# - Important!! Separate STOPPOINTS are always required for PuT LINEROUTES which either:
#   commence from / pass through / or terminate at that particular STOP!
# - (E.g. Several LINEROUTES commencing from a given STOP can depart from the same STOPPOINT, but this S.P. should
#   always be separated from the STOPPOINT served by LINEROUTES which pass through that STOP.)
#
## LINES / LINEROUTES:
# - LINEROUTES will be imported into BusMezzo as {lines} assigned with different numbers (IDs)
#   - the original LINEROUTE name/no. will be saved under a separate attribute in the BM file.
# - Intermediate LINEROUTE segments can use shared LINK segments and STOPPOINTS with other LINEROUTES
#   - but: first and last LINEROUTE segment require separate LINKS and origin/destination-only STOPOINTS.
#
## TIMEPROFILES:
# - Only ONE TIMEPROFILE per each LINEROUTE (preferably, name = '1').
# - Remember to assign the VEHICLECOMBINATION to each TIMEPROFILE!
# - VEHICLE JOURNEYS need to be defined for each TIMEPROFILE / LINEROUTE.
# - BM {trips} format 2: TIMEPROFILES imported with exact departure times from the origin {stop}.
# - BM {trips} format 3: TIMEPROFILES imported with average service headways (rounded to 30 secs).
#
## VEHICLEUNITS / VEHICLECOMBINATIONS:
# - These should be defined and assigned to the specific TIMEPROFILES.
# - Make sure that Seat/TotalCapacity parameters are defined, and SeatCap <= TotalCap.
# - BM {vehicle_scheduling}: simplified driving roster assumed for now (single trips only).
#
## DEMAND MODEL:
# - PuT demand model from Visum will be imported into BusMezzo as {passenger_rates} format: 3.
#   (Zone-level OD from Visum -> mapped as stop-level OD into BM, with additional fictitious {stops} created.)
# - Make sure that demand matrix is assigned to the PuT DEMAND SEGMENT (in the OD DEMANDDATA settings).
# - Furthermore, check that StartTime and EndTime are defined in the SEGMENT TIME SERIES (these should be consistent
#   with the PuT assignment simulation time!).


import os
import win32com.client
import math
from verPreparator import *
from visumFilters import *
from BMcreator import make_Demand, make_Hist_Times, make_Net, make_Turnings, make_Vehicle_Mix, make_Routes, \
    make_Transit_Demand, make_Transit_Fleet, make_Transit_Network, make_Transit_Routes,\
    make_Allmoes, make_Assign, make_Assign_Links, make_V_Queues, make_Virtual_Links, make_NoIncident,\
    make_Server_Rates, make_Signal, make_Mezzo_Masterfile, make_Parameters, logPrinter
MAIN_PATH = ""



bm_log = ""  # main string to append logs


##################################
##       MAIN PROCEDURES        ##
##################################

### 1.
def modify_network(Visum):
    # change the Visum network itself, to make it importable
    modify_network_Zones(Visum)
    logPrinter("modify_network_Zones(Visum)",Visum=Visum)

### 2.
def add_UDAs(Visum):
    # add additional attributes in Visum network, necessary for subsequent BM export
    addUDAs_Nodes(Visum)
    logPrinter("addUDAs_Nodes(Visum)",Visum=Visum)
    addUDAs_Links(Visum)
    logPrinter("addUDAs_Links(Visum)", Visum=Visum)
    # addUDAs_Zones(Visum)
    # logPrinter("addUDAs_Zones(Visum)", Visum=Visum)
    addUDAs_Connectors(Visum)
    logPrinter("addUDAs_Connectors(Visum)", Visum=Visum)
    addUDAs_LinkTypes(Visum)
    logPrinter("addUDAs_LinkTypes(Visum)", Visum=Visum)
    addUDAs_Turns(Visum)
    logPrinter("addUDAs_Turns(Visum)", Visum=Visum)

    addUDAs_LineRoutes(Visum)
    logPrinter("addUDAs_LineRoutes(Visum)", Visum=Visum)
    addUDAs_TimeProfiles(Visum)
    logPrinter("addUDAs_TimeProfiles(Visum)", Visum=Visum)
    addUDAs_VehicleJourneys(Visum)
    logPrinter("addUDAs_VehicleJourneys(Visum)", Visum=Visum)
    addUDAs_VehicleUnits(Visum)
    logPrinter("addUDAs_VehicleUnits(Visum)", Visum=Visum)
    addUDAs_StopPoints(Visum)
    logPrinter("addUDAs_StopPoints(Visum)", Visum=Visum)

### 3.
def adjust_UDAs(Visum):
    # adjust specific Visum input attributes (to comply with the BM network requirements)
    adjust_Nodes(Visum)
    logPrinter("adjust_Nodes(Visum)", Visum=Visum)
    adjust_Links(Visum)
    logPrinter("adjust_Links(Visum)", Visum=Visum)
    adjust_Connectors(Visum)
    logPrinter("adjust_Connectors(Visum)", Visum=Visum)
    adjust_Turns(Visum)
    logPrinter("adjust_Turns(Visum)", Visum=Visum)

    adjust_LineRoutes(Visum)
    logPrinter("adjust_LineRoutes(Visum)", Visum=Visum)
    adjust_TimeProfiles(Visum)
    logPrinter("adjust_TimeProfiles(Visum)", Visum=Visum)
    adjust_VehicleJourneys(Visum)
    logPrinter("adjust_VehicleJourneys(Visum)", Visum=Visum)
    adjust_StopPoints(Visum)
    logPrinter("adjust_StopPoints(Visum)", Visum=Visum)

### 4.
def filter_Visum_Net(Visum):
    # filter the Visum network objects in case that's necessary
    filter_Links(Visum)
    logPrinter("filter_Links(Visum)", Visum=Visum)
    filter_Turns(Visum)
    logPrinter("filter_Turns(Visum)", Visum=Visum)
    # filter_LinkTypes(Visum)
    # logPrinter("filter_LinkTypes(Visum)", Visum=Visum)

### 5.
def make_BM(Visum):
    # produce the final BusMezzo input network (.dat) files

    # Mezzo:
    make_Demand(Visum)
    logPrinter("make_Demand(Visum)", Visum=Visum)
    make_Hist_Times(Visum)
    logPrinter("make_Hist_Times(Visum)", Visum=Visum)
    make_Net(Visum)
    logPrinter("make_Net(Visum)", Visum=Visum)
    make_Turnings(Visum)
    logPrinter("make_Turnings(Visum)", Visum=Visum)
    make_Vehicle_Mix(Visum)
    logPrinter("make_Vehicle_Mix(Visum)", Visum=Visum)
    make_Routes(Visum)
    logPrinter("make_Routes(Visum)", Visum=Visum)

    # BusMezzo:
    make_Transit_Demand(Visum)
    logPrinter("make_Transit_Demand(Visum)", Visum=Visum)
    make_Transit_Fleet(Visum)
    logPrinter("make_Transit_Fleet(Visum)", Visum=Visum)
    make_Transit_Network(Visum)
    logPrinter("make_Transit_Network(Visum)", Visum=Visum)
    make_Transit_Routes(Visum)
    logPrinter("make_Transit_Routes(Visum)", Visum=Visum)


    # other Mezzo files (fixed input) - not related to Visum network!:

    make_Allmoes(Visum)
    logPrinter("make_Allmoes(Visum)", Visum=Visum)
    make_Assign(Visum)
    logPrinter("make_Assign(Visum)", Visum=Visum)
    make_Assign_Links(Visum)
    logPrinter("make_Assign_Links(Visum)", Visum=Visum)
    make_NoIncident(Visum)
    logPrinter("make_NoIncident(Visum)", Visum=Visum)
    make_Server_Rates(Visum)
    logPrinter("make_Server_Rates(Visum)", Visum=Visum)
    make_Signal(Visum)
    logPrinter("make_Signal(Visum)", Visum=Visum)
    make_V_Queues(Visum)
    logPrinter("make_V_Queues(Visum)", Visum=Visum)
    make_Virtual_Links(Visum)
    logPrinter("make_Virtual_Links(Visum)", Visum=Visum)

    make_Mezzo_Masterfile(Visum)
    logPrinter("make_Mezzo_Masterfile(Visum)", Visum=Visum)
    make_Parameters(Visum)
    logPrinter("make_Parameters(Visum)", Visum=Visum)


##################################
##          MAIN CALL           ##
##################################

def main(Visum):
    """
    Main importer call, applied as a sequence of procedures
    :param Visum: COM object of PTV Visum
    :return: void
    """
    modify_network(Visum)
    add_UDAs(Visum)
    adjust_UDAs(Visum)
    filter_Visum_Net(Visum)
    make_BM(Visum)


if __name__ == "__main__":
    # initialize VISUM and load the .ver file
    if 'Visum' in globals():
        MAIN_PATH = Visum.GetPath(2)
    else:
        # standalone
        MAIN_PATH = os.getcwd()
        #MAIN_PATH = "E:\BM"
        MAIN_PATH = MAIN_PATH+"\\test\\Krakow_test_I_obw\\"
        Visum = win32com.client.Dispatch('Visum.Visum')
        Visum.LoadVersion(MAIN_PATH+"KRK_test1.ver")
        Visum.SetPath(2, MAIN_PATH)
    # Visum.Graphic.StopDrawing = True
    main(Visum)
    # Visum.Graphic.StopDrawing = False
