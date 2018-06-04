#############################################################
#              PTV Visum -> BusMezzo importer              ##
#############################################################

version 1.0 (beta), released: June 2018
(c) Department of Transportation Systems, Cracow University of Technology, 2018
(c) Department of Transport and Planning, Delft University of Technology, 2018
Arkadiusz Drabicki, Rafal Kucharski, Oded Cats
adrabicki [at] pk.edu.pl, rkucharski [at] pk.edu.pl, o.cats [at] tudelft.nl
http://www.kst.pk.edu.pl, https://www.tudelft.nl/en/ceg/about-faculty/departments/transport-planning/

feel free to use however you want, the software is provided as-is, without warranty of any kind

for Visum see: http://vision-traffic.ptvgroup.com/en-us/products/ptv-visum/
for BusMezzo see: https://odedcats.weblog.tudelft.nl/busmezzo/
or contact the main BusMezzo developer:
Dr Oded Cats - http://www.citg.tudelft.nl/en/about-faculty/departments/transport-and-planning/staff-information/dr-oded-cats/


########################################
##               usage:                ##
########################################

run the script in Visum (drag & drop).
BusMezzo files (.dat) will be created in the Version Project Directory of Visum (%MYDOCUMENTS% by default)


##############################################################
##     Before using the script, please read the following    ##
###     - VISUM INPUT NETWORK (.ver file) REQUIREMENTS:       ##
###     (otherwise the BM export will NOT work properly!)     ##
##############################################################

### LINKS:
- Bidirectional LINKS can be used in Visum for intermediate LINEROUTE segments.
- !! BUT !! - First and last STOPPOINTS (LINEROUTE segments) should always be placed on separate, unidirectional LINKS!
- (This is to comply with the Mezzo representation of in/out {links} as an exit from / entry to the PuT depot.)

### LINKTYPES:
- Visum LINKTYPE data -> mapped into the BM {sdfuncs} data.
- BM {sdfunc} max. speed assumed from the v0_PrT_max parameter in Visum.

### ZONES / CONNECTORS:
- ZONES will be imported as additional {stops} into BusMezzo.
- CONNECTORS should be pinned directly to ACCESSNODES - these will be imported as additional {stop_distances}.

### STOPS / STOPAREAS / STOPPOINTS:
- BusMezzo {stops} will be imported from the STOPAREA level - therefore, each STOPPOINT should be preferably assigned
  to an individual STOPAREA (actually - that's highly recommended, otherwise BusMezzo network might not work properly).
- STOPPOINTS in Visum should be defined as directed, on LINKS.
- Important!! Separate STOPPOINTS are always required for PuT LINEROUTES which either:
  commence from / pass through / or terminate at that particular STOP!
- (E.g. Several LINEROUTES commencing from a given STOP can depart from the same STOPPOINT, but this S.P. should
  always be separated from the STOPPOINT served by LINEROUTES which pass through that STOP.)

### LINES / LINEROUTES:
- LINEROUTES will be imported into BusMezzo as {lines} assigned with different numbers (IDs)
  - the original LINEROUTE name/no. will be saved under a separate attribute in the BM file.
- Intermediate LINEROUTE segments can use shared LINK segments and STOPPOINTS with other LINEROUTES
  - but: first and last LINEROUTE segment require separate LINKS and origin/destination-only STOPOINTS.

### TIMEPROFILES:
- Only ONE TIMEPROFILE per each LINEROUTE (preferably, name = '1').
- Remember to assign the VEHICLECOMBINATION to each TIMEPROFILE!
- VEHICLE JOURNEYS need to be defined for each TIMEPROFILE / LINEROUTE.
- BM {trips} format 2: TIMEPROFILES imported with exact departure times from the origin {stop}.
- BM {trips} format 3: TIMEPROFILES imported with average service headways (rounded to 30 secs).

### VEHICLEUNITS / VEHICLECOMBINATIONS:
- These should be defined and assigned to the specific TIMEPROFILES.
- Make sure that Seat/TotalCapacity parameters are defined, and SeatCap <= TotalCap.
- BM {vehicle_scheduling}: simplified driving roster assumed for now (single trips only).

### DEMAND MODEL:
- PuT demand model from Visum will be imported into BusMezzo as {passenger_rates} format: 3.
  (Zone-level OD from Visum -> mapped as stop-level OD into BM, with additional fictitious {stops} created.)
- Make sure that demand matrix is assigned to the PuT DEMAND SEGMENT (in the OD DEMANDDATA settings).
- Furthermore, check that StartTime and EndTime are defined in the SEGMENT TIME SERIES (these should be consistent
  with the PuT assignment simulation time!).
