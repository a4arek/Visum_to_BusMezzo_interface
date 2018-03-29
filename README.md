# Visum -> BusMezzo importer

(c) Department of Transport Systems, Cracow University of Technology, 2018
(c) Department of Transport and Planning, Delft University of Technology, 2018
 Arkadiusz Drabicki, Rafal Kucharski, Oded Cats
 adrabicki@pk.edu.pl, rkucharski@pk.edu.pl, o.cats@tudelft.nl

feel free to use however you want, the software is provided as-is, without warranty of any kind

for Visum see: http://vision-traffic.ptvgroup.com/en-us/products/ptv-visum/
for BusMezzo see: https://odedcats.weblog.tudelft.nl/busmezzo/
or contact with main BusMezzo developer:
Dr Oded Cats http://www.citg.tudelft.nl/en/about-faculty/departments/transport-and-planning/staff-information/dr-oded-cats/

# usage:
run the script in Visum (drag & drop).
BusMezzo files (.dat) will be created in the Version Project Directory of Visum (%MYDOCUMENTS% by default)

# network rules:
- NODES:
- LINKS/LINKTYPES: min. length 27[m] if contains StopPointOnLink
- TURNS:
- ZONES/CONNECTORS:
- STOPPOINTS/STOPAREAS:
- STOPS:
- LINES/LINEROUTES:
- TIMEPROFILES: only ONE per each LineRoute (=1) / remember to assign VehicleCombinations
- VEHICLEUNITS: only ONE per each VehicleCombination
- OD MATRICES:
- stops on links (DIRECTED!)
- one connector per zone ONLY
- connectors pinned directly to the stopArea access nodes
- PuT: timetable coded (no headways)
