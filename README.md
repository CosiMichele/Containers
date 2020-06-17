# Containers

Containers used in the PhytoOracle project.

#### Meantemp

Extracts mean temperature information from geotif images.

Usage:
+ singularity run -B $(pwd):/mnt --pwd /mnt/ docker://cosimichele/po_meantemp:latest -g <geojson> <tifdir>
