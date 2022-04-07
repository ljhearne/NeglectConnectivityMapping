# %%
import os
import glob
from tqdm import tqdm
import numpy as np
from nilearn.image import math_img

# ignore divide by 0 warning when normalising
np.seterr(divide='ignore', invalid='ignore')

# paths
proj_dir = '/home/lukeh/projects/NeglectNetworks/'
dsi_path = '/home/lukeh/projects/NeglectNetworks/tools/dsi-studio/'
lesn_dir = proj_dir+'data/derivatives/resampled_lesions/'
fib_file = proj_dir+'data/tractography_atlas/HCP842_1mm.fib.gz'
tract_file = proj_dir+'data/tractography_atlas/all_tracts_1mm.trk.gz'
out_dir = proj_dir+'data/derivatives/connectivity_lesions/'
out_dir_norm = proj_dir+'data/derivatives/connectivity_lesions_normalised/'

# get list of lesions to process
lesion_list = glob.glob(lesn_dir+'*.nii.gz')


def dsi_studio_wrapper(dsi_path, fib_file, tract_file, out_file, roi=None):

    # dsi command
    if roi is None:
        cmd = (dsi_path+'dsi_studio --action=ana '
               '--source='+fib_file+' '
               '--tract='+tract_file+' '
               '--output='+out_file+' '
               '--connectivity_type=end '
               '--connectivity_threshold=0   --export=tdi')
    else:
        cmd = (dsi_path+'dsi_studio --action=ana '
               '--source='+fib_file+' '
               '--tract='+tract_file+' '
               '--roi='+roi+' '
               '--output='+out_file+' '
               '--connectivity_type=end '
               '--connectivity_threshold=0  --export=tdi')

    # run the command
    if os.system(cmd) != 0:
        print('dsi command failed.')
        print(cmd)

    # remove the extra files - no use for it
    # and it is quite large
    os.remove(glob.glob(out_file+'*tt.gz')[0])


def generate_dmg():
    for lesion_file in tqdm(lesion_list):

        subjID = lesion_file.split(
            '/')[-1].split('.nii')[0].split('_Lesion')[0]

        dsi_studio_wrapper(dsi_path, fib_file, tract_file,
                           out_file=out_dir+subjID, roi=lesion_file)

        # use nilearn to divide subj data by normative data
        result_img = math_img('img1 / img2',
                              img1=out_dir+subjID+'.tdi.nii.gz',
                              img2=fib_file+'.tdi.nii.gz')
        result_img.to_filename(out_dir_norm+subjID+'_norm.tdi.nii.gz')


if __name__ == "__main__":

    # generate the normative fiber tracts in NIFTI space
    dsi_studio_wrapper(dsi_path, fib_file, tract_file, out_file=fib_file)

    # generate connectivity damage for all possible lesion maps
    generate_dmg()
