from IPython.display import Image
import matplotlib
import matplotlib.image as mpimg
import matplotlib.colors
import numpy as np; np.random.seed(1)
import os
import matplotlib.pyplot as plt
from PIL import Image
from scipy import signal
import scipy
import math
from scipy import stats
from mpl_toolkits.axes_grid1 import make_axes_locatable

subdir = os.getcwd() + '/data_repository'

adamts2_dir = os.path.join(subdir, "Adamts2_processed")
adamts2_crop = os.path.join(subdir, "Adamts2_cropped")
baz1a_dir = os.path.join(subdir, "Baz1a_processed")
baz1a_crop = os.path.join(subdir, "Baz1a_cropped")
agmat_dir = os.path.join(subdir, "Agmat_processed")
agmat_crop = os.path.join(subdir, "Agmat_cropped")

example_dir = os.path.join(subdir, "example_photos_figure/process_example/processed_example")

adamts2_processed = adamts2_dir + '/' + os.listdir(adamts2_dir)[16]
img1 = mpimg.imread(adamts2_processed)
adamts2_crop_image = adamts2_processed.strip('_processed.png').replace('processed','cropped')+'.png'
img2 = mpimg.imread(adamts2_crop_image)

agmat_processed = agmat_dir + '/' + os.listdir(agmat_dir)[5]
img3 = mpimg.imread(agmat_processed)
agmat_crop_image = agmat_processed.strip('_processed.png').replace('processed','cropped')+'.png'
img4 = mpimg.imread(agmat_crop_image)

baz1a_processed = baz1a_dir + '/' + os.listdir(baz1a_dir)[5]
img5 = mpimg.imread(baz1a_processed)
baz1a_crop_image = baz1a_processed.strip('_processed.png').replace('processed','cropped')+'.png'
img6 = mpimg.imread(baz1a_crop_image)

figdir = os.getcwd() + '/code_generated_figures'

fig, ax = plt.subplots(1,6)
ax[0].imshow(img1)
plt.axis('off')
ax[1].imshow(img2);
plt.axis('off')
ax[2].imshow(img3);
plt.axis('off')
ax[3].imshow(img4);
plt.axis('off')
ax[4].imshow(img5);
plt.axis('off')
ax[5].imshow(img6);
plt.axis('off')
plt.savefig(os.path.join(figdir, "fig_5_example_density_images.pdf"), dpi = 300)

def get_vertical_vector(input_image):
    """This function takes an image
    and returns a 1 dimensional vector
    that is an average along the vertical
    axis"""
    img_array = mpimg.imread(input_image)
    img_vector = np.mean(img_array, axis=1)  #takes an average of the rows
    img_vector = img_vector[:,1]  #just take the first channel in the png
    return(img_vector)

def average_images_from_directory(input_dir):
    vertical_array_length = 200
    current_column = 0
    file_list = os.listdir(input_dir)
    averages_array = np.zeros(shape=(vertical_array_length,len(file_list)))
    for item in file_list:
        current_file = input_dir + '/' + item
        current_array = get_vertical_vector(current_file)
        current_array = signal.resample(current_array, vertical_array_length)
        if sum(current_array) == 0:
            print(item)
            continue
        current_array = current_array/np.amax(current_array) ## normalize the array
        averages_array[:, current_column] =  current_array
        current_column += 1
    std_dev = np.std(averages_array,1)
    row_means = averages_array.mean(axis=1)
    # Savitzky Golay Filtering
    row_means = scipy.signal.savgol_filter(row_means, 9, 1, deriv=0, delta=1.0, axis=- 1, mode='interp', cval=0.0)
    row_means = row_means/np.amax(row_means)  #normalize to the max values
    return(row_means,std_dev,averages_array)

example = average_images_from_directory(example_dir)
example_vector = example[0];

import matplotlib.pyplot as plt
import numpy as np; np.random.seed(1)
plt.rcParams["figure.figsize"] = 5,2

x = np.linspace(0, len(example_vector), num=len(example_vector), endpoint=True, retstep=False, dtype=None, axis=0)
y = example_vector
fig, (ax,ax2) = plt.subplots(nrows=2, sharex=True)

extent = [x[0]-(x[1]-x[0])/2., x[-1]+(x[1]-x[0])/2.,0,1]
ax.imshow(y[np.newaxis,:], cmap="gray", aspect="auto", extent=extent)
ax.set_yticks([])
ax.set_xlim(extent[0], extent[1])
ax2.plot(x,y)
plt.tight_layout()
plt.savefig('')
plt.savefig(os.path.join(figdir, "fig_5_agmat_example_heatmap.pdf"), dpi = 300)


adamts2_vector = average_images_from_directory(adamts2_dir)
agmat_vector = average_images_from_directory(agmat_dir)
baz1a_vector = average_images_from_directory(baz1a_dir)

x = range(adamts2_vector[2].shape[0])

adam_v_agmat = [];
adam_v_baz = [];
agmat_v_baz = [];

for n in x:
    first = adamts2_vector[2][n,]
    second = agmat_vector[2][n,]
    third = baz1a_vector[2][n,]
    adam_v_agmat_tmp = stats.ttest_ind(first, second, equal_var=False)[1]
    adam_v_agmat.append(adam_v_agmat_tmp)
    adam_v_baz_tmp = stats.ttest_ind(first, third, equal_var=False)[1]
    adam_v_baz.append(adam_v_baz_tmp)
    agmat_v_baz_tmp = stats.ttest_ind(second, third, equal_var=False)[1]
    agmat_v_baz.append(agmat_v_baz_tmp)
    
# remove signifgance values that only exist for only one or two points

