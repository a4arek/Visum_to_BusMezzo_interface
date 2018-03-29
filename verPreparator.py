import math
from fileWriter import *
from visumAttributes import DEFAULT_STOPPOINTRELPOS


# auxiliary functions for the modify_network_StopPoints(Visum) procedure:

def get_spline_coords_of_Link(in_WKT_Poly_list):
    # input - WKT_Poly list of the Link
    # output - 2D array with [x,y] coordinates of intermediate (polygon) points of the Link

    in_raw_list = in_WKT_Poly_list.replace("LINESTRING(", "")
    in_raw_list = in_raw_list.replace(")", "")

    in_list = in_raw_list.split(",")

    # initialize 2D array of the same size
    out_list = [[0 for x in range(2)] for y in range(len(in_list))]

    for row_id, row in enumerate(in_list):
        out_list[row_id][0] = float(row.split(" ")[0])
        out_list[row_id][1] = float(row.split(" ")[1])

    return out_list

def get_splitting_coords(ref_stoppoint, ref_node, dist_factor):
    # returns the X,Y coordinates for splitting the Link - based on:
    # (1) reference StopPoint, (2) reference Node, (3) distance/scale factor

    stop_x = ref_stoppoint[0]
    stop_y = ref_stoppoint[1]
    node_x = ref_node[0]
    node_y = ref_node[1]

    # get the X-coord
    if stop_x > node_x:
        split_x = stop_x + abs(stop_x - node_x) * dist_factor
    else:
        split_x = stop_x - abs(stop_x - node_x) * dist_factor
    # get the Y-coord
    if stop_y > node_y:
        split_y = stop_y + abs(stop_y - node_y) * dist_factor
    else:
        split_y = stop_y - abs(stop_y - node_y) * dist_factor

    return [split_x, split_y]

def find_nearest_intermediate_ref_Link_point(ref_stoppoint, Link_WKT_poly_list):
    # returns the X,Y coordinates of the nearest/closest spline point on the Link to the ref StopPoint
    # input - (1) reference StopPoint, (2) (converted) list of spline [x,y] coordinates

    rel_dist_list = [None] * len(Link_WKT_poly_list)
    for i, int_point in enumerate(Link_WKT_poly_list):
        rel_dist_list[i] = math.sqrt( (ref_stoppoint[0] - int_point[0])**2 + (ref_stoppoint[1] - int_point[1])**2 )

    # find intermediate node with minimum distance
    nearest_nd_id = rel_dist_list.index(min(rel_dist_list))
    point_x = Link_WKT_poly_list[nearest_nd_id][0]
    point_y = Link_WKT_poly_list[nearest_nd_id][1]

    return [point_x, point_y]

def find_opposite_ref_Link_point(ref_stoppoint, ref_int_node):
    # returns "mirror" coordinates of reference point for splitting procedure
    # (case 3 only)
    opposite_int_node_x = ref_stoppoint[0] - (ref_int_node[0] - ref_stoppoint[0])
    opposite_int_node_y = ref_stoppoint[1] - (ref_int_node[1] - ref_stoppoint[1])

    return [opposite_int_node_x, opposite_int_node_y]

def find_dist_factor(ref_stoppoint, ref_node, BM_stop_length):

    actual_distance = math.sqrt( (ref_stoppoint[0] - ref_node[0])**2 + (ref_stoppoint[1] - ref_node[1])**2 )
    distance_factor = BM_stop_length / actual_distance

    return distance_factor

#################################
## 0a. ADD EXTRA VISUM OBJECTS ##
#################################

# add necessary objects and modify Visum network before BusMezzo import

def modify_network_Zones(Visum):
    # Zones - convert into additional Nodes

    Iterator = Visum.Net.Zones.Iterator
    max_node_no = max(row[1] for row in Visum.Net.Nodes.GetMultiAttValues("No"))
    zone_offset_magnitude = math.ceil(math.log10(max_node_no))
    zone_id_offset = int(math.pow(10,zone_offset_magnitude))

    while Iterator.Valid:
        zone = Iterator.Item

        Visum.Net.AddNode(zone_id_offset + zone.AttValue("No"),
                          zone.AttValue("XCoord"),
                          zone.AttValue("YCoord"))
        zone.SetAttValue("AddVal1", int(zone_id_offset + zone.AttValue("No")))
        zone.SetAttValue("BM_ZoneID", int(zone_id_offset + zone.AttValue("No")))

        Iterator.Next()

