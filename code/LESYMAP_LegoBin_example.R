# This code uses the LESYMAP toolbox to run a univariate VLSM
# on regular lesion data and connectivity lesion data.
# I've just ran univariate methods because the multivariate method
# (sparse CCA) is really slow.

library(LESYMAP)

# project directory
proj_dir <- "/home/lukeh/projects/NeglectNetworks/"

# participant information spreadsheet
df_file <- paste(proj_dir, "data/derivatives/participant_dataframe.csv", sep = "")

# directory where results will be saved
res_dir <- paste(proj_dir, "data/derivatives/results/LEgoBin/", sep = "")

# read in the df
df <- read.csv(file = df_file)

## LESYMAP parameters
# for now I am using mostly defaults, worth looking through the manual as
# some of these choices interact, e.g., a univariate t-test method cannot use
# the "voxel" dTVLC correction method
min_subj <- 10
correctByLesSize <- "behavior" # this is the typical lesion size behaviour regression
multipleComparison <- "bonferroni"
# univariate analysis on typical lesion maps
# define the inputs
X <- imageFileNames2ImageList(as.character(df$resampled_lesion_file))
y <- as.numeric(df$LEgoBin)

# run the VLSM
lsm <- lesymap(X, y,
    method = "BMfast",
    multipleComparison = multipleComparison,
    minSubjectPerVoxel = min_subj,
    correctByLesSize = correctByLesSize,
    saveDir = paste(res_dir, "univariate_lesion", sep = "")
)

# univariate analysis on connectivity data
# change the X input
X <- imageFileNames2ImageList(as.character(df$connectivity_lesion_normalised_binarized80_file))

# run the VLSM
lsm <- lesymap(X, y,
    method = "BMfast",
    multipleComparison = multipleComparison,
    minSubjectPerVoxel = min_subj,
    correctByLesSize = correctByLesSize,
    saveDir = paste(res_dir, "univariate_connectivity", sep = "")
)
