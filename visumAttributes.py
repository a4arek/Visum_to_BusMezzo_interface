# [visumAttributes] - sets of V-to-BM input and output attributes

##### Visum fixed input - user-defined attributes (UDAs):

# general network model
UDA_LinkTypes_V0_min = 0.1          # default minimum driving speed [m/s]
UDA_LinkTypes_K_max = 20.1          # default maximum vehicle density [veh/km/lane]
UDA_LinkTypes_K_min = 0.1           # default minimum vehicle density [veh/km/lane]
UDA_Turns_ServerID = 0              # default server ID [-]
UDA_Turns_LookBack = 40.0           # default look-back distance [m]

# PuT network model
UDA_VehicleUnits_VehLength = 6.0   # default PuT vehicle length [m]
UDA_VehicleUnits_DTFunc = 1         # default dwell-time function [-]
UDA_VehicleJourneys_NumTrips = 1    # default no. of trips [-] (simplified driving roster - quick-fix for now)
UDA_StopPoints_StopLength = 15.0    # default stop length [m]
UDA_StopPoints_StopType = 0         # default stop type [-]
UDA_StopPoints_CanOvertake = 0      # default overtaking capability [-]
UDA_StopPoints_RTI_Level = 3        # default RTI level (network-level = 3) [-]
UDA_StopPoints_DefaultRelPos = 0.49 # default stop relative position factor [-] (used in adjust_Nodes(Visum))
UDA_StopPoints_GateFlag = 0         # default gate flag - assumed none [-]

##### BusMezzo output attribute sets

# Mezzo network input
ATTR_LIST_NODES = ["No", "BM_NodeType", "XCoord", "YCoord"]
ATTR_LIST_LINKTYPES = ["No", "BM_SDID_Function", "BM_V0PrT", "BM_VminPrT", "BM_Kmax", "BM_KMin"]
ATTR_LIST_LINKS = ["BM_LinkID", "FromNodeNo", "ToNodeNo", "BM_Length", "NumLanes", "TypeNo"]
ATTR_LIST_LINKS_HISTTIMES = ["BM_LinkID", "BM_Hist_T0_Time"]
ATTR_LIST_TURNS = ["BM_TurnID", "ViaNodeNo", "BM_ServerID", "BM_InLinkID", "BM_OutLinkID", "BM_LookBack"]
ATTR_LIST_ROUTES = ["BM_RouteID", "BM_Start_Node_No", "BM_End_Node_No", "BM_No_Of_Links", "BM_List_Links"]

# Mezzo - output attribute types
TYPE_LIST_NODES = [int, int, float, float, int]
TYPE_LIST_LINKTYPES = [int, int, float, float, float, float]
TYPE_LIST_LINKS = [int, int, int, int, int, int]
TYPE_LIST_LINKS_HISTTIMES = [int, float]
TYPE_LIST_TURNS = [int, int, int, int, int, int]
TYPE_LIST_ROUTES = [int, int, int, int, str]

# BusMezzo network input
ATTR_LIST_STOPPOINTS = ["StopAreaNo", "Name", "BM_StopLinkID", "BM_Position", "BM_Length", "BM_StopType", "BM_CanOvertake",
                        "DefDwellTime", "BM_RTI_Level", "BM_GateFlag"]
ATTR_LIST_LINEROUTES = ["BM_RouteID", "BM_OppositeRouteID", "BM_RouteName", "BM_Start_Node_No", "BM_End_Node_No",
                        "BM_RouteID", "BM_VehType", "BM_HoldingStrategy", "BM_HoldingRatio", "BM_InitialOccupPerStop",
                        "BM_InitialOccupNumStops", "NumStopPoints", "BM_List_Stops", "NumStopPoints", "BM_List_Stops"]
ATTR_LIST_TIMEPROFILES_format3 = ["BM_TimeProfileID", "BM_No_of_RunTimes", "BM_List_RunTimes", "BM_First_Dispatch_Time",
                                  "BM_Headway", "Count:VehJourneys"]
ATTR_LIST_TIMEPROFILES_format2 = ["BM_TimeProfileID", "BM_No_of_RunTimes", "BM_List_RunTimes", "Count:VehJourneys",
                                  "BM_List_DispTimes"]
ATTR_LIST_VEHICLEJOURNEYS = ["BM_TripID", "BM_VehTypeID", "BM_NumTrips", "BM_List_Trips"]
ATTR_LIST_VEHICLEUNITS = ["No", "Name", "BM_VehLength", "SeatCap", "TotalCap", "BM_DTFunction"]
ATTR_LIST_TRANSITODPAIRS =["FromZone\BM_ZoneID", "ToZone\BM_ZoneID"]

# BusMezzo - output attribute types
TYPE_LIST_STOPPOINTS = [int, str, int, float, float, int, int, float, int, int]
TYPE_LIST_LINEROUTES = [int, int, str, int, int, int, int, int, float, int, int, int, str, int, str]
TYPE_LIST_TIMEPROFILES_format3 = [int, int, str, int, int, int]
TYPE_LIST_TIMEPROFILES_format2 = [int, int, str, int, str]
TYPE_LIST_VEHICLEJOURNEYS = [int, int, int, str]
TYPE_LIST_VEHICLEUNITS = [int, str, float, int, int, int]
TYPE_LIST_TRANSITODPAIRS = [int, int, int]

if __name__ == "__main__":
    pass

