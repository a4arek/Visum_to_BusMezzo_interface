
###############################################################
# 3. FILTER VISUM OBJECTS BEFORE IMPORTING THEM TO BUSMEZZO ##
###############################################################


def filter_Links(Visum):

    Iterator = Visum.Net.Links.Iterator

    while Iterator.Valid:

        check_link = Iterator.Item.AttValue("BM_FILTER_Visum_Links")

        if check_link == 1.0:
            Iterator.Item.Active = True
        else:
            Iterator.Item.Active = False

        Iterator.Next()

def filter_Turns(Visum):

    Iterator = Visum.Net.Turns.Iterator

    while Iterator.Valid:

        tr = Iterator.Item
        check_in_link = Visum.Net.Links.ItemByKey(tr.AttValue("FromLink\FromNodeNo"), tr.AttValue("FromLink\ToNodeNo")).Active
        check_out_link = Visum.Net.Links.ItemByKey(tr.AttValue("ToLink\FromNodeNo"), tr.AttValue("ToLink\ToNodeNo")).Active

        if check_in_link == True and check_out_link == True:
            Iterator.Item.Active = True
        else:
            Iterator.Item.Active = False

        Iterator.Next()

def filter_LinkTypes(Visum):
    # should be OK but doesn't work now - since LinkTypes cannot be set (in)active in Visum yet

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

