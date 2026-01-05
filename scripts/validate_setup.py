#!/usr/bin/env python3
"""
A quick test including:
    importing the package,
    loading config,
    resolving dataset paths,
    creating output directories.
"""

from __future__ import annotations

from aiops_hdfs.config import load_config
from aiops_hdfs.paths import raw_file, ensure_dirs
from aiops_hdfs.repro import set_global_seed

cfg = load_config("configs/default.yaml")
ensure_dirs(cfg)
set_global_seed(cfg.seed)

paths = {
    "event_traces": str(raw_file(cfg, cfg.data_files.event_traces)),
    "anomaly_labels": str(raw_file(cfg, cfg.data_files.anomaly_labels)),
    "hdfs_log": str(raw_file(cfg, cfg.data_files.hdfs_log)),
    "templates": str(raw_file(cfg, cfg.data_files.templates)),
    "time_order": str(raw_file(cfg, cfg.data_files.time_order)),
}

print("Loaded config OK:", cfg.name, "seed=", cfg.seed)
print("Resolved raw paths:")
for k, v in paths.items():
    print(" -", k, "=>", v)
