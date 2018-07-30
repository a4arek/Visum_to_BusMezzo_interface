# [BMcreator] - final part of the V-BM importer - produce output BusMezzo network (.dat) files

import numpy as np

from visumAttributes import *
from fileWriter import *


#####################################################
## 5. PRODUCE OUTPUT BUSMEZZO (.DAT) NETWORK FILES ##
#####################################################

## Mezzo input files

def make_Demand(Visum):
    MAIN_PATH = Visum.GetPath(2)

    od_list = Visum.Lists.CreateLineRouteList
    od_list.AddColumn("BM_Start_Node_No")
    od_list.AddColumn("BM_End_Node_No")

    in_list = od_list.SaveToArray()

    zeros_column = np.zeros((len(in_list),1))
    in_list = np.hstack((in_list, zeros_column))
    ATTR_LIST_ODPAIRS = np.vstack({tuple(od_path) for od_path in in_list})
    TYPE_LIST_ODPAIRS = [int, int, int]

    file = open(MAIN_PATH+'demand.dat', 'w')
    file.write("od_pairs: " + str(len(ATTR_LIST_ODPAIRS)) + LINE_NEW)
    file.write("scale: 1.0" + LINE_NEW)
    addTable(file,"",ATTR_LIST_ODPAIRS, TYPE_LIST_ODPAIRS)
    file.close()

def make_Hist_Times(Visum):
    MAIN_PATH = Visum.GetPath(2)

    file = open(MAIN_PATH+'\\histtimes.dat', 'w')
    file.write("links: " + str(Visum.Net.Links.CountActive) + LINE_NEW)
    file.write("periods: 1" + LINE_NEW)
    file.write("periodlength: 3600" + LINE_NEW)
    addTable(file, "", Visum.Net.Links.GetMultipleAttributes(ATTR_LIST_LINKS_HISTTIMES, True), TYPE_LIST_LINKS_HISTTIMES)
    file.close()

def make_Net(Visum):
    MAIN_PATH = Visum.GetPath(2)

    file = open(MAIN_PATH+'\\net.dat', 'w')
    addTable(file,"servers",[[0,0,0,0,0]], [int, int, int, int, int])
    node_table = list()
    # handle exception issue #6

    for i, node in enumerate(list(Visum.Net.Nodes.GetMultipleAttributes(ATTR_LIST_NODES))):
        n = list(node)
        if int(node[1]) == 2:
            n.append(0)
        node_table.append(tuple(n))
    addTable(file, "nodes", node_table, TYPE_LIST_NODES)
    addTable(file,"sdfuncs", Visum.Net.LinkTypes.GetMultipleAttributes(ATTR_LIST_LINKTYPES, True), TYPE_LIST_LINKTYPES)
    addTable(file,"links", Visum.Net.Links.GetMultipleAttributes(ATTR_LIST_LINKS, True), TYPE_LIST_LINKS)
    file.close()

