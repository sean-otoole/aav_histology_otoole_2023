# aav_histology_OToole_2023

Examination of the spatial patterns of expression for AAVs designed to label specific neuronal cell types for the publication entitled: [Molecularly targetable cell types in mouse visual cortex have distinguishable prediction error responses](https://www.cell.com/neuron/pdf/S0896-6273(23)00626-8.pdf).

**Please note** that this repository, even with the appropriate libraries and packages installed, will not operate independently. Due to size limitations, the **original datasets** are not included. However, for those who are interested, the *original published dataset* as well as the code are available [elsewhere](https://doi.org/10.5281/zenodo.8229544).

At the moment this README is still under construction, more details to follow.

## Project Organization
```

┌── cropped_to_processed_macro.ijm                  : imagej macro for processing histology images, outputs a series of binarized images filtered to exclude non-cellular particles
|── fig_5_analysis_code.py                          : analysis and plotting code for examining the columnar expression profile for artificial promoter AAVs
├── images/                                         : contains example images used for explanations within the README
│   └── figure_5.png                               
├── LICENSE.md                                      : license
└── README.md                                       : project description

```
<br>

## Modified excerpts (figure and methods) from O'Toole et al. 2023 relevant to this repository

<p align="center">
<img src="https://github.com/sean-otoole/aav_histology_otoole_2023/blob/main/images/figure_5.png" height= 500>
</p>

### Artificial promoters exhibited differential expression patterns in cortex
**(A)** Bulk RNA-sequencing data for Adamts2 expression in populations of L1, L2/3 and L4 cortical neurons infected with an AAV2/1-AP.Adamts2.1-eGFP vector, for high and low eGFP expressing populations separately. The low and high eGFP groups constitute the lower and upper thirds of the GFP fluorescence distribution (cells with no expression were excluded). Fold-change (FC) values were normalized to the average expression levels in the low eGFP group. Note all samples, each consisting of 1000 sorted cells, were collected in pairs, however, in some cases library preparation failed for one of the two samples accounting for unequal sample sizes in some cases (here and in other figure panels of this figure). Box plots mark the median and quartiles, whiskers extend to cover data up to ± 1.5 inter quartile range past the 75th and 25th quartiles respectively. *: p < 0.05, **: p < 0.01, ***: p < 0.001, n.s.: not significant; see Table S1 for all statistical information. 
**(B)** As in **A**, but for the AP.Agmat.1 promoter.  
**(C)** As in **A**, but for the AP.Baz1a.1 promoter. 
**(D-F)** As in **A-C**, but for Agmat expression. 
**(G-I)** As in **A-C**, but for Baz1a expression. 
___

### Methods
To determine the expression profile of viral vectors as a function of cortical depth, we used images corresponding to 200 mm in width
and spanning the entire depth of cortex. Image processing was done in FIJI where images were converted to 8-bit and then enhanced
for local contrast (CLAHE plugin, blocksize = 30, histogram = 256, maximum = 3). The images were then binarized with a cutoff value
corresponding to the 92.5 th percentile of pixel intensities (calculated for each image separately) and filtered for cellular particles. Bi-
narized images were converted to depth profiles by averaging in the horizontal dimension. All vectors were then scaled to an equal
length and normalized to peak. Finally, vectors were averaged across groups, normalized to peak, and passed through a Savitzky-
Golay filter.
