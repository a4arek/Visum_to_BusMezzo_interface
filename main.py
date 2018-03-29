##############################################################
#                    Visum -> BusMezzo importer              #
##############################################################
# (c) Department of Transport Systems, Cracow University of Technology, 2018
# (c) Department of Transport and Planning, Delft University of Technology, 2018
#  Arkadiusz Drabicki, Rafal Kucharski, Oded Cats
#  adrabicki@pk.edu.pl, rkucharski@pk.edu.pl, o.cats@tudelft.nl
#
# feel free to use however you want, the software is provided as-is, without warranty of any kind
#
# for Visum see: http://vision-traffic.ptvgroup.com/en-us/products/ptv-visum/
# for BusMezzo see: https://odedcats.weblog.tudelft.nl/busmezzo/
# or contact with main BusMezzo developer:
# Dr Oded Cats http://www.citg.tudelft.nl/en/about-faculty/departments/transport-and-planning/staff-information/dr-oded-cats/
#
# usage:
# run the script in Visum (drag & drop).
# BusMezzo files (.dat) will be created in the Version Project Directory of Visum (%MYDOCUMENTS% by default)
#
######## network rules:
# - NODES:
# - LINKS/LINKTYPES: min. length 27[m] if contains StopPointOnLink
# - TURNS:
# - ZONES/CONNECTORS:
# - STOPPOINTS/STOPAREAS:
# - STOPS:
# - LINES/LINEROUTES:
# - TIMEPROFILES: only ONE per each LineRoute (=1) / remember to assign VehicleCombinations
# - VEHICLEUNITS: only ONE per each VehicleCombination
# - OD MATRICES:
# - stops on links (DIRECTED!)
# - one connector per zone ONLY
# - connectors pinned directly to the stopArea access nodes
# - PuT: timetable coded (no headways)

import os

from fileWriter import *
from verPreparator import *
from visumFilters import *
from visumAttributes import *
from BMcreator import *

bm_log = ""  # main string to append logs


def modify_network(Visum):
    # change the Visum network itself, to make it importable
    modify_network_StopPoints(Visum)
    logPrinter("modify_network_StopPoints(Visum)")


def add_UDAs(Visum):

    addUDAs_Nodes(Visum)
    logPrinter("addUDAs_Nodes(Visum)")
    addUDAs_Links(Visum)
    logPrinter("addUDAs_Links(Visum)")
    addUDAs_LinkTypes(Visum)
    logPrinter("addUDAs_LinkTypes(Visum)")
    addUDAs_Turns(Visum)
    logPrinter("addUDAs_Turns(Visum)")

    addUDAs_LineRoutes(Visum)
    logPrinter("addUDAs_LineRoutes(Visum)")
    addUDAs_TimeProfiles(Visum)
    logPrinter("addUDAs_TimeProfiles(Visum)")
    addUDAs_VehicleJourneys(Visum)
    logPrinter("addUDAs_VehicleJourneys(Visum)")
    addUDAs_VehicleUnits(Visum)
    logPrinter("addUDAs_VehicleUnits(Visum)")
    addUDAs_StopPoints(Visum)
    logPrinter("addUDAs_StopPoints(Visum)")


def adjust_UDAs(Visum):
    adjust_Nodes(Visum)
    logPrinter("adjust_Nodes(Visum)")
    adjust_Links(Visum)
    logPrinter("adjust_Links(Visum)")
    adjust_Turns(Visum)
    logPrinter("adjust_Turns(Visum)")

    adjust_LineRoutes(Visum)
    logPrinter("adjust_LineRoutes(Visum)")
    adjust_TimeProfiles(Visum)
    logPrinter("adjust_TimeProfiles(Visum)")
    adjust_VehicleJourneys(Visum)
    logPrinter("adjust_VehicleJourneys(Visum)")
    adjust_StopPoints(Visum)
    logPrinter("adjust_StopPoints(Visum) finished")


def filter_Visum_Net(Visum):
    filter_Links(Visum)
    logPrinter("filter_Links(Visum)")
    filter_Turns(Visum)
    logPrinter("filter_Turns(Visum)")
    filter_LinkTypes(Visum)
    logPrinter("filter_LinkTypes(Visum)")


def make_BM(Visum):
    # Mezzo:
    make_Demand(Visum)
    logPrinter("make_Demand(Visum)")
    make_Hist_Times(Visum)
    logPrinter("make_Hist_Times(Visum)")
    make_Net(Visum)
    logPrinter("make_Net(Visum)")
    make_Turnings(Visum)
    logPrinter("make_Turnings(Visum)")
    make_Vehicle_Mix(Visum)
    logPrinter("make_Vehicle_Mix(Visum)")
    make_Routes(Visum)
    logPrinter("make_Routes(Visum)")

    # BusMezzo:
    make_Transit_Demand(Visum)
    logPrinter("make_Transit_Demand(Visum)")
    make_Transit_Fleet(Visum)
    logPrinter("make_Transit_Fleet(Visum)")
    make_Transit_Network(Visum)
    logPrinter("make_Transit_Network(Visum)")
    make_Transit_Routes(Visum)
    logPrinter("make_Transit_Routes(Visum)")


    # other Mezzo files (not related to Visum input):
    # make_Allmoes()
    # make_Assign()
    # make_Assign_Links()
    # make_No_Incident()
    # make_Parameters()
    # make_Server_Rates()
    # make_Signal()
    # make_V_Queues()
    # make_Virtual_Links()
    # make_Masterfile_Mezzo()


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
    # Visum.SaveVersion("E:\BM_adjusted3.ver")
    make_BM(Visum)



if __name__ == "__main__":
    # initialize VISUM and load the .ver file
    try:
        # from Visum
        Visum
        MAIN_PATH = Visum.GetPath(2)
    except:
        # standalone
        import win32com.client
        MAIN_PATH = os.getcwd()
        Visum = win32com.client.Dispatch('Visum.Visum')
        # Visum.LoadVersion(MAIN_PATH+".ver")
        Visum.LoadVersion("E:\BM_adjusted3.ver")

    main(Visum)