def modify_network_Connectors(Visum):
    # Connectors - convert into additional Links

    Iterator = Visum.Net.Connectors.Iterator
    max_link_no = max(row[1] for row in Visum.Net.Links.GetMultiAttValues("No"))
    conn_offset_magnitude = math.ceil(math.log10(max_link_no))
    conn_id_offset = int(math.pow(10,conn_offset_magnitude))

    while Iterator.Valid:
        conn = Iterator.Item

        if conn.AttValue("Direction") == 1.0:
            zone = Visum.Net.Zones.ItemByKey(conn.AttValue("ZoneNo"))
            Visum.Net.AddLink(conn_id_offset, zone.AttValue("BM_ZoneID"), conn.AttValue("NodeNo"))
            conn_id_offset += 1
        else:
            pass

        Iterator.Next()

def modify_network_StopPoints(Visum):
    # add StopPoint Links (split) and set RelativePosition

    # add UDA (if not added yet)
    try:
        Visum.Net.StopPoints.AddUserDefinedAttribute("BM_StopPoint_Modified","BM_StopPoint_Modified","BM_StopPoint_Modified",9)
    except:
        pass

    Iterator = Visum.Net.StopPoints.Iterator

    while Iterator.Valid:
        sp = Iterator.Item
        sp_no = sp.AttValue("No")

        # FIRST - check if the StopPoint has already been modified
        if sp.AttValue("BM_StopPoint_Modified") == 1:
            # IF SO - SKIP the whole loop and proceed to the next StopPoint
            pass

        else:
            # IF NOT - MODIFY the StopPoint position
            # collect necessary input (StopPoint / Link / Node) parameters:
            sp_from_node = sp.AttValue("FromNodeNo")
            sp_link_no = sp.AttValue("LinkNo")

            link = Visum.Net.Links.ItemByLinkNrFromNode(sp_link_no, sp_from_node)
            link_length = link.AttValue("Length") * 1000        # in [m]

            # FIRST CHECK - minimum link length
            if link_length <= 26.0:
                pass # RK: what then?

            else:
                sp_to_node = link.AttValue("ToNodeNo")
                sp_rel_position = sp.AttValue("RelPos")

                sp_dist_from_node = link_length * sp_rel_position  # distance [m] between StopPoint <-> start node
                sp_dist_to_node = link_length - sp_dist_from_node  # distance [m] between StopPoint <-> end node

                # X, Y COORDINATES - data required for Link splitting procedure
                # X,Y COORDINATES - StopPoint
                sp_x = sp.AttValue("XCoord")
                sp_y = sp.AttValue("YCoord")
                ref_stoppoint = [sp_x, sp_y]
                # X,Y COORDINATES - FromNode
                from_node_x = Visum.Net.Nodes.ItemByKey(sp_from_node).AttValue("XCoord")
                from_node_y = Visum.Net.Nodes.ItemByKey(sp_from_node).AttValue("YCoord")
                ref_fromnode = [from_node_x, from_node_y]
                # X,Y COORDINATES - ToNode
                to_node_x = Visum.Net.Nodes.ItemByKey(sp_to_node).AttValue("XCoord")
                to_node_y = Visum.Net.Nodes.ItemByKey(sp_to_node).AttValue("YCoord")
                ref_tonode = [to_node_x, to_node_y]

                if sp_dist_from_node < 13.0:
                # case 1 - adjust StopPoint and split Link 26 [m] from the start node

                    adjust_rel_pos = 26.0/2.0 / link_length
                    try:
                        sp.SetAttValue("RelPos", adjust_rel_pos)
                    except:
                        print "Adjusting StopPoint position failed: ", sp.AttValue("No")
                        pass
                    split_node = get_splitting_coords(ref_stoppoint, ref_fromnode, 1.0)

                    try:
                        link.SplitAtPosition(split_node[0], split_node[1])
                    except:
                        print "Link splitting failed", link.AttValue("No")
                        pass

                elif sp_dist_to_node < 13.0:
                # case 2 - adjust StopPoint and split Link 26 [m] from the end node

                    adjust_rel_pos = (link_length - 26.0)/2.0 / link_length
                    try:
                        sp.SetAttValue("RelPos", adjust_rel_pos)
                        print "nie udalo sie przesunac StopPoint no", sp.AttValue("No")
                    except:
                        pass
                    split_node = get_splitting_coords(ref_stoppoint, ref_tonode, 1.0)

                    try:
                        link.SplitAtPosition(split_node[0], split_node[1])
                    except:
                        print "nie udalo sie podzielic Link no", link.AttValue("No")
                        pass

                else:
                # case 3 - split Link only within the StopPoint position

                    # X, Y COORDINATES - Link intermediate (polygon) points
                    link_polygon_course = link.AttValue("WKTPoly")
                    link_spline_coords = get_spline_coords_of_Link(link_polygon_course)
                    ref_int_node = find_nearest_intermediate_ref_Link_point(ref_stoppoint, link_spline_coords)
                    dist_factor = find_dist_factor(ref_stoppoint, ref_int_node, 26.0)

                    split_node_no1 = get_splitting_coords(ref_stoppoint, ref_int_node, dist_factor)
                    try:
                        link.SplitAtPosition(split_node_no1[0], split_node_no1[1])
                    except:
                        print "nie udalo sie przesunac StopPoint no", sp.AttValue("No")
                        pass

                    ref_opposite_int_node = find_opposite_ref_Link_point(ref_stoppoint,ref_int_node)
                    split_node_no2 = get_splitting_coords(ref_stoppoint, ref_opposite_int_node, dist_factor)
                    try:
                        link.SplitAtPosition(split_node_no2[0], split_node_no2[1])
                    except:
                        print "nie udalo sie podzielic Link no", link.AttValue("No")
                        pass
                try:
                    sp.SetAttValue("RelPos", DEFAULT_STOPPOINTRELPOS)
                except:
                    pass
                # FINAL PART - mark that the StopPoint was modified
                sp.SetAttValue("BM_StopPoint_Modified", 1)

        # proceed to the next StopPoint
        Iterator.Next()

    ## !! TO BE FIXED - PuT Assignment has to be run again
    Visum.Procedures.Execute()







    ## FIRST - check if the Visum network has already been modified
    # relpos_min_limit = 0.49
    # relpos_max_limit = 0.51

    # relpos_checklist = Visum.Net.StopPoints.GetMultiAttValues("RelPos")

    # min_r = min(i[1] for i in relpos_checklist)
    # max_r = max(i[1] for i in relpos_checklist)

    # if (relpos_min_limit < min_r and max_r < relpos_max_limit):
    ## in case it's already done - exit()
    #    return True

    ## ELSE - if not done yet, modify the StopPoint/Link network layout
    # Iterator = Visum.Net.StopPoints.Iterator

    # while Iterator.Valid:
    #    sp = Iterator.Item
    #    rel_pos = sp.AttValue("RelPos")
    #    sp_from_node = sp.AttValue("FromNodeNo")
    #    sp_link_no = sp.AttValue("LinkNo")

    #    link = Visum.Net.Links.ItemByLinkNrFromNode(sp_link_no, sp_from_node)

    #    sp_to_node = link.AttValue("ToNodeNo")
    #    link_length = link.AttValue("Length") * 1000

    #    access_node = sp.StopArea.AttValue("NodeNo")

    #    if access_node == sp_from_node:
            # if StopArea is assigned to the FromNode
            # then move StopPoint towards the FromNode
    #        adjust_rel_pos = 26.0/2.0 / link_length
    #        sp.SetAttValue("RelPos", adjust_rel_pos)

    #        from_node_x = Visum.Net.Nodes.ItemByKey(sp_from_node).AttValue("XCoord")
    #        from_node_y = Visum.Net.Nodes.ItemByKey(sp_from_node).AttValue("YCoord")
    #        sp_x = sp.AttValue("XCoord")
    #        sp_y = sp.AttValue("YCoord")

            # the following is to check the link orientation (if x,y are increasing or else)
    #        if sp_x > from_node_x:
    #            split_x = sp_x + (sp_x - from_node_x)
    #        elif sp_x == from_node_x:
    #            split_x = sp_x
    #        else:
    #            split_x = sp_x - (from_node_x - sp_x)

    #        if sp_y > from_node_y:
    #            split_y = sp_y + (sp_y - from_node_y)
    #        elif sp_x == from_node_x:
    #            split_y = sp_y
    #        else:
    #            split_y = sp_y - (from_node_y - sp_y)

            # finally - split the Link
    #        link.SplitAtPosition(split_x, split_y)

    #    else:
    #        # if StopArea is assigned to the ToNode
    #        # move StopPoint towards the ToNode -> then split Link
    #        adjust_rel_pos = (link_length - 26.0/2.0) / link_length
    #        sp.SetAttValue("RelPos", adjust_rel_pos)

    #        from_node_x = Visum.Net.Nodes.ItemByKey(sp_to_node).AttValue("XCoord")
    #        from_node_y = Visum.Net.Nodes.ItemByKey(sp_to_node).AttValue("YCoord")
    #        sp_x = sp.AttValue("XCoord")
    #        sp_y = sp.AttValue("YCoord")

            # the following is to check the link orientation (if x,y are increasing or else)
    #        if sp_x > from_node_x:
    #            split_x = sp_x + (sp_x - from_node_x)
    #        elif sp_x == from_node_x:
    #            split_x = sp_x
    #        else:
    #            split_x = sp_x - (from_node_x - sp_x)

    #        if sp_y > from_node_y:
    #            split_y = sp_y + (sp_y - from_node_y)
    #        elif sp_x == from_node_x:
    #            split_y = sp_y
    #        else:
    #            split_y = sp_y - (from_node_y - sp_y)

            # finally - split the Link
    #        link.SplitAtPosition(split_x, split_y)

        # ugly but necessary quick-fix - RelPos = 0.49 everywhere
    #    sp.SetAttValue("RelPos",0.49)

    #    Iterator.Next()


