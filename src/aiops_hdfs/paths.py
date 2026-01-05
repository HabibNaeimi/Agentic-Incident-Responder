"""
Central path resolution utilities.
    This is for preventing hard-coded paths scattered across code. 
    The idea is to compute paths relative to repo root deterministically which will reduces
        running from a different working directory failure.
"""

from __future__ import annotations
from pathlib import Path
from .config import ProjectConfig

def repo_root() -> Path:
    # Assumes this file is at src/aiops_hdfs/paths.py
    return Path(__file__).resolve().parents[2]


def raw_file(cfg: ProjectConfig, filename: str) -> Path:
    return repo_root() / cfg.paths.raw_data_dir / filename


def ensure_dirs(cfg: ProjectConfig) -> None:
    root = repo_root()
    (root / cfg.paths.processed_data_dir).mkdir(parents=True, exist_ok=True)
    (root / cfg.paths.artifacts_dir).mkdir(parents=True, exist_ok=True)
    (root / cfg.paths.splits_dir).mkdir(parents=True, exist_ok=True)
    (root / cfg.paths.reports_dir).mkdir(parents=True, exist_ok=True)
    (root / cfg.paths.models_dir).mkdir(parents=True, exist_ok=True)
