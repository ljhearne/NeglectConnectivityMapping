'''
Resample the raw lesion images to the desired 1mm space using 
nilearn.

Flip the lesions from radiological convention to neurological
convention.
'''
# %%
import nibabel as nib
from nilearn.image import resample_img, swap_img_hemispheres
from tqdm import tqdm
import glob

# paths
proj_dir = '/home/lukeh/projects/NeglectNetworks/'
lesn_dir = proj_dir+'data/sourcedata/lesions/'
out_dir = proj_dir+'data/derivatives/resampled_lesions/'

# template image
temp_img = nib.load(proj_dir+'data/parcellations/' +
                    'Schaefer_Tian_AAL/Schaefer_100_Tian_1_AAL.nii.gz')

# get a list of all the lesions
# note that no selection of data
# is done at this stage
lesion_list = glob.glob(lesn_dir+'*.nii')


def resample_lesions():
    # loop and resample
    for file in tqdm(lesion_list):

        # resample the image
        resampled_img = resample_img(file,
                                     target_affine=temp_img.affine,
                                     target_shape=temp_img.shape,
                                     interpolation='nearest')

        # convert to neurological convention (left-is-left)
        resampled_img = swap_img_hemispheres(resampled_img)

        # save as a new image
        filename = file.split('/')[-1].split('.nii')[0]
        nib.save(resampled_img, out_dir+filename+'_resampled.nii.gz')


if __name__ == "__main__":

    # resample and flip all lesion maps
    resample_lesions()