#########################################
## 2. ADJUST SPECIFIC VISUM ATTRIBUTES ##
#########################################

# adjust selected Visum input attributes and evaluate the UDAs for subsequent BusMezzo export

def adjust_Nodes(Visum):
    # {nodes} - assign NodeType values

    ## NEEDS TO BE FIXED!!
    Iterator = Visum.Net.LineRoutes.Iterator
    while Iterator.Valid:
        lr = Iterator.Item
        sp_list = lr.LineRouteItems.GetMultiAttValues("StopPointNo")

        # for start stop - set the BM_NodeType of FromNodeNo (accessed directly)
        start_stop_no = int(sp_list[0][1])
        from_node_no = Visum.Net.StopPoints.ItemByKey(start_stop_no).AttValue("FromNodeNo")
        start_node = Visum.Net.Nodes.ItemByKey(from_node_no)
        start_node.SetAttValue("BM_NodeType",1)

        # for end stop - set the BM_NodeType of ToNodeNo (accessed via the Link object)
        end_stop_no = int(sp_list[len(lr.LineRouteItems)-1][1])
        from_node_no = Visum.Net.StopPoints.ItemByKey(end_stop_no).AttValue("FromNodeNo")
        link_no = Visum.Net.StopPoints.ItemByKey(end_stop_no).AttValue("LinkNo")
        to_node_no = Visum.Net.Links.ItemByLinkNrFromNode(link_no,from_node_no).AttValue("ToNodeNo")
        end_node = Visum.Net.Nodes.ItemByKey(to_node_no)
        end_node.SetAttValue("BM_NodeType",2)

        Iterator.Next()

    Iterator = Visum.Net.Nodes.Iterator
    while Iterator.Valid:
        nd = Iterator.Item

        if (nd.AttValue("BM_NodeType")==1 or nd.AttValue("BM_NodeType")==2):
            pass
        else:
            nd.SetAttValue("BM_NodeType",3)

        # !! TO BE FIXED - ADD THE SERVER ID (additional column) to NodeType = 2
        Iterator.Next()

