library(LESYMAP)

# project directory
proj_dir = '/home/lukeh/projects/NeglectNetworks/'

# participant information spreadsheet
df_file = paste(proj_dir,'data/derivatives/participant_dataframe.csv', sep='')

# directory where results will be saved
res_dir = paste(proj_dir,'data/derivatives/results/LEgoBin/', sep='')

# read in the df
df <- read.csv(file = df_file)

## LESYMAP parameters
# for now I am using mostly defaults, worth looking through the manual as
# some of these choices interact, e.g., a univariate t-test method cannot use 
# the "voxel" dTVLC correction method
min_subj = 10

# generic template for plotting
lesydata = file.path(find.package('LESYMAP'),'extdata')
template = antsImageRead(Sys.glob(file.path(lesydata, 'template', 'ch2.nii.gz')))

# univariate analysis on lesion maps

# define the inputs
X <- imageFileNames2ImageList(as.character(df$resampled_lesion_file))
y <- as.numeric(df$LEgoBin)

# run univariate lesion mapping 
lsm = lesymap(X, y, 
              method = 'BMfast', 
              minSubjectPerVoxel = min_subj,
              correctByLesSize = 'behavior',
              saveDir = paste(res_dir,'univariate_lesion', sep=''))

# plot the stat map if you are running interactively
plot(template, lsm$stat.img)

# run multivariate lesion mapping 
lsm = lesymap(X, y, 
              method = 'sccan', 
              minSubjectPerVoxel = min_subj,
              correctByLesSize = 'behavior',
              saveDir = paste(res_dir,'univariate_lesion', sep=''))

# plot the stat map if you are running interactively
plot(template, lsm$stat.img)
