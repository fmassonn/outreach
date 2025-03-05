#!/bin/bash
set -o nounset
set -o errexit

region="Antarctic"

mkdir -p ./figs/stitch/${region}

start_date="2005-01-01"
end_date="2014-12-31"

current_date="$start_date"

while [[ "$current_date" < "$end_date" ]] || [[ "$current_date" == "$end_date" ]]; do
    echo "$current_date"

    convert ./figs/eorca1_elic_6_lumi/${region}/rotating/${current_date}.png -gravity West     -crop 33.33%x100%+0+0 A_crop.png
    convert ./figs/eorca025_elic_4_lumi/${region}/rotating/${current_date}.png -gravity center -crop 33.33%x100%+0+0 B_crop.png
    convert ./figs/eorca12_elic_lumi/${region}/rotating/${current_date}.png -gravity East      -crop 33.33%x100%+0+0 C_crop.png

    convert A_crop.png B_crop.png C_crop.png +append final.png

    convert final.png -gravity South -crop 100.0%x89%+0+0 final.png

    # Draw vertical lines
    magick final.png -stroke black -strokewidth 5 -draw "line 600,0 600,1600" -draw "line 1200,0 1200,1600" final.png

    convert final.png -font helvetica -pointsize 70 -draw "text 100,1700 '1° resolution'"     final.png
    convert final.png -font helvetica -pointsize 70 -draw "text 670,1700 '1/4° resolution'"   final.png
    convert final.png -font helvetica -pointsize 70 -draw "text 1250,1700 '1/12° resolution'" final.png

    mv final.png ./figs/stitch/${region}/stitch_${current_date}.png
    rm -f ?_crop.png

    current_date=$(date -j -v+1d -f "%Y-%m-%d" "$current_date" "+%Y-%m-%d")
done

