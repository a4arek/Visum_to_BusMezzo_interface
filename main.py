##############################################################
############# Visum -> BusMezzo importer #####################
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
# or contact with main developer: Dr Oded Cats http://www.citg.tudelft.nl/en/about-faculty/departments/transport-and-planning/staff-information/dr-oded-cats/
#
######## usage:
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


from fileWriter import *
from verPreparator import *
from visumFilters import *
from visumAttributes import *
from BMcreator import *


def modify_network(Visum):
    modify_network_StopPoints(Visum)
    logPrinter("modify_network_StopPoints(Visum) finished")


def add_UDAs(Visum):

    addUDAs_Nodes(Visum)
    logPrinter("addUDAs_Nodes(Visum) finished")
    addUDAs_Links(Visum)
    logPrinter("addUDAs_Links(Visum) finished")
    addUDAs_LinkTypes(Visum)
    logPrinter("addUDAs_LinkTypes(Visum) finished")
    addUDAs_Turns(Visum)
    logPrinter("addUDAs_Turns(Visum) finished")

    addUDAs_LineRoutes(Visum)
    logPrinter("addUDAs_LineRoutes(Visum) finished")
    addUDAs_TimeProfiles(Visum)
    logPrinter("addUDAs_TimeProfiles(Visum) finished")
    addUDAs_VehicleJourneys(Visum)
    logPrinter("addUDAs_VehicleJourneys(Visum) finished")
    addUDAs_VehicleUnits(Visum)
    logPrinter("addUDAs_VehicleUnits(Visum) finished")
    addUDAs_StopPoints(Visum)
    logPrinter("addUDAs_StopPoints(Visum) finished")


def adjust_UDAs(Visum):
    adjust_Nodes(Visum)
    logPrinter("adjust_Nodes(Visum) finished")
    adjust_Links(Visum)
    logPrinter("adjust_Links(Visum) finished")
    adjust_Turns(Visum)
    logPrinter("adjust_Turns(Visum) finished")

    adjust_LineRoutes(Visum)
    logPrinter("adjust_LineRoutes(Visum) finished")
    adjust_TimeProfiles(Visum)
    print "adjust_TimeProfiles(Visum) finished"
    adjust_VehicleJourneys(Visum)
    print "adjust_VehicleJourneys(Visum) finished"
    adjust_StopPoints(Visum)
    print "adjust_StopPoints(Visum) finished"


def filter_Visum_Net(Visum):
    filter_Links(Visum)
    print "filter_Links(Visum) finished"
    filter_Turns(Visum)
    print "filter_Turns(Visum) finished"
    filter_LinkTypes(Visum)
    print "filter_LinkTypes(Visum) finished"


def make_BM(Visum):
    # Mezzo:
    make_Demand(Visum)
    print "make_Demand(Visum) finished"
    make_Hist_Times(Visum)
    print "make_Hist_Times(Visum) finished"
    make_Net(Visum)
    print "make_Net(Visum) finished"
    make_Turnings(Visum)
    print "make_Turnings(Visum) finished"
    make_Vehicle_Mix(Visum)
    print "make_Vehicle_Mix(Visum) finished"
    make_Routes(Visum)
    print "make_Routes(Visum) finished"

    # BusMezzo:
    make_Transit_Demand(Visum)
    print "make_Transit_Demand(Visum) finished"
    make_Transit_Fleet(Visum)
    print "make_Transit_Fleet(Visum) finished"
    make_Transit_Network(Visum)
    print "make_Transit_Network(Visum) finished"
    make_Transit_Routes(Visum)
    print "make_Transit_Routes(Visum) finished"


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
    :return: voidjj
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
        MAIN_PATH = "E:\BM"
        Visum = win32com.client.Dispatch('Visum.Visum')
        # Visum.LoadVersion(MAIN_PATH+".ver")
        Visum.LoadVersion("E:\BM_adjusted3.ver")

    main(Visum)










