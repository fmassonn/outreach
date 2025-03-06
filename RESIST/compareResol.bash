#!/bin/bash
set -o nounset
set -o errexit

region="Antarctic"

mkdir -p ./figs/stitch/${region}

start_date="1997-01-01"
end_date="2014-12-31"

current_date="$start_date"

while [[ "$current_date" < "$end_date" ]] || [[ "$current_date" == "$end_date" ]]; do
    echo "$current_date"

    fileName="./figs/stitch/${region}/stitch_${current_date}.png"

    if [ -f $fileName ]
    then
        echo "$fileName already existing, thus skipping"
    else

        convert ./figs/eorca1_elic_6_lumi/${region}/rotating/${current_date}.png -gravity West     -crop 33.33%x100%+0+0 A_${region}_crop.png
        convert ./figs/eorca025_elic_4_lumi/${region}/rotating/${current_date}.png -gravity center -crop 33.33%x100%+0+0 B_${region}_crop.png
        convert ./figs/eorca12_elic_lumi/${region}/rotating/${current_date}.png -gravity East      -crop 33.33%x100%+0+0 C_${region}_crop.png

        convert A_${region}_crop.png B_${region}_crop.png C_${region}_crop.png +append final_${region}.png

        convert final_${region}.png -gravity South -crop 100.0%x89%+0+0 final_${region}.png

        # Draw vertical lines
        magick final_${region}.png -stroke black -strokewidth 5 -draw "line 600,0 600,1600" -draw "line 1200,0 1200,1600" final_${region}.png

        convert final_${region}.png -font helvetica -pointsize 70 -draw "text 100,1700 '1° resolution'"     final_${region}.png
        convert final_${region}.png -font helvetica -pointsize 70 -draw "text 670,1700 '1/4° resolution'"   final_${region}.png
        convert final_${region}.png -font helvetica -pointsize 70 -draw "text 1250,1700 '1/12° resolution'" final_${region}.png

        mv final_${region}.png $fileName
        rm -f ?_final_${region}_crop.png
    fi

    current_date=$(date -j -v+1d -f "%Y-%m-%d" "$current_date" "+%Y-%m-%d")

done