def remove_sig_vals(input_array):
    output_array = input_array
    isolated_sig_indices = [i for i in range(0,len(output_array)) if list(output_array[i:i+3])==[0,1,0]]
    for i in isolated_sig_indices:
        output_array[i+1] = 0
    isolated_sig_indices = [i for i in range(0,len(output_array)) if list(output_array[i:i+4])==[0,1,1,0]]
    for i in isolated_sig_indices:
        output_array[i+1] = 0
        output_array[i+2] = 0
    return(output_array)

#threshold based on 0.05
adam_v_agmat = 1*(np.array(adam_v_agmat)<0.05)
adam_v_baz = 1*(np.array(adam_v_baz)<0.05)
agmat_v_baz = 1*(np.array(agmat_v_baz)<0.05)

#removing patterns  of 0-1-0 or 0-1-1-0
adam_v_agmat = remove_sig_vals(adam_v_agmat)
adam_v_baz = remove_sig_vals(adam_v_baz)
agmat_v_baz = remove_sig_vals(agmat_v_baz)

#scaling for easy plotting
adam_v_baz = adam_v_baz*0.66
agmat_v_baz = agmat_v_baz*0.33

plt.figure(1)

plt.subplot(211)
plt.plot(adamts2_vector[0],'y',label = 'adamts2')
plt.plot(agmat_vector[0], 'k',label = 'agmat')
plt.plot(baz1a_vector[0], 'b',label = 'baz1a')
plt.plot((adamts2_vector[0]+adamts2_vector[1]), label = 'adamts2 + error',c='0.85')
plt.plot((adamts2_vector[0]-adamts2_vector[1]), label = 'adamts2 - error',c='0.85')
plt.plot((agmat_vector[0]+agmat_vector[1]), label = 'agmat + error',c='0.85')
plt.plot((agmat_vector[0]-agmat_vector[1]), label = 'agmat - error',c= '0.85')
plt.plot((baz1a_vector[0]+baz1a_vector[1]), label = 'baz + error',c='0.85')
plt.plot((baz1a_vector[0]-baz1a_vector[1]), label = 'baz - error',c='0.85')

plt.subplot(212)
plt.plot(adam_v_agmat)
plt.plot(adam_v_baz)
plt.plot(agmat_v_baz)

# plt.legend(loc="none")
plt.savefig(os.path.join(figdir, "fig_5_ihc_curves_and_stats.pdf"), dpi = 300)

plt.rcParams["figure.figsize"] = 5,2

#x = np.linspace(-3,3)
x = np.linspace(0, len(adamts2_vector[0]), num=len(adamts2_vector[0]), endpoint=True, retstep=False, dtype=None, axis=0)
y = adamts2_vector[0]
fig, (ax,ax2) = plt.subplots(nrows=2, sharex=True)

extent = [x[0]-(x[1]-x[0])/2., x[-1]+(x[1]-x[0])/2.,0,1]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","#F9EA50",'#F18F26'])
ax.imshow(y[np.newaxis,:], cmap=cmap, aspect="auto", extent=extent)
ax.set_yticks([])
ax.set_xlim(extent[0], extent[1])
ax2.plot(x,y)
plt.tight_layout()
plt.savefig(os.path.join(figdir, "fig_5_adamts2_heatmap.pdf"), dpi = 300)

fig, ax = plt.subplots(figsize=(6, 1))
fig.subplots_adjust(bottom=0.5)
norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap,
                                norm=norm,
                                orientation='horizontal')
cb1.set_label('Units')
plt.savefig(os.path.join(figdir, "fig_5_adamts2_colorbar.pdf"), dpi = 300)

x = np.linspace(0, len(adamts2_vector), num=len(adamts2_vector[0]), endpoint=True, retstep=False, dtype=None, axis=0)
y = agmat_vector[0]
fig, (ax,ax2) = plt.subplots(nrows=2, sharex=True)

extent = [x[0]-(x[1]-x[0])/2., x[-1]+(x[1]-x[0])/2.,0,1]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","#757574","#3F3F3F"])
ax.imshow(y[np.newaxis,:], cmap=cmap, aspect="auto", extent=extent)
ax.set_yticks([])
ax.set_xlim(extent[0], extent[1])
ax2.plot(x,y)
plt.tight_layout()
plt.savefig(os.path.join(figdir, "fig_5_agmat_heatmap.pdf"), dpi = 300)

fig, ax = plt.subplots(figsize=(6, 1))
fig.subplots_adjust(bottom=0.5)
norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap,
                                norm=norm,
                                orientation='horizontal')
cb1.set_label('Units')
plt.savefig(os.path.join(figdir, "fig_5_agmat_colorbar.pdf"), dpi = 300)

x = np.linspace(0, len(adamts2_vector[0]), num=len(adamts2_vector[0]), endpoint=True, retstep=False, dtype=None, axis=0)
y = baz1a_vector[0]
fig, (ax1,ax2) = plt.subplots(nrows=2, sharex=True)
extent = [x[0]-(x[1]-x[0])/2., x[-1]+(x[1]-x[0])/2.,0,1]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","#43A9DE",'#272361'])
ax1.imshow(y[np.newaxis,:], cmap=cmap, aspect="auto", extent=extent)
ax1.set_yticks([])
ax1.set_xlim(extent[0], extent[1])
ax2.plot(x,y)
plt.tight_layout()
plt.savefig(os.path.join(figdir, "fig_5_baz_heatmap.pdf"), dpi = 300)

fig, ax = plt.subplots(figsize=(6, 1))
fig.subplots_adjust(bottom=0.5)
norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
cb1 = matplotlib.colorbar.ColorbarBase(ax, cmap=cmap,
                                norm=norm,
                                orientation='horizontal')
cb1.set_label('Units')
plt.savefig(os.path.join(figdir, "fig_5_baz_colorbar.pdf"), dpi = 300)