def adjust_Links(Visum):
    # {links} - assign LinkID values

    Iterator = Visum.Net.Links.Iterator
    i = 1
    while Iterator.Valid:
        link = Iterator.Item
        link.SetAttValue("BM_LinkID",i)
        i += 1

        Iterator.Next()

def adjust_Turns(Visum):
    # (turns} - assign TurnID and In/Out_LinkID values

    Iterator = Visum.Net.Turns.Iterator
    i = 1
    while Iterator.Valid:
        turn = Iterator.Item
        turn.SetAttValue("BM_TurnID",i)

        inlink = Visum.Net.Links.ItemByKey(turn.AttValue("FromNodeNo"),turn.AttValue("ViaNodeNo")).AttValue("BM_LinkID")
        outlink = Visum.Net.Links.ItemByKey(turn.AttValue("ViaNodeNo"),turn.AttValue("ToNodeNo")).AttValue("BM_LinkID")
        turn.SetAttValue("BM_InLinkID",inlink)
        turn.SetAttValue("BM_OutLinkID",outlink)

        i += 1

        Iterator.Next()

def adjust_LineRoutes(Visum):

    Iterator = Visum.Net.LineRoutes.Iterator
    line_no = 1

    while Iterator.Valid:

        ln = Iterator.Item.AttValue("LineName")
        dir = Iterator.Item.AttValue("DirectionCode")
        lrn = Iterator.Item.AttValue("Name")
        tp = Visum.Net.TimeProfiles.ItemByKey(ln, dir, lrn, '1')
        veh_type = tp.AttValue("VehCombNo")

        stop_list = Iterator.Item.LineRouteItems.GetMultiAttValues("StopPointNo")
        link_list = Iterator.Item.LineRouteItems.GetMultiAttValues("InLink\No")
        from_node_list = Iterator.Item.LineRouteItems.GetMultiAttValues("InLink\FromNodeNo")
        node_list = Iterator.Item.LineRouteItems.GetMultiAttValues("NodeNo")

        line_course = Iterator.Item.LineRouteItems.GetMultiAttValues("InLink\BM_LinkID")

        # !!! UPDATE LINKS FOR FILTERING - HERE!
        Visum_list_links = convert_ConcatenatedMultiAttValues(link_list)
        Visum_list_fromnodes = convert_ConcatenatedMultiAttValues(from_node_list)
        id = 1
        for lnk in range(1, len(Visum_list_links)+1):
            link_to_be_active = Visum.Net.Links.ItemByLinkNrFromNode(Visum_list_links[lnk-1],Visum_list_fromnodes[lnk-1])
            link_to_be_active.SetAttValue("BM_FILTER_Visum_Links",1)

        # BACK TO THE LINE ROUTE:

        # find start node
        second_node = node_list[1][1]
        if second_node is None:             # exception handler
            second_node = node_list[2][1]
        first_link = link_list[1][1]
        start_node = Visum.Net.Links.ItemByLinkNrFromNode(first_link,second_node).AttValue("ToNodeNo")

        # find end node
        last_node = node_list[len(node_list)-2][1]
        if last_node is None:               # exception handler
            last_node = node_list[len(node_list)-3][1]
        last_link = link_list[len(link_list)-1][1]
        end_node = Visum.Net.Links.ItemByLinkNrFromNode(last_link,last_node).AttValue("ToNodeNo")

        # find start stop
        start_stop = stop_list[0][1]
        # find end stop
        end_stop = stop_list[len(stop_list)-1][1]

        # convert Visum lists into "BusMezzo-tailored" strings
        conv_stop_list = convert_ConcatenatedMultiAttValues(stop_list)
        conv_line_course = convert_ConcatenatedMultiAttValues(line_course)
        no_stops = len(conv_stop_list)
        no_links = len(conv_line_course)
        add_stop_list = calc_BM_list_of_elements(conv_stop_list)
        add_line_course = calc_BM_list_of_elements(conv_line_course)

        opp_line_no = 1000 - line_no
        line_name = '_'.join([ln,dir,lrn])

        Iterator.Item.SetAttValue("BM_RouteID",line_no)
        Iterator.Item.SetAttValue("BM_OppositeRouteID",opp_line_no)
        Iterator.Item.SetAttValue("BM_RouteName", line_name)

        Iterator.Item.SetAttValue("BM_Start_Node_No",start_node)
        Iterator.Item.SetAttValue("BM_End_Node_No",end_node)
        Iterator.Item.SetAttValue("BM_No_Of_Links",no_links)
        Iterator.Item.SetAttValue("BM_List_Links",add_line_course)

        Iterator.Item.SetAttValue("BM_Start_Stop_No",start_stop)
        Iterator.Item.SetAttValue("BM_End_Stop_No",end_stop)
        Iterator.Item.SetAttValue("BM_List_Stops", add_stop_list)

        Iterator.Item.SetAttValue("BM_VehType",veh_type)

        line_no += 1    # assign the BM_RouteID iteratively
        Iterator.Next()

