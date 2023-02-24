# Evaluation

## Description

Source code of the evaluation of the recommend methods.

Used datasets:
 - ACL Anthology Network (http://clair.eecs.umich.edu/aan/index.php)
 - DBLP-Citation-network v11 (https://www.aminer.org/citation)
 - DBLP-Citation-network v12 (https://www.aminer.org/citation)

File description:
 - `datasets/` : used datasets (not in the repo)
 - `evaloff1_archives/` : first set of evaluations (deprecated)
 - `evaloff2_archives/` : second set of evaluations (deprecated)
 - `evaloff3/` : third set of evaluations
 - `loading_scripts/` : scripts to load data into databases (see prototype repo)
 - `analysing*.ipynb` : analysing datasets
 - `loading*.ipynb` : loading data to db (deprecated, see `loading_scripts/`)
 - `preprocessingAAN.ipynb` : preprocessing AAN
 - `preprocessingDBLP.ipynb` : preprocessing DBLP v11
 - `preprocessingDBLP_v12.ipynb` : preprocessing DBLP v12 for prototype
 - `preprocessingDBLP_v12_evaloff.ipynb` : preprocessing DBLP v12 for evaloff
 - `preprocessingDBLP_v12_part2.ipynb` : preprocessing DBLP v12 for prototype (part 2)
 
 ## Sources

This evaluation code was developed by Julien Albert, master student in CS at UNamur, during his
internship at the CETIC, under the supervision of Mathieu Goeminne (CETIC) and Benoît
Frenay (UNamur).

Master's Thesis : https://researchportal.unamur.be/fr/studentTheses/conception-dun-syst%C3%A8me-de-recommandation-de-litt%C3%A9rature-scientifi
