# Methods evaluation

Datasets : AAN and DBLP v12

Workflow:
 1. Creation of the test sets
 2. Compute the recommendation lists with the evaluated methods
 3. Compute the results with the different metrics applied to the recommendation lists
 4. Compare results (statically and graphically)

File description:
 - `data/` : preprocessed datasets (not in the repo)
 - `results/` : result files (not in the repo)
 - `scikit_posthocs/` : source files for posthocs (not in the repo)
 - `temp/` : some temp files created by methods (not in the repo)
 - `base_*.ipynb` : baselines
 - `compare_methods_*.ipynb` : comparing methods (deprecated)
 - `compare_methods_*_v2.ipynb` : comparing methods
 - `compute_metrics.ipynb` : compute metrics from recommendation lists (deprecated)
 - `compute_metrics_v2.ipynb` : compute metrics from recommendation lists
 - `creatingTestSets` : script for creating test sets
 - `custom_*.ipynb` : custom methods
 - `stateofart_*.ipynb` : state-of-art methods