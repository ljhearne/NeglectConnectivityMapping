# Neglect Connectivity Mapping Project

## Lesion Connectivity Preprocessing
White matter connectivity 'disconnection' maps were generated in line with methods published in the Lesion Quantification Toolkit [1]. The normative connectome used is from Yeh et al., 2018 [2] and is based on 842 participants from the Human Connectome Project. For a good overview of the analysis pros and cons I would read section 2.5.3. ("White matter disconnection maps") in [1].

### Pipeline
- _resample_flip_lesions.py_: Resample lesion maps to the same space as the Yeh et al., normative connectome (1mm) and convert to neurological convention (flip left and right). Located in _data/derivatives/resampled_lesions/_.
- _generate_connectivity_damage.py_: Takes each individuals lesion map and estimates connectivity damage using dsi studio [3]. Several parameter choices are made here that match the Lesion Quantification Toolkit. These results are generated in voxel space:
    - __absolute estimates of disconnection:__ voxel values correspond to the densities of disconnected streamlines within each voxel. Located in _data/derivatives/connectivity_lesions/_.
    - __normalised estimates of disconnection:__ voxel values correspond to the percentage of all of the streamlines contained within each voxel (i.e., computed from the HCP-842 streamline tractography atlas) that are expected to be disconnected by the lesion. Located in _data/derivatives/connectivity_lesions_normalised/_.
- _generate_binarized_connectivity.py_: Generates binary maps of connectivity damage.
    - __binarized, normalised estimates of disconnection:__ voxel values represent where at least X% of streamlines in a voxel are thought to be disconnected. This step is important for using traditional VLSM mapping tools where binarized input data are needed. Located in _data/derivatives/connectivity_lesions_normalised_binarized/_.
- _generate_clean_dataframe.py_: Takes the original participant spreadsheet and matches all the subject-specific file locations and behavioural data to generate a dataframe that can be loaded into R for analysis. Located in _data/derivatives/_.

## Statistical analysis
Statistical analysis is performed using LESYMAP [4]. This allows for flexible analysis with several important parameters including, for example, controlling for lesion size, lesion participant number cutoffs and univariate vs. multivariate options.

- _LESYMAP_LegoBin_example.R_:
Produces output in the results folder: /data/derivatives/results. It runs through two univariate analysis examples - one for regular lesion maps and one for connectivity lesion maps.

## Notebooks
- _Preprocessing example.ipynb_: Displays the output of preprocessing for single subjects and plots the group level maps.
- _LegoBin_example.ipynb_: Plots the outputs of the LESYMAP analyses.

## File directory
```
├── code
├── data (not on github, sent via Box)
│   ├── derivatives
│   │   ├── connectivity_lesions
│   │   ├── connectivity_lesions_normalised
│   │   ├── connectivity_lesions_normalised_binarized-50
│   │   ├── connectivity_lesions_normalised_binarized-80
│   │   ├── resampled_lesions
│   │   ├── results/LEgoBin
│   │   └── participant_dataframe.csv
│   ├── sourcedata (raw data from M.M.)
│   └── tractography_atlas (Yeh et al., atlas)
└── notebooks
    ├── Connectivity Preprocessing Example.ipynb
    └── Left Ego Neglect Example.ipynb
```

## References
[1] Griffis, Joseph C., et al. "Lesion Quantification Toolkit: A MATLAB software tool for estimating grey matter damage and white matter disconnections in patients with focal brain lesions." NeuroImage: Clinical 30 (2021): 102639.
- https://www.sciencedirect.com/science/article/pii/S2213158221000838

[2] Yeh, Fang-Cheng, et al. "Population-averaged atlas of the macroscale human structural connectome and its network topology." Neuroimage 178 (2018): 57-68

[3] Yeh, F. C. "Diffusion mri reconstruction in dsi studio." Advanced Biomedical MRI Lab, National Taiwan University Hospital. Available online at: http://dsi-studio. labsolver. org/Manual/Reconstruction# TOC-Q-Space-Diffeomorphic-Reconstruction-QSDR (2017).

[4] Pustina, Dorian, et al. "Improved accuracy of lesion to symptom mapping with multivariate sparse canonical correlations." Neuropsychologia 115 (2018): 154-166.
- https://raw.githubusercontent.com/dorianps/LESYMAP/master/LESYMAP.pdf (manual)
- https://github.com/dorianps/LESYMAP (github)
