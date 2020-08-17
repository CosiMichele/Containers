# Containers

Containers used in the PhytoOracle project.

## Functional (use Singularity!)

+ `flirfieldplot`
+ `po_flir2tif_s10`
+ `po_flir2tif_s11`
+ `po_meantemp_comb`

#### flirfieldplot

+ Creates a stitched "ortho" for flir images.

Usage:
`singularity run -B $(pwd):/mnt --pwd /mnt/ docker://cosimichele/flirfieldplot -o <out_dir> -d <scan_date> <tif_dir>`

#### po_flir2tif_s10

+ Re-calibrated transformer: converts bin to tif for gantry files (s10).

Usage:
`singularity run -B $(pwd):/mnt --pwd /mnt/ docker://cosimichele/po_flir2tif_s10 -m <metadata.json> <bin_dir>`

#### po_flir2tif_s11

+ Calibrated transformer: converts bin to tif fomr gantry files (s11).

Usage:
`singularity run -B $(pwd):/mnt --pwd /mnt/ docker://cosimichele/po_flir2tif_s11 -m <metadata.json> <bin_dir>`

#### po_meantemp_comb

+ Extracts mean temperature information from geotif images sing stats and CV2.

Usage:
`singularity run -B $(pwd):/mnt --pwd /mnt/ docker://cosimichele/po_temp_cv2stats -g <shp.geojson> -o <out_dir/> -d <scan_date> <tif_dir>`
  
## Redundant/developmental

+ `po_meantemp`
+ `peaks_temp`
+ `po_mt_img`
+ `zero2nan`

#### po_meantemp

+ Extracts mean temperature information from geotif images using CV2. Integrated in `po_meantemp_comb`.

Usage:
`singularity run -B $(pwd):/mnt --pwd /mnt/ docker://cosimichele/po_meantemp:latest -g <shp.geojson> <tif_dir>`

#### peaks_temp

+ Extracts mean temperature information from geotif images by delimiting histogram peaks. Integrated in `po_meantemp_comb`.

Usage:
`singularity run -B $(pwd):/mnt --pwd /mnt/ docker://cosimichele/peakstemp:latest -g <shp.geojson> <tif_dir>`

#### po_mt_img

+ Extracts mean temperature information from geotif images using CV2 and outputs mask image for quality control.

Usage:
`singularity run -B $(pwd):/mnt --pwd /mnt/ docker://cosimichele/po_mt_img:latest -g <shp.geojson> <tif_dir>`

#### zero2nan

+ Sets pixels with value = 0 to NaN. integrated in `flirfieldplot`.

Usage:
`singularity run -B $(pwd):/mnt --pwd /mnt/ docker://cosimichele/zero2nan:latest -o <output_file> -O <output_dir> <tif_img>`

