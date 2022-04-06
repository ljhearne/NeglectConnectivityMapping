# Neglect Connectivity Mapping Project

## Lesion Connectivity Preprocessing
White matter connectivity 'disconnection' maps were generated in line with methods published in the Lesion Quantification Toolkit [1]. The normative connectome used is from Yeh et al., 2018 [2] and is based on 842 participants from the Human Connectome Project.

### Pipeline
- _resample_flip_lesions.py_: Resample lesion maps to the same space as the Yeh et al., normative connectome (1mm) and convert to neurological convention (flip left and right). Located in _data/derivatives/resampled_lesions/_.
- _generate_connectivity_damage.py_: Takes each individuals lesion map and estimates connectivity damage using dsi studio [3]. Several parameter choices are made here that match the Lesion Quantification Toolkit. Two results are generated in voxel space - absolute estimates of disconnection and normalised estimates. Located in _data/derivatives/connectivity_lesions/_.
- _generate_clean_dataframe.py_: Takes the original participant spreadsheet and matches all the subject-specific file locations and behavioural data to generate a dataframe that can be loaded into R. Located in _data/derivatives/_.

## Statistical analysis
Statistical analysis is performed using LESYMAP [4]. This allows for flexible analysis with several important parameters including, for example, controlling for lesion size, lesion participant number cutoffs and univariate vs. multivariate options.

- _LESYMAP_LegoBin_example.R_:
Produces output in the results folder

## Notebooks
- _Preprocessing example.ipynb_:
- _LegoBin_example.ipynb_:

## File directory
```
├── code
├── data
│   ├── derivatives
│   │   ├── connectivity_lesions
│   │   └── resampled_lesions
│   ├── sourcedata (data from Margaret M.)
│   │   └── lesions
│   └── tractography_atlas (Yeh et al., atlas)
└── notebooks
    ├── 
    └── 
```

## References
[1] Griffis, Joseph C., et al. "Lesion Quantification Toolkit: A MATLAB software tool for estimating grey matter damage and white matter disconnections in patients with focal brain lesions." NeuroImage: Clinical 30 (2021): 102639.
- https://www.sciencedirect.com/science/article/pii/S2213158221000838

[2] Yeh, Fang-Cheng, et al. "Population-averaged atlas of the macroscale human structural connectome and its network topology." Neuroimage 178 (2018): 57-68

[3] Yeh, F. C. "Diffusion mri reconstruction in dsi studio." Advanced Biomedical MRI Lab, National Taiwan University Hospital. Available online at: http://dsi-studio. labsolver. org/Manual/Reconstruction# TOC-Q-Space-Diffeomorphic-Reconstruction-QSDR (2017).

[4] Pustina, Dorian, et al. "Improved accuracy of lesion to symptom mapping with multivariate sparse canonical correlations." Neuropsychologia 115 (2018): 154-166.
- https://raw.githubusercontent.com/dorianps/LESYMAP/master/LESYMAP.pdf (manual)
- https://github.com/dorianps/LESYMAP (github)
