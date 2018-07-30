# [fileWriter] - building blocks, constants and functions

import math

### building blocks and constants

LIST_BEGIN = "{"
LIST_END = "}"
LIST_END_NL = "}\n"
LINE_TAB = "	"
LINE_NEW = "\n"
VISUM_CONCAT_DELIM = ","
LOG_HEADER = "-"*50+"\n\t"

### mapping functions

def logPrinter(msg, msg_type = 'finished', Visum = None):
    msg = LOG_HEADER + str(msg) + "\t:\t" + msg_type
    #if Visum is not None:
    Visum.Log(8192, msg)

    print(msg)

def addTable(file, name, table, type_list):
    # add new BM {object category}
    if name != "":
        file.write(name + ":" + LINE_TAB+str(len(table)) + "\n")
    for line in table:
        appendDataLine(file, line, type_list)
    file.write(LINE_NEW)

def appendDataLine(file, line, type_list):
    # add new BM {object instance}

    toAdd = LIST_BEGIN
    for i, raw_field in enumerate(line):

        if isinstance(raw_field, list):
        # exception accessed for STOP_TRANSFERS only - make_Transit_Demand(Visum)
            list_len = -1* len(raw_field)
            datatype = type_list[list_len:]
            toAdd += LIST_BEGIN
            for j, raw_nested_field in enumerate(raw_field):
                    # toAdd += LINE_TAB + '{0:.1f}'.format(float(nested_field))
                    nested_field = datatype[j](raw_nested_field)
                    toAdd += LINE_TAB + addField(nested_field)
            toAdd += LINE_TAB + LIST_END

        else:
        # all other instances in the make_BM(Visum):
            datatype = type_list[i]
            field = datatype(raw_field)
            add = addField(field)
            toAdd += LINE_TAB + add
    toAdd += LINE_TAB + LIST_END_NL
    file.write(toAdd)

def addField (field):
    # add BM parameter of specific format
    if isinstance(field, int):
        return '{:1}'.format(int(field))
    elif isinstance(field, float):
        return '{0:.1f}'.format(float(field))
    elif isinstance(field, str):
        return str(field)
    elif isinstance(field, bytes):
        return str(field)
    else:
        return str(0)


### auxilliary functions for mapping/adjusting procedures:

def str_int(in_float):
    # converts float number into string(integer) - NO decimal places
    out_str_int = '{0:g}'.format(float(in_float))
    return(out_str_int)

def convert_ConcatenatedMultipleAttributes(input_tuple):
    # input - 2D tuple list with Visum attributes
    # !! (important! - does not contain empty fields)
    # remove duplicate rows - if 1st column contains duplicate entries
    # output - 2D array with integers

    input_array = [list(row) for row in input_tuple]
    in_array_remove_duplicates = []
    row_prev = [None, None]

    for row in input_array:
        if row[0] == row_prev[0]:
            pass
        else:
            in_array_remove_duplicates.append([int(k) for k in row])
            row_prev = row

    output_2d_array = in_array_remove_duplicates

    return output_2d_array


def convert_ConcatenatedMultiAttValues(input_list):
    # remove NoneTypes
    # remove duplicates (i.e. elements appearing twice IN A ROW)
    # produce list of integers (final output)
    in_list_remove_nones = [i[1] for i in input_list if i[1] is not None]
    in_list_remove_duplicates = []
    i_prev = None

    for i in in_list_remove_nones:
        if i == i_prev:
            pass
        else:
            in_list_remove_duplicates.append(i)
            i_prev = i

    out_list_convert_integers = map(lambda j: int(float(j)), in_list_remove_duplicates)
    output_list = list(out_list_convert_integers)

    return output_list

def calc_BM_list_of_elements(in_int_list):
    """
    returns no. of list elements (e.g. route stops)
    :param in_int_list:
    :return:
    """

    out_str_list = LIST_BEGIN + ' '.join(map(str, in_int_list)) + LIST_END
    return(out_str_list)

def numbering_offset(Visum_Object_List_Creator):
    # calculates the numbering offset of Visum Net elements
    # as a further order of magnitude
    # e.g. max(No) = 7896 => numbering_offset(No) = 10001

    object_no_list = Visum_Object_List_Creator
    object_no_list.AddColumn("No")
    max_object_no = float(object_no_list.Max(0))
    magnitude_order = math.ceil(math.log10(max_object_no))

    output_offset = (10 ** magnitude_order) + 1

    return output_offset

def find_source_point(input_source_conn, output_stop_list):
    # used in {stop_distances} mapping - find the ZoneID index

    source_id = input_source_conn[0]

    for i, zone_id in enumerate(output_stop_list):
        if zone_id[0] == source_id:
            break

    output_row_index = i

    return output_row_index

