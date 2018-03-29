# auxiliary functions for the modify_network_StopPoints(Visum) procedure:
from math import sqrt


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
        rel_dist_list[i] = sqrt( (ref_stoppoint[0] - int_point[0])**2 + (ref_stoppoint[1] - int_point[1])**2 )

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

    actual_distance = sqrt( (ref_stoppoint[0] - ref_node[0])**2 + (ref_stoppoint[1] - ref_node[1])**2 )
    distance_factor = BM_stop_length / actual_distance

    return distance_factor