def make_Turnings(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\turnings.dat', 'w')
    addTable(file, "turnings",Visum.Net.Turns.GetMultipleAttributes(ATTR_LIST_TURNS, True), TYPE_LIST_TURNS)
    file.write("giveways:0")
    file.close()

def make_Vehicle_Mix(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\vehiclemix.dat', 'w')
    file.write("vtypes: 5" + LINE_NEW)
    file.write(LIST_BEGIN + "1 NewCars 0.410 6.0" + LIST_END_NL)
    file.write(LIST_BEGIN + "2 OldCars 0.400 6.0" + LIST_END_NL)
    file.write(LIST_BEGIN + "3 Taxis 0.100 6.0" + LIST_END_NL)
    file.write(LIST_BEGIN + "5 Trucks 0.090 16.0" + LIST_END_NL)
    file.write(LIST_BEGIN + "4 Buses 0.000 13.0" + LIST_END_NL)
    file.close()

def make_Routes(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\routes.dat', 'w')
    addTable(file, "routes",Visum.Net.LineRoutes.GetMultipleAttributes(ATTR_LIST_ROUTES), TYPE_LIST_ROUTES)
    file.close()


## BusMezzo input files

def make_Transit_Demand(Visum):
    MAIN_PATH = Visum.GetPath(2)

    MatNo = str(int(Visum.Net.DemandSegments.ItemByKey("X").ODMatrix.AttValue("No")))

    ### previous version - passenger demand derived from the PuT stop-level matrix:

    ### !!! make sure that the [StopPoint-level PuT matrix] is already calculated in Visum !!! ###
    ### Calculate -> General procedure settings -> PuT settings -> Assignment -> ...           ###
    ### ... -> tick [Save the volume matrix between stop points on the path level] -> ...      ###
    ### ... -> run [PuT Assignment] -> save the .ver file                                      ###

    # od_list = Visum.Lists.CreatePuTStopPointVolumeMatrixPathList
    # od_list.AddColumn("FromStopPointNo")
    # od_list.AddColumn("ToStopPointNo")
    # od_list.AddColumn("Volume(AP)")

    # ATTR_LIST_TRANSITODPAIRS = od_list.SaveToArray()
    # TYPE_LIST_TRANSITODPAIRS = [int, int, int]

    file = open(MAIN_PATH+'\\transit_demand.dat', 'w')
    file.write("passenger_rates: " + str(Visum.Net.ODPairs.Count) + LINE_NEW)
    file.write("format: 3" + LINE_NEW)

    ATTR_LIST_TRANSITODPAIRS.append("MatValue({})".format(MatNo))
    addTable(file, "", Visum.Net.ODPairs.GetMultipleAttributes(ATTR_LIST_TRANSITODPAIRS), TYPE_LIST_TRANSITODPAIRS)
    file.close()

def make_Transit_Fleet(Visum):
    MAIN_PATH = Visum.GetPath(2)

    file = open(MAIN_PATH + '\\transit_fleet.dat', 'w')
    ATTR_LIST_DWELL_TIME_FUNCTIONS = [[1,11,0.0,2.0,2.0,2.0,0.0,2.0],[2,11,0.0,2.0,2.0,2.0,0.0,2.0]]
    TYPE_LIST_DWELL_TIME_FUNCTIONS = [int, int, float, float, float, float, float, float]
    addTable(file, "dwell_time_functions",ATTR_LIST_DWELL_TIME_FUNCTIONS, TYPE_LIST_DWELL_TIME_FUNCTIONS)
    addTable(file, "vehicle_types",Visum.Net.VehicleUnits.GetMultipleAttributes(ATTR_LIST_VEHICLEUNITS), TYPE_LIST_VEHICLEUNITS)
    addTable(file, "vehicle_scheduling",Visum.Net.VehicleJourneys.GetMultipleAttributes(ATTR_LIST_VEHICLEJOURNEYS), TYPE_LIST_VEHICLEJOURNEYS)
    file.close()

def make_Transit_Network(Visum):

    # STOPS data:
    MAIN_PATH = Visum.GetPath(2)

    file = open(MAIN_PATH + '\\transit_network.dat', 'w')
    # addTable(file, "stops",Visum.Net.StopPoints.GetMultipleAttributes(ATTR_LIST_STOPPOINTS, True), TYPE_LIST_STOPPOINTS)
    addTable(file, "stops",Visum.Net.StopAreas.GetMultipleAttributes(ATTR_LIST_STOPAREAS, True), TYPE_LIST_STOPAREAS)

    # STOPS_DISTANCES{...} - list export and processing steps:

    ### 1. STOP_AREA_TRANSFERS - within-stop walking links
    # 1a. create StopArea transfer matrix
    walk_list = Visum.Lists.CreateStopTransferWalkTimeList
    walk_list.AddColumn("FromStopAreaNo")
    walk_list.AddColumn("ToStopAreaNo")
    walk_list.AddColumn("Time(W)")
    walk_list.SetObjects(True)
    # walk_list.AddColumn("ToStopAreaNo",GroupOrAggrFunction=10)
    # walk_list.AddColumn("Time(W)",GroupOrAggrFunction=10)
    in_list = np.array(walk_list.SaveToArray())

    # 1b. remove duplicates and transfers within the same stop
    for row in in_list:
        if row[0] == row[1]:
            row[0:2] = 0
        else:
            pass
    in_list = in_list[~(in_list==0).all(1)]

    # 1c. finally - prepare a BusMezzo-adequate input list
    out_list = dict()
    from_stops = [r[0] for r in in_list]
    for r in in_list:
        if r[0] in out_list.keys():     # apparently this is not accessed
            out_list[r[0]][-1].append([r[1], r[2]])
        else:
            toAdd = []
            toAdd.append([r[1], r[2]])
            out_list[r[0]] = [[r[0], from_stops.count(r[0]), toAdd[0]]]

    ATTR_LIST_STOPTRANSFERS = out_list.values()
    # quick-fix -  remove outer brackets
    ATTR_LIST_STOPTRANSFERS = [i[0] for i in ATTR_LIST_STOPTRANSFERS]

    ### 2. ORIGIN/DESTINATION TRANSFERS - map Connectors(Zone<=>Stop) into additional walking links

    # 2a. create list of Connector walking links
    conn_list = Visum.Lists.CreateConnectorList
    conn_list.AddColumn("BM_OrigPointData")
    conn_list.AddColumn("BM_DestPointData")
    conn_list.AddColumn("T0_TSys(W)")
    conn_list.SetObjects(True)
    in_conn_list = [[str(x) for x in row] for row in np.array(conn_list.SaveToArray())]
    out_conn_list = []

    # 2b. prepare a BusMezzo-adequate input list
    for connector in in_conn_list:
        if connector[0] == '':      # skip non-origin connectors
            pass
        else:                       # add origin connectors' data only
            zone_connections = []
            orig_point = connector[0]
            dest_points = connector[1].split(',')
            conn_walk_time = connector[2]
            num_connections = len(dest_points)
            stop_connections = []
            for i in dest_points:
                stop_connections.append([int(i), float(conn_walk_time)])
            zone_connections.append(int(orig_point))
            zone_connections.append(num_connections)
            for list_of_walk_connections in stop_connections:
                zone_connections.append(list_of_walk_connections)

        out_conn_list.append(zone_connections)

    ATTR_LIST_CONNECTORS = out_conn_list

    ### 3. MERGE STOP-TRANSFER LISTS

    input_stop_transfers_list = ATTR_LIST_STOPTRANSFERS
    input_stop_transfers_list.extend(ATTR_LIST_CONNECTORS)
    origin_set = sorted(set([origin[0] for origin in input_stop_transfers_list]))
    output_stop_transfers_list = [[row, 0] for row in np.array(origin_set)]

    # merge duplicate entries for source connections and prepare final output list
    for source_connections in input_stop_transfers_list:
        row_id = find_source_point(source_connections, output_stop_transfers_list)
        output_stop_transfers_list[row_id][1] += source_connections[1]
        for connectors in source_connections[2:]:
            output_stop_transfers_list[row_id].append(connectors)

    ### 4. WRITE FINAL OUTPUT TO .DAT FILE

    ATTR_LIST_STOPDISTANCES = output_stop_transfers_list
    TYPE_LIST_STOPDISTANCES = [int, int, int, float]
    stops_dist_length = str(len(ATTR_LIST_STOPDISTANCES))

    file.write("stops_distances: " + stops_dist_length + LINE_NEW)
    file.write("format: 1" + LINE_NEW)
    addTable(file, "", ATTR_LIST_STOPDISTANCES, TYPE_LIST_STOPDISTANCES)

    ### 5. STOPS_WALKING_TIMES - to be updated soon
    file.write("stops_walking_times: 0" + LINE_NEW)

    # LINES / TRIPS data:

    file.write("lines: " + str(Visum.Net.LineRoutes.Count) + LINE_NEW)
    addTable(file,"",Visum.Net.LineRoutes.GetMultipleAttributes(ATTR_LIST_LINEROUTES), TYPE_LIST_LINEROUTES)
    file.write("trips: " + str(Visum.Net.LineRoutes.Count) + LINE_NEW)
    # if trips format:2
    # file.write("format: 2" + LINE_NEW)
    # addTable(file,"",Visum.Net.TimeProfiles.GetMultipleAttributes(ATTR_LIST_TIMEPROFILES_format2), TYPE_LIST_TIMEPROFILES_format2)
    # if trips format:3
    file.write("format: 3" + LINE_NEW)
    addTable(file,"",Visum.Net.TimeProfiles.GetMultipleAttributes(ATTR_LIST_TIMEPROFILES_format3), TYPE_LIST_TIMEPROFILES_format3)

    file.write("travel_time_disruptions: 0" + LINE_NEW)
    file.close()

def make_Transit_Routes(Visum):
    MAIN_PATH = Visum.GetPath(2)

    file = open(MAIN_PATH + '\\transit_routes.dat', 'w')
    addTable(file, "routes", Visum.Net.LineRoutes.GetMultipleAttributes(ATTR_LIST_ROUTES), TYPE_LIST_ROUTES)
    file.close()


## other M/BM files - fixed input

def make_Allmoes(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\allmoes.dat', 'w')
    file.write("MOES" + LINE_NEW)
    file.close()

def make_Assign(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\assign.dat', 'w')
    file.write("no_obs_links: 0" + LINE_NEW)
    file.write("no_link_pers: 12" + LINE_NEW)
    file.write(LIST_BEGIN + "link_period: 0" + LIST_END_NL)
    file.write(LIST_BEGIN + "link_period: 1" + LIST_END_NL)
    file.write(LIST_BEGIN + "link_period: 2" + LIST_END_NL)
    file.write(LIST_BEGIN + "link_period: 3" + LIST_END_NL)
    file.write(LIST_BEGIN + "link_period: 4" + LIST_END_NL)
    file.write(LIST_BEGIN + "link_period: 5" + LIST_END_NL)
    file.write(LIST_BEGIN + "link_period: 6" + LIST_END_NL)
    file.write(LIST_BEGIN + "link_period: 7" + LIST_END_NL)
    file.write(LIST_BEGIN + "link_period: 8" + LIST_END_NL)
    file.write(LIST_BEGIN + "link_period: 9" + LIST_END_NL)
    file.write(LIST_BEGIN + "link_period: 10" + LIST_END_NL)
    file.write(LIST_BEGIN + "link_period: 11" + LIST_END_NL)
    file.close()

def make_V_Queues(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\v_queues.dat', 'w')
    file.write("" + LINE_NEW)
    file.close()

def make_Virtual_Links(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\virtuallinks.dat', 'w')
    file.write("virtuallinks: 0" + LINE_NEW)
    file.close()

def make_NoIncident(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\noincident.dat', 'w')
    file.write("sdfuncs: 0" + LINE_NEW)
    file.write("incidents: 0" + LINE_NEW)
    file.write("parameters: 4" + LINE_NEW)
    file.write(LIST_BEGIN + "1.0 0.1" + LIST_END_NL)
    file.write(LIST_BEGIN + "1.0 0.1" + LIST_END_NL)
    file.write(LIST_BEGIN + "1.0 0.1" + LIST_END_NL)
    file.write(LIST_BEGIN + "1.0 0.1" + LIST_END_NL)
    file.write("X1:" + LINE_NEW)
    file.write(LIST_BEGIN + "2.0 0.5" + LIST_END_NL)
    file.close()

def make_Assign_Links(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\assign_links.dat', 'w')
    file.write("no_obs_links: 0" + LINE_NEW)
    file.write(LIST_BEGIN + " " + LIST_END)
    file.close()

def make_Server_Rates(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\serverrates.dat', 'w')
    file.write("rates: 0" + LINE_NEW)
    file.close()

def make_Signal(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\signal.dat', 'w')
    file.write("controls: 0" + LINE_NEW)
    file.close()


## Mezzo masterfile (fixed input)

def make_Mezzo_Masterfile(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\masterfile.mezzo', 'w')

    file.write("	#input_files	" + LINE_NEW)
    file.write("	network= net.dat	" + LINE_NEW)
    file.write("	turnings= turnings.dat	" + LINE_NEW)
    file.write("	signals= signal.dat	" + LINE_NEW)
    file.write("	histtimes= histtimes.dat	" + LINE_NEW)
    file.write("	routes= routes.dat	" + LINE_NEW)
    file.write("	demand= demand.dat	" + LINE_NEW)
    file.write("	incident= noincident.dat	" + LINE_NEW)
    file.write("	vehicletypes= vehiclemix.dat	" + LINE_NEW)
    file.write("	virtuallinks= virtuallinks.dat	" + LINE_NEW)
    file.write("	serverrates= serverrates.dat	" + LINE_NEW)
    file.write("	#output_files	" + LINE_NEW)
    file.write("	linktimes= output/linktimes.dat	" + LINE_NEW)
    file.write("	output= output/output.dat	" + LINE_NEW)
    file.write("	summary= output/summary.dat	" + LINE_NEW)
    file.write("	speeds= output/speeds.dat	" + LINE_NEW)
    file.write("	inflows= output/inflows.dat	" + LINE_NEW)
    file.write("	outflows= output/outflows.dat	" + LINE_NEW)
    file.write("	queuelengths= output/queuelengths.dat	" + LINE_NEW)
    file.write("	densities= output/densities.dat	" + LINE_NEW)
    file.write("	#scenario	" + LINE_NEW)
    file.write("	starttime= 0	" + LINE_NEW)
    file.write("	stoptime= 10800	" + LINE_NEW)
    file.write("	calc_paths= 0	" + LINE_NEW)
    file.write("	traveltime_alpha= 0.4	" + LINE_NEW)
    file.write("	parameters= parameters.dat	" + LINE_NEW)
    file.write("	nobackground= 	" + LINE_NEW)

    file.close()


## Parameters' file (fixed input)

def make_Parameters(Visum):
    MAIN_PATH = Visum.GetPath(2)
    file = open(MAIN_PATH+'\\parameters.dat', 'w')

    file.write("	#drawing_parameters	" + LINE_NEW)
    file.write("	   draw_link_ids= 0	" + LINE_NEW)
    file.write("	   link_thickness= 1	" + LINE_NEW)
    file.write("	   node_thickness= 1	" + LINE_NEW)
    file.write("	   node_radius= 3	" + LINE_NEW)
    file.write("	   queue_thickness= 6	" + LINE_NEW)
    file.write("	   selected_thickness= 10	" + LINE_NEW)
    file.write("	   show_background_image= 1	" + LINE_NEW)
    file.write("	   linkcolor= black	" + LINE_NEW)
    file.write("	   nodecolor= black	" + LINE_NEW)
    file.write("	   queuecolor= red	" + LINE_NEW)
    file.write("	   backgroundcolor= white	" + LINE_NEW)
    file.write("	   selectedcolor= green	" + LINE_NEW)
    file.write("	   gui_update_step= 0.2	" + LINE_NEW)
    file.write("	#moe_parameters	" + LINE_NEW)
    file.write("	   moe_speed_update= 60.0	" + LINE_NEW)
    file.write("	   moe_inflow_update= 60.0	" + LINE_NEW)
    file.write("	   moe_outflow_update= 60.0	" + LINE_NEW)
    file.write("	   moe_queue_update= 60.0	" + LINE_NEW)
    file.write("	   moe_density_update= 60.0	" + LINE_NEW)
    file.write("	   linktime_alpha= 0.2	" + LINE_NEW)
    file.write("	#assignment_matrix_parameters	" + LINE_NEW)
    file.write("	   use_ass_matrix= 1	" + LINE_NEW)
    file.write("	   ass_link_period= 900.0	" + LINE_NEW)
    file.write("	   ass_od_period= 900.0	" + LINE_NEW)
    file.write("	#turning_parameters	" + LINE_NEW)
    file.write("	   default_lookback_size= 20	" + LINE_NEW)
    file.write("	   turn_penalty_cost= 99999.0	" + LINE_NEW)
    file.write("	#server_parameters	" + LINE_NEW)
    file.write("	   od_servers_deterministic= 1	" + LINE_NEW)
    file.write("	   odserver_sigma= 0.2	" + LINE_NEW)
    file.write("	   sd_server_scale= 1.0	" + LINE_NEW)
    file.write("	   server_type= 3	" + LINE_NEW)
    file.write("	#vehicle_parameters	" + LINE_NEW)
    file.write("	   standard_veh_length= 7	" + LINE_NEW)
    file.write("	#route_parameters	" + LINE_NEW)
    file.write("	   update_interval_routes= 60.0	" + LINE_NEW)
    file.write("	   mnl_theta= -0.5	" + LINE_NEW)
    file.write("	   kirchoff_alpha= -1.0	" + LINE_NEW)
    file.write("	   delete_bad_routes= 0	" + LINE_NEW)
    file.write("	   max_rel_route_cost= 20.0	" + LINE_NEW)
    file.write("	   small_od_rate= 0.0	" + LINE_NEW)
    file.write("	#mime_parameters	" + LINE_NEW)
    file.write("	   mime_comm_step= 0.4	" + LINE_NEW)
    file.write("	   mime_min_queue_length= 20	" + LINE_NEW)
    file.write("	   mime_queue_dis_speed= 6	" + LINE_NEW)
    file.write("	   vissim_step= 0.1	" + LINE_NEW)
    file.write("	   sim_speed_factor= 1.9	" + LINE_NEW)
    file.write("	#transit_demand_parameters	" + LINE_NEW)
    file.write("	   demand_format= 3	" + LINE_NEW)
    file.write("	   demand_scale= 1.0	" + LINE_NEW)
    file.write("	   choice_set_indicator= 0	" + LINE_NEW)
    file.write("	   pass_day_to_day_indicator= 0	" + LINE_NEW)
    file.write("	   in_vehicle_d2d_indicator= 0	" + LINE_NEW)
    file.write("	   break_criterium= 0	" + LINE_NEW)
    file.write("	   transfer_coefficient= -0.40	" + LINE_NEW)
    file.write("	   in_vehicle_time_coefficient= -0.20	" + LINE_NEW)
    file.write("	   waiting_time_coefficient= -0.20	" + LINE_NEW)
    file.write("	   walking_time_coefficient= -0.20	" + LINE_NEW)
    file.write("	   average_walking_speed= 84.0	" + LINE_NEW)
    file.write("	   max_nr_extra_transfers= 3	" + LINE_NEW)
    file.write("	   absolute_max_transfers= 4	" + LINE_NEW)
    file.write("	   max_in_vehicle_time_ratio= 4.0	" + LINE_NEW)
    file.write("	   max_walking_distance= 2500.0	" + LINE_NEW)
    file.write("	   max_waiting_time= 2400.0	" + LINE_NEW)
    file.write("	   dominancy_perception_threshold= 40.0	" + LINE_NEW)
    file.write("	   choice_model= 1	" + LINE_NEW)
    file.write("	   real_time_info= 3	" + LINE_NEW)
    file.write("	   share_RTI_network= 1	" + LINE_NEW)
    file.write("	   start_pass_generation= 0	" + LINE_NEW)
    file.write("	   stop_pass_generation= 3600	" + LINE_NEW)
    file.write("	   od_pairs_for_generation= 0	" + LINE_NEW)
    file.write("	   gate_generation_time_diff= 0	" + LINE_NEW)
    file.write("	#transit_control_parameters	" + LINE_NEW)
    file.write("	   riding_time_weight= 1.0	" + LINE_NEW)
    file.write("	   dwell_time_weight= 1.0	" + LINE_NEW)
    file.write("	   waiting_time_weight= 2.0	" + LINE_NEW)
    file.write("	   holding_time_weight= 2.5	" + LINE_NEW)
    file.write("	   compliance_rate= 1.0	" + LINE_NEW)
    file.write("	   transfer_sync= 0	" + LINE_NEW)
    file.write("	#day2day_assignment	" + LINE_NEW)
    file.write("	   default_alpha_RTI= 0.7	" + LINE_NEW)

    file.close()


if __name__ == "__main__":
    pass
