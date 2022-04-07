'''
Creates binarized connectivity lesion maps for use in LESYMAP
'''
# %%
# create binary connectivity files
import os
import glob
from tqdm import tqdm
import numpy as np
from nilearn.image import binarize_img

# binarized threshold value
'''
Thresholds are arbitrary and hotly debated. From Griffis et al., (2021)
"By default, the threshold value is set to 50%, but it can be adjusted 
by the user, and we recommend comparing analysis results across 
thresholds to assess threshold dependency."
'''
thresholds = [0.5, 0.8]

# paths
proj_dir = '/home/lukeh/projects/NeglectNetworks/'
lesn_dir = proj_dir+'data/derivatives/connectivity_lesions_normalised/'
out_dir = proj_dir+'data/derivatives/'

# get list of lesions to process
lesion_list = glob.glob(lesn_dir+'*.nii.gz')

for thresh in thresholds:
    # create an output directory:
    thresh_dir = out_dir+'/connectivity_lesions_normalised_binarized-' + \
        str(int(thresh*100))+'/'

    if not os.path.exists(thresh_dir):
        os.makedirs(thresh_dir)

    # binarize all the lesions according to threshold
    for lesion_file in tqdm(lesion_list):
        subjID = lesion_file.split(
            '/')[-1].split('.nii')[0].split('_Lesion')[0]
        img = binarize_img(lesion_file, threshold=thresh)
        img.to_filename(thresh_dir+subjID+'_norm_bin-' +
                        str(int(thresh*100))+'.tdi.nii.gz')

# %%
