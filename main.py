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
import win32com.client
from verPreparator import *
from visumFilters import *
from BMcreator import make_Demand, make_Hist_Times, make_Net, make_Turnings, make_Vehicle_Mix, make_Routes, \
    make_Transit_Demand, make_Transit_Fleet, make_Transit_Network, make_Transit_Routes, logPrinter
MAIN_PATH = ""



bm_log = ""  # main string to append logs





# def modify_network(Visum):
    # change the Visum network itself, to make it importable
    ### update 25-05-2018 - temporarily switched off (maybe we won't need this)
    # modify_network_StopPoints(Visum)
    # logPrinter("modify_network_StopPoints(Visum)",Visum=Visum)


def add_UDAs(Visum):
    addUDAs_Nodes(Visum)
    logPrinter("addUDAs_Nodes(Visum)",Visum=Visum)
    addUDAs_Links(Visum)
    logPrinter("addUDAs_Links(Visum)", Visum=Visum)
    addUDAs_Zones(Visum)
    logPrinter("addUDAs_Zones(Visum)", Visum=Visum)
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


def adjust_UDAs(Visum):
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
    logPrinter("adjust_StopPoints(Visum) finished", Visum=Visum)


def filter_Visum_Net(Visum):
    filter_Links(Visum)
    logPrinter("filter_Links(Visum)", Visum=Visum)
    filter_Turns(Visum)
    logPrinter("filter_Turns(Visum)", Visum=Visum)
    filter_LinkTypes(Visum)
    logPrinter("filter_LinkTypes(Visum)", Visum=Visum)


def make_BM(Visum):
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
    # modify_network(Visum)
    add_UDAs(Visum)
    adjust_UDAs(Visum)
    filter_Visum_Net(Visum)
    make_BM(Visum)


if __name__ == "__main__":
    # initialize VISUM and load the .ver file
    try:
        # from Visum
        Visum
        MAIN_PATH = MAIN_PATH = Visum.GetPath(2)
    except:
        # standalone
        MAIN_PATH = os.getcwd()
        #MAIN_PATH = "E:\BM"
        MAIN_PATH = MAIN_PATH+"\\test\\Krakow_test_I_obw\\"
        Visum = win32com.client.Dispatch('Visum.Visum')
        Visum.LoadVersion(MAIN_PATH+"KRK_test1.ver")
        Visum.SetPath(2,MAIN_PATH)
    Visum.Graphic.StopDrawing = True
    main(Visum)
    Visum.Graphic.StopDrawing = False