def adjust_TimeProfiles(Visum):
    # {trips} - assign selected attributes

    Iterator = Visum.Net.TimeProfiles.Iterator

    while Iterator.Valid:
        i = 0
        tp = Iterator.Item
        add_tp_list = str()
        add_dep_list = str()

        tp_list = [str_int(60*row[1]) for row in tp.TimeProfileItems.GetMultiAttValues("PreRunTime")]
        no_of_tp_segments = len(tp_list)
        add_tp_list = calc_BM_list_of_elements(tp_list)
        # add_tp_list = space.join(str(int(r)) for r in tp_list)

        # first dispatch time of each line
        sim_start_time_offset = Visum.Net.TimeSeriesCont.ItemByKey(1).AttValue("StartTime")

        try:
            first_dep = tp.VehJourneys.GetMultiAttValues("Dep")[0][1]
            first_dep_offset = first_dep - sim_start_time_offset
            # relevant for format:2 - timetable-based BusMezzo assignment
            dep_list = [str_int(row[1] - first_dep) for row in tp.VehJourneys.GetMultiAttValues("Dep")]
            add_dep_list = calc_BM_list_of_elements(dep_list)
            # relevant for format:3 - headway-based BusMezzo assignment
            no_of_trips = tp.VehJourneys.Count
            headway = str_int(60 * round(float(3600/no_of_trips)/60))

        except:
            # in case no VehJourneys are defined for this TimeProfile:

            first_dep = 0
            first_dep_offset = 0
            dep_list = ""
            add_dep_list = ""
            no_of_trips = 0
            headway = 0

        # trip ID: BM_TimeProfileID = BM_LineRouteID
        tp_id = tp.AttValue("LineRoute\BM_RouteID")

        tp.SetAttValue("BM_TimeProfileID",tp_id)
        tp.SetAttValue("BM_No_of_RunTimes",no_of_tp_segments)
        tp.SetAttValue("BM_List_RunTimes",add_tp_list)
        tp.SetAttValue("BM_Headway",headway)
        tp.SetAttValue("BM_First_Dispatch_Time",first_dep_offset)
        tp.SetAttValue("BM_List_DispTimes",add_dep_list)

        Iterator.Next()

