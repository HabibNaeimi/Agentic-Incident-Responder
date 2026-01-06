from __future__ import annotations
import argparse, logging
from pathlib import Path
from aiops_hdfs.config import load_config
from aiops_hdfs.logging_utils import setup_logging
from aiops_hdfs.paths import repo_root, ensure_dirs, raw_file
from aiops_hdfs.data.event_sequences import parse_event_sequences_to_jsonl_gz
from aiops_hdfs.data.event_sequences import write_report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, default="configs/default.yaml")
    ap.add_argument("--chunksize", type=int, default=50_000)
    args = ap.parse_args()
    setup_logging(logging.INFO)
    cfg = load_config(args.config)
    ensure_dirs(cfg)
    input_csv = raw_file(cfg, cfg.data_files.event_traces)
    out_jsonl = repo_root() / cfg.paths.processed_data_dir / "event_sequences.jsonl.gz"
    out_report = repo_root() / cfg.paths.artifacts_dir / "phase1_step1_parse_events_report.json"
    report = parse_event_sequences_to_jsonl_gz(
        input_csv=input_csv,
        output_jsonl_gz=out_jsonl,
        chunksize=args.chunksize,
    )

    write_report(report, out_report)
    
    logging.getLogger(__name__).info("Wrote parsed sequences: %s", out_jsonl)
    logging.getLogger(__name__).info("Wrote report: %s", out_report)
    logging.getLogger(__name__).info(
        "Summary: rows=%d empty_sequences=%d max_len=%d p95_len=%.1f",
        report.rows_out, report.empty_sequences, report.max_len, report.p95_len
    )

if __name__ == "__main__":
    main()