input = "Baz1a_cropped/";
output = "Baz1a_processed/";

function process_images(input, output, filename) {
open(input+filename);
run("8-bit");
run("Enhance Local Contrast (CLAHE)", "blocksize=30 histogram=256 maximum=3 mask=*None*");

tissueThreshPerc = 92.5;
nBins = 256;
getHistogram(values, count, nBins);
size = count.length;
// find culmulative sum
cumSum = 0;
for (i = 0; i<count.length; i++)
{
  cumSum += count[i];
}

tissueValue = cumSum * tissueThreshPerc / 100;

cumSumValues = count;
for (i = 1; i<count.length; i++)
{
  cumSumValues[i] += cumSumValues[i-1];
}
for (i = 1; i<cumSumValues.length; i++)
{
  if (cumSumValues[i-1] <= tissueValue && tissueValue <= cumSumValues[i])
    final_threshold = i;
}

setAutoThreshold("Default dark");
run("Threshold...");
setThreshold(final_threshold, 255);
setOption("BlackBackground", false);
run("Convert to Mask");
//run("Close");
run("Convert to Mask");
run("Shape Filter", "area=10-200 area_convex_hull=0-Infinity perimeter=0-Infinity perimeter_convex_hull=0-Infinity feret_diameter=0-Infinity min._feret_diameter=0-Infinity max._inscr._circle_diameter=0-Infinity area_eq._circle_diameter=0-Infinity long_side_min._bounding_rect.=0-Infinity short_side_min._bounding_rect.=0-Infinity aspect_ratio=1-Infinity area_to_perimeter_ratio=0-Infinity circularity=0-100 elongation=0-0.7 convexity=0-1 solidity=0-1 num._of_holes=0-Infinity thinnes_ratio=0-1 contour_temperatur=0-1 orientation=0-180 fractal_box_dimension=0-2 option->box-sizes=2,3,4,6,8,12,16,32,64 draw_holes black_background exclude_on_edges");

orignalName = filename;
originalNameWithoutExt = replace(orignalName , ".png" , "" ); 
finalName = originalNameWithoutExt + "_processed.png";
print(finalName);
saveAs("png",output+finalName);
close();
}

list = getFileList(input);
for (file_index = 0; file_index < list.length; file_index++){
        process_images(input, output, list[file_index]);
}