def adjust_VehicleJourneys(Visum):
    # {trips} - assign VehTypeID
    # nested iterator - (1.) LineRoutes => (2.) VehJourneys

    Iterator = Visum.Net.LineRoutes.Iterator

    while Iterator.Valid:
        lr = Iterator.Item

        ln = lr.AttValue("LineName")
        dir = lr.AttValue("DirectionCode")
        lrn = lr.AttValue("Name")
        tp_code = "1"
        vehcomb = lr.TimeProfiles.ItemByKey(ln,dir,lrn,tp_code).AttValue("VehCombNo")

        line_code = lr.AttValue("BM_RouteID")

        Iterator2 = lr.TimeProfiles.ItemByKey(ln,dir,lrn,tp_code).VehJourneys.Iterator
        vj_id = 1

        while Iterator2.Valid:
            vehtrip = Iterator2.Item

            trip_id = 100 * line_code + vj_id
            add_trip_list = LIST_BEGIN + str_int(trip_id) + LIST_END

            vehtrip.SetAttValue("BM_TripID",trip_id)
            vehtrip.SetAttValue("BM_VehTypeID",vehcomb)
            vehtrip.SetAttValue("BM_List_Trips",add_trip_list)

            vj_id += 1
            Iterator2.Next()

        Iterator.Next()


    # Iterator = Visum.Net.VehicleJourneys.Iterator

    # while Iterator.Valid:
    #    vehtrip = Iterator.Item
    #    ln = vehtrip.AttValue("LineName")
    #    dir = vehtrip.AttValue("DirectionCode")
    #    lrn = vehtrip.AttValue("LineRouteName")
    #    tp = vehtrip.AttValue("TimeProfileName")

    #    tripno = vehtrip.AttValue("No")
    #    tripid =  LIST_BEGIN + str_int(tripno) + LIST_END

    #    vehcomb = Visum.Net.TimeProfiles.ItemByKey(ln,dir,lrn,tp).AttValue("VehCombNo")

    #    vehtrip.SetAttValue("BM_TripID",tripid)
    #    vehtrip.SetAttValue("BM_VehTypeID",vehcomb)

    #    Iterator.Next()

