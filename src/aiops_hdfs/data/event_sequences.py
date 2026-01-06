"""
THis script will serve as a pursing modul in order to detect BlockID and Features columns and
    parsing events via regex. Also we have chunked streams of data so that not facing any memory isssue. 
"""

from __future__ import annotations
import gzip, json, logging, re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Optional, Tuple
import pandas as pd

logger = logging.getLogger(__name__)

EVENT_RE = re.compile(r"E\d+")   # The regex for our event since they're "E1, E2, etc."

# The column names were BlockId and Features as checked but these are all the variations. 
BLOCKID_CANDIDATES = ["BlockId", "BlockID", "block_id", "blk_id", "blockid"]
FEATURES_CANDIDATES = ["Features", "features", "Sequence", "sequence", "EventSequence", "Events"]

@dataclass(frozen=True)
class ParseReport:
    input_csv: str
    output_jsonl_gz: str
    rows_in: int
    rows_out: int
    min_len: int
    max_len: int
    mean_len: int
    p50_len: int
    p95_len: int
    p99_len: int
    blockid_col: str
    features_col: str
    empty_sequences: int
    sample_rows: list[dict]

def detect_columns(csv_path: Path) -> Tuple[str, str]:
    """
    Detect BlockId and Features columns by reading only the header.
    """

    header = pd.read_csv(csv_path, nrows=0)           # nrows=0 means header!
    cols = list(header.columns)

    def pick(candidates: list[str]) -> Optional[str]:
        # Checking for exact match first
        for candidate in candidates:
            if candidate in cols:
                return candidate
            
        # Checking for case insensitive matches
        lower_map = {c.lower(): c for c in cols}
        for candidate in candidates:
            if candidate.lower() in lower_map:
                return lower_map[candidate.lower()]
            return None
    

    block_col = pick(BLOCKID_CANDIDATES)
    feat_col = pick(FEATURES_CANDIDATES)

    if not block_col or not feat_col:
        raise ValueError(
            f"Could not detect required columns. Found columns={cols}. "
            f"Need one of BlockId candidates={BLOCKID_CANDIDATES} and "
            f"Features candidates={FEATURES_CANDIDATES}."
        )

    return block_col, feat_col

def extract_event_tokens(features: str) -> list[str]:
    """
    Converting one Features cell into a list of event IDs.
    Considerations:
    - Using EVENT_RE that we defines earlier, regex findall is robust to formats like:
      "E1 E2 E3", "['E1','E2']", "[E1, E2]", etc.
    - Returns [] for empty or invalid strings then count these and report.
    """    
    if features is None:
        return []
    
    s = str(features)        # Ensure string (pandas might pass non-str)

    if not s or s.strip == "":
        return []
    
    return EVENT_RE.findall(s)

def parse_event_sequences_to_jsonl_gz(
        input_csv: Path,
        output_jsonl_gz: Path,
        chunksize: int = 50_000,
) -> ParseReport:
    """
    Stream-read Event_traces.csv, parse Features -> EventSequence, write JSONL.GZ:
      {"BlockId":"...", "EventSequence":["E1","E2",...]}
    """
    # Detecting ID and features columns.
    block_col, feat_col = detect_columns(input_csv)
    # Logging them.
    logger.info("Detected columns: blockid_col=%s, features_col=%s", block_col, feat_col)  

    output_jsonl_gz.parent.mkdir(parents=True, exist_ok=True)
    rows_in = 0
    rows_out = 0
    empty_sequences = 0
    lengths: list[int] = []
    sample_rows: list[dict] = []

    reader = pd.read_csv(
        input_csv,
        usecols=[block_col, feat_col],
        dtype=str,
        keep_default_na=False,
        chunksize=chunksize,
    )

    with gzip.open(output_jsonl_gz, "wt", encoding="utf-8") as f:
        for chunk_idx, chunk in enumerate(reader):
            rows_in += len(chunk)
            seqs = chunk[feat_col].str.findall(EVENT_RE)
            chunk_lens = seqs.str.len().astype(int)
            lengths.extend(chunk_lens.tolist())
            empty_sequences += int((chunk_lens == 0).sum())

            out_lines: list[str] = []            # Preparing JSONL lines per chunk
            for bid, seq in zip(chunk[block_col].tolist(), seqs.tolist()):
                rec = {"BlockId": bid, "EventSequence": seq}
                if len(sample_rows) < 5:
                    sample_rows.append(rec)
                out_lines.append(json.dumps(rec, ensure_ascii=False))

            f.write("\n".join(out_lines))
            f.write("\n")
            rows_out += len(out_lines)

            if chunk_idx % 5 == 0:
                logger.info("Processed chunks=%d rows_in=%d", chunk_idx + 1, rows_in)
        
    if rows_out != rows_in:
        raise RuntimeError(f"Row count mismatch: rows_in={rows_in}, rows_out={rows_out}")
    
    if not lengths:
        raise RuntimeError("No rows parsed; check input file and detected columns.")
    
    s = pd.Series(lengths)
    report = ParseReport(
        input_csv=str(input_csv),
        output_jsonl_gz=str(output_jsonl_gz),
        rows_in=rows_in,
        rows_out=rows_out,
        empty_sequences=empty_sequences,
        min_len=int(s.min()),
        max_len=int(s.max()),
        mean_len=float(s.mean()),
        p50_len=float(s.quantile(0.50)),
        p95_len=float(s.quantile(0.95)),
        p99_len=float(s.quantile(0.99)),
        blockid_col=block_col,
        features_col=feat_col,
        sample_rows=sample_rows,
    )

    return report

def write_report(report: ParseReport, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(asdict(report), indent=2, sort_keys=True), encoding="utf-8")
