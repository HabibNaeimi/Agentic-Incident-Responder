# Agentic-Incident-Responder



## Directory Explanation

### src/
Our production-quality pipelines as something like a Python package.

### src/aiops_hdfs/
The actual package namespace is located here. 

### notebooks/
For experiments and investigation works.

### data/raw/
Place of raw, immutable inputs, aka Datasets.

### data/processed/
For datasets produced by preprocessing steps.

### models/
Including saved model weights and model metadeta (hyperparams, train date, metrics, data hash reference, etc.)

### reports/
Plots/tables/markdown/PDF summaries that explain what happened.

### configs/
Configuration files in order to not hard codeing dataset paths or hyperparameters.

### tests/
Automated ML pipelines tests. Mostly about parsing correctness, leakage checks, split integrity (no overlaps), and deterministic outputs.

### scripts/
Since the project is devided to a staged plan, here pleced the runnable entrypoints for each step in the plan. It makes every phase repeatable without the notebook.

### artifacts/
A critical “pipeline objects” in order for consistent inference and debugging. Parts of the model indluding vocabularies, scalers, thresholds, training metadata, data manifests, and reports of preprocessing. “everything that makes a run deterministic” in other word!

### splits/
Immutabe lists of BlockIds for train/val/test.



## Simple Mindmap of Project
1. Inputs
    + Data/

2. Pipeline engine
    + src/ (our library)
    + scripts/ (project steps)
    + configs/ (knobs)

3. Outputs
    + data/processed/ 
    + splits/ (the frozen IDs)
    + models/ (our trained models)
    + reports/ (plots, and summaries)
    + artifacts/ (transforms, thresholds, metadata, etc.)



## Citation
In this project we are gonna use dataset from the following papers.
+ Wei Xu, Ling Huang, Armando Fox, David Patterson, Michael Jordan. [Detecting Large-Scale System Problems by Mining Console Logs](https://people.eecs.berkeley.edu/~jordan/papers/xu-etal-sosp09.pdf), in Proc. of the 22nd ACM Symposium on Operating Systems Principles (SOSP), 2009.
+ Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. [Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics](https://arxiv.org/abs/2008.06448). IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023.