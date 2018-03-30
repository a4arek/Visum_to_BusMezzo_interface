# Visum -> BusMezzo importer

(c) Department of Transport Systems, Cracow University of Technology, 2018

(c) Department of Transport and Planning, Delft University of Technology, 2018

 Arkadiusz Drabicki, Rafal Kucharski, Oded Cats
 
 adrabicki_at_pk.edu.pl, rkucharski_at_pk.edu.pl, o.cats_at_tudelft.nl

# general

Scripts to export `BusMezzo` input files from `PTV Visum` version file.

for Visum see: http://vision-traffic.ptvgroup.com/en-us/products/ptv-visum/
for BusMezzo see: https://odedcats.weblog.tudelft.nl/busmezzo/
or contact with main BusMezzo developer:
Dr Oded Cats http://www.citg.tudelft.nl/en/about-faculty/departments/transport-and-planning/staff-information/dr-oded-cats/

# usage:
run the script in Visum (drag & drop).
BusMezzo files (.dat) will be created in the Version Project Directory of Visum (%MYDOCUMENTS% by default)

# network rules:
- NODES:
- LINKS/LINKTYPES: min. length 27m if contains StopPointOnLink
- TURNS:
- ZONES/CONNECTORS:
- STOPPOINTS/STOPAREAS:
- STOPS:
- LINES/LINEROUTES:
- TIMEPROFILES: only ONE per each LineRoute (=1) / remember to assign VehicleCombinations
- VEHICLEUNITS: only ONE per each VehicleCombination
- OD MATRICES

# visum network rules

- stops on links (DIRECTED!)
- one connector per zone ONLY
- connectors pinned directly to the stopArea access nodes
- PuT: timetable coded (no headways)

# licence

[licence](https://github.com/a4arek/Visum_to_BusMezzo_interface/blob/master/LICENSE)