def adjust_StopPoints(Visum):

    Iterator = Visum.Net.StopPoints.Iterator

    while Iterator.Valid:

        sp = Iterator.Item

        sp_link_no = sp.AttValue("LinkNo")
        sp_fromnode = sp.AttValue("FromNodeNo")

        print sp.AttValue("No")
        sp_link = Visum.Net.Links.ItemByLinkNrFromNode(sp_link_no, sp_fromnode)
        sp_link_id = sp_link.AttValue("BM_LinkID")

        link_length = sp_link.AttValue("Length") * 1000         # in [m]
        sp_relpos = sp.AttValue("RelPos")
        sp_position = link_length * sp_relpos

        sp.SetAttValue("BM_StopLinkID", sp_link_id)
        sp.SetAttValue("BM_Position", sp_position)


        Iterator.Next()


####################################################
## 1. ADD NECESSARY VISUM USER-DEFINED ATTRIBUTES ##
####################################################

def addUDAs(_obj, _name, _call):
    # general function for adding UDAs
    # create user-defined attributes (UDAs) for Visum objects with following arguments:
    # _obj - Visum.Net object
    # _name - attribute name/ID
    # _call - data type parameters (EnumValueType)
    _obj.AddUserDefinedAttribute(*[_name]*3+_call)

# add necessary UDAs to convert Visum variables into "BusMezzo-tailored" units

def addUDAs_Nodes(Visum):

    obj = Visum.Net.Nodes
    # UDAs formulae and constants

    addUDAs(obj,"BM_NodeType",[1,0,0,0,0,0])

def addUDAs_Links(Visum):

    obj = Visum.Net.Links
    # UDAs formulae and constants
    length_formula = formula="1000*[Length]"
    # quick-fix here
    hist_t0_time_formula = formula="max(0.1,3600*[Length]/[V0PrT])"

    addUDAs(obj,"BM_LinkID",[1,0,0,0,0,0])
    addUDAs(obj,"BM_Length",[225,1,0,0,0,0,0,0,length_formula])
    addUDAs(obj,"BM_Hist_T0_Time",[225,1,0,0,0,0,0,0,hist_t0_time_formula])

    addUDAs(obj,"BM_FILTER_Visum_Links",[9])

def addUDAs_LinkTypes(Visum):

    obj = Visum.Net.LinkTypes
    # UDAs formulae and constants
    v0_PrT_formula = formula="[V0PrT]/3.6"

    addUDAs(obj,"BM_SDID_Function",[1,0,0,0,0,0])
    addUDAs(obj,"BM_V0PrT",[225,1,0,0,0,0,0,0,v0_PrT_formula])
    addUDAs(obj,"BM_VminPrT",[1,0,0,0,0,1])
    addUDAs(obj,"BM_Kmax",[1,0,0,0,0,1])
    addUDAs(obj,"BM_Kmin",[1,0,0,0,0,1])

def addUDAs_Turns(Visum):

    obj = Visum.Net.Turns

    addUDAs(obj,"BM_TurnID",[1,0,0,0,0,0])
    addUDAs(obj,"BM_InLinkID",[1,0,0,0,0,0])
    addUDAs(obj,"BM_OutLinkID",[1,0,0,0,0,0])
    addUDAs(obj,"BM_ServerID",[1,0,0,0,0,0])
    addUDAs(obj,"BM_LookBack",[1,0,0,0,0,40])

