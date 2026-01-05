"""
The idea is defining a typed configuration object and a YAML loader 
    in order to have consistent config parsing, strongly structured access, 
    and also allowing validation later.

"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
import yaml

@dataclass(frozen=True)
class Paths:
    raw_data_dir: Path
    processed_data_dir: Path
    artifacts_dir: Path
    splits_dir: Path
    reports_dir: Path
    models_dir: Path


@dataclass(frozen=True)
class DataFiles:
    event_traces: str
    anomaly_labels: str
    hdfs_log: str
    templates: str
    time_order: str


@dataclass(frozen=True)
class ProjectConfig:
    name: str
    seed: int
    paths: Paths
    data_files: DataFiles


def load_config(config_path: str | Path) -> ProjectConfig:
    config_path = Path(config_path)
    with config_path.open("r", encoding="utf-8") as f:
        cfg: Dict[str, Any] = yaml.safe_load(f)

    proj = cfg.get("project", {})
    paths = cfg.get("paths", {})
    files = cfg.get("data_files", {})

    p = Paths(
        raw_data_dir=Path(paths["raw_data_dir"]),
        processed_data_dir=Path(paths["processed_data_dir"]),
        artifacts_dir=Path(paths["artifacts_dir"]),
        splits_dir=Path(paths["splits_dir"]),
        reports_dir=Path(paths["reports_dir"]),
        models_dir=Path(paths["models_dir"]),
    )
    df = DataFiles(
        event_traces=files["event_traces"],
        anomaly_labels=files["anomaly_labels"],
        hdfs_log=files["hdfs_log"],
        templates=files.get("templates", "HDFS.log_templates.csv"),
        time_order=files.get("time_order", "Time_Order.csv"),
    )

    return ProjectConfig(
        name=str(proj.get("name", "aiops-hdfs")),
        seed=int(proj.get("seed", 1337)),
        paths=p,
        data_files=df,
    )
