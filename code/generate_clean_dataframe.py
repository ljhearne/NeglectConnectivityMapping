'''
This code takes the original spreadsheet and the outputs that 
have been generated and creates a new dataframe with subject specific
links to the resampled lesion and connectivity data.

It outputs a .csv file that can be loaded into R for statistical
analyses with LESYMAP.
'''

# %%
import pandas as pd
import numpy as np
import glob


# paths
proj_dir = '/home/lukeh/projects/NeglectNetworks/'
src_dir = proj_dir+'data/sourcedata/'
lesn_dir = proj_dir+'data/derivatives/resampled_lesions/'
con_dir = proj_dir+'data/derivatives/connectivity_lesions'  # note the lack of /
out_dir = proj_dir+'data/derivatives/'
# the raw behavioural data spreadsheet
raw_ss = src_dir+'NetworkLM_Updated.xlsx'


def search_df_IDnum(df, df2, col, newcol):
    # loops through df to find possible ID matches
    # in df2. If found, the file in df2 is saved.
    # If none are found a nan is reported.

    for i, row in df.iterrows():

        # compare with parcel damage spreadsheet
        data = df2[df2[col].str.contains('(?i)p'+row.ID_num+'_')]

        # if there is relevant data
        if data.shape[0] == 1:
            data = data[col].values[0]

        elif data.shape[0] == 0:
            data = np.nan

        elif data.shape[0] > 1:
            # hard code the correct file when
            # there are multiple choices
            if row.ID_num == '6084':
                data = data[col].values[1]
            else:
                print('Odd data:')
                print('\tIDS', i, row.ID_num)
                print('\t', data[col])
                print('shape:', data.shape[0])

        # add to df
        df.loc[df.index[i], newcol] = data

    return df

# gets the (raw) behav spreadsheet and aligns it
# with all the generated data


if __name__ == "__main__":
    # get behavioural measure
    df = pd.read_excel(raw_ss)

    # assign ID numbers in raw df.
    # these are used going forward as the 'true' ID to match
    for i, row in df.iterrows():

        # extract the ID number by itself
        ID_num = row.ID.split('P')[-1]

        # add this into the df
        df.loc[df.index[i], 'ID_num'] = ID_num

    # 'raw' original lesions
    df2 = pd.DataFrame(
        glob.glob(src_dir+'lesions/'+'*.nii'), columns=['files'])
    df = search_df_IDnum(df, df2, 'files', 'raw_lesion_file')

    for loc, label in zip([lesn_dir,
                           con_dir+'/',
                           con_dir+'_normalised/',
                           con_dir+'_normalised_binarized-50/',
                           con_dir+'_normalised_binarized-80/'],
                          ['resampled_lesion_file',
                           'connectivity_lesion_file',
                           'connectivity_lesion_normalised_file',
                           'connectivity_lesion_normalised_binarized50_file',
                           'connectivity_lesion_normalised_binarized80_file']):

        # resampled lesions
        df2 = pd.DataFrame(glob.glob(loc+'*.nii.gz'), columns=['files'])
        df = search_df_IDnum(df, df2, 'files', label)

    # drop missing data
    print('Dropping the following missing data:',
          df[df.raw_lesion_file.isna()].ID.values)
    df = df.dropna(subset=['raw_lesion_file'])

    # reset the index
    df = df.reset_index(drop=True)
    df.to_csv(out_dir+'participant_dataframe.csv', index=False)

