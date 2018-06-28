# [visumFilters] - necessary filters for several Visum object categories

#################################################################
# 4. FILTER VISUM OBJECTS BEFORE IMPORTING THEM INTO BUSMEZZO  ##
#################################################################


def filter_Links(Visum):
    # filter out only those Links which form a part of at least one LineRoute segment

    Iterator = Visum.Net.Links.Iterator

    while Iterator.Valid:

        check_link = Iterator.Item.AttValue("BM_FILTER_Visum_Links")
        check_link_zone = Iterator.Item.AttValue("BM_FILTER_Visum_Zone_Centroid_Links")

        if (check_link == 1.0) or (check_link_zone == 1.0):
            Iterator.Item.Active = True
        else:
            Iterator.Item.Active = False

        Iterator.Next()

def filter_Turns(Visum):
    # filter out Turns between active Links only

    Iterator = Visum.Net.Turns.Iterator

    while Iterator.Valid:

        tr = Iterator.Item
        no_of_passing_line_routes = tr.AttValue("Count:LineRouteItems")

        if no_of_passing_line_routes > 0:
            Iterator.Item.Active = True
        else:
            Iterator.Item.Active = False

        ### fixed 25-05-2018 - new method added above, old method (below)

        # check_in_link = Visum.Net.Links.ItemByKey(tr.AttValue("FromLink\FromNodeNo"), tr.AttValue("FromLink\ToNodeNo")).Active
        # check_out_link = Visum.Net.Links.ItemByKey(tr.AttValue("ToLink\FromNodeNo"), tr.AttValue("ToLink\ToNodeNo")).Active

        # if check_in_link == True and check_out_link == True:
        #     Iterator.Item.Active = True
        # else:
        #     Iterator.Item.Active = False

        Iterator.Next()

def filter_LinkTypes(Visum):
    # should be OK but it's obsolete (and not used) for now - since LinkTypes cannot be set (in)active in Visum yet

    Iterator = Visum.Net.LinkTypes.Iterator

    while Iterator.Valid:

        check_link_type = Iterator.Item.AttValue("CountActive:Links")

        if check_link_type > 0:
            Iterator.Item.Active = True
        else:
            Iterator.Item.Active = False

        Iterator.Next()


if __name__ == "__main__":
    pass