def addUDAs_LineRoutes(Visum):

    obj = Visum.Net.LineRoutes

    # ATTR_LIST_ROUTES
    addUDAs(obj,"BM_RouteID",[1,0,0,0,0,0])
    addUDAs(obj,"BM_RouteName",[5])
    addUDAs(obj,"BM_List_Links",[5])
    addUDAs(obj,"BM_No_of_Links",[1,0,0,0,0,0])
    addUDAs(obj,"BM_List_Stops",[5])
    addUDAs(obj,"BM_Start_Node_No",[1,0,0,0,0,0])
    addUDAs(obj,"BM_End_Node_No",[1,0,0,0,0,0])
    addUDAs(obj,"BM_Start_Stop_No",[1,0,0,0,0,0])
    addUDAs(obj,"BM_End_Stop_No",[1,0,0,0,0,0])

    # ATTR_LIST_LINEROUTES
    addUDAs(obj,"BM_VehType",[1,0,0,0,0,0])
    addUDAs(obj,"BM_OppositeRouteID",[1,0,0,0,0,0])
    addUDAs(obj,"BM_HoldingStrategy",[1,0,0,0,0,0])
    addUDAs(obj,"BM_HoldingRatio",[1,0,0,0,0,0])
    addUDAs(obj,"BM_InitialOccupPerStop",[1,0,0,0,0,0])
    addUDAs(obj,"BM_InitialOccupNumStops",[1,0,0,0,0,0])

def addUDAs_TimeProfiles(Visum):

    obj = Visum.Net.TimeProfiles

    addUDAs(obj,"BM_TimeProfileID",[1,0,0,0,0,0])
    addUDAs(obj,"BM_List_RunTimes",[5])
    addUDAs(obj,"BM_No_of_RunTimes",[1,0,0,0,0,0])
    addUDAs(obj,"BM_First_Dispatch_Time",[1,0,0,0,0,0])
    # relevant in case of format:3 only:
    addUDAs(obj,"BM_Headway",[1,0,0,0,0,0])
    # relevant in case of format:2 only:
    addUDAs(obj,"BM_List_DispTimes",[5])

def addUDAs_VehicleUnits(Visum):

    obj = Visum.Net.VehicleUnits
    # UDAs formulae and constants
    veh_length_formula = formula="12"
    dt_func_formula = formula="1"

    addUDAs(obj,"BM_VehLength",[225,0,0,0,0,0,0,0,veh_length_formula])
    addUDAs(obj,"BM_DTFunction",[225,0,0,0,0,0,0,0,dt_func_formula])

def addUDAs_VehicleJourneys(Visum):

    obj = Visum.Net.VehicleJourneys
    # UDAs formulae and constants
    # !! TO BE FIXED - ADD {..brackets..} below here:
    numtrips_formula = formula="1"

    addUDAs(obj,"BM_TripID",[1,0,0,0,0,0])
    addUDAs(obj,"BM_List_Trips",[5])
    addUDAs(obj,"BM_VehTypeID",[1,0,0,0,0,0])
    addUDAs(obj,"BM_NumTrips",[225,0,0,0,0,0,0,0,numtrips_formula])

def addUDAs_StopPoints(Visum):

    obj = Visum.Net.StopPoints
    # UDAs formulae and constants
    length_formula = formula="25"
    stoptype_formula = formula="0"
    can_overtake_formula = formula="0"
    RTI_lvl_formula = formula="3"

    addUDAs(obj,"BM_StopLinkID",[1,0,0,0,0,0])
    addUDAs(obj,"BM_Position",[2,1,0,0,0,0])
    addUDAs(obj,"BM_Length",[225,1,0,0,0,0,0,0,length_formula])
    addUDAs(obj,"BM_StopType",[225,0,0,0,0,0,0,0,stoptype_formula])
    addUDAs(obj,"BM_CanOvertake",[225,0,0,0,0,0,0,0,can_overtake_formula])
    addUDAs(obj,"BM_RTI_Level",[225,0,0,0,0,0,0,0,RTI_lvl_formula])

