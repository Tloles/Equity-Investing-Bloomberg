"""
finviz_fetcher.py — scrapes Finviz for supplementary peer lists and
fundamental metrics.  This is a best-effort, fire-and-forget fetch that
runs in parallel with FMP calls.  Any failure degrades gracefully.

Requires: finvizfinance  (pip install finvizfinance)
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# ── Data container ─────────────────────────────────────────────────────────────

@dataclass
class FinvizData:
    ticker: str
    peers: List[str] = field(default_factory=list)
    metrics: Dict[str, str] = field(default_factory=dict)

    # Parsed numeric / string fields
    analyst_target: Optional[float] = None
    analyst_recom:  Optional[float] = None   # 1=Strong Buy … 5=Strong Sell
    forward_pe:     Optional[float] = None
    peg:            Optional[float] = None
    ps:             Optional[float] = None
    pb:             Optional[float] = None
    pfcf:           Optional[float] = None
    beta:           Optional[float] = None

    # Kept as strings because they carry % signs
    roe:            Optional[str] = None
    dividend_yield: Optional[str] = None
    insider_own:    Optional[str] = None
    inst_own:       Optional[str] = None


# ── Helpers ────────────────────────────────────────────────────────────────────

_FLOAT_KEYS = {
    "analyst_target": "Target Price",
    "analyst_recom":  "Recom",
    "forward_pe":     "Forward P/E",
    "peg":            "PEG",
    "ps":             "P/S",
    "pb":             "P/B",
    "pfcf":           "P/FCF",
    "beta":           "Beta",
}

_STR_KEYS = {
    "roe":            "ROE",
    "dividend_yield": "Dividend %",
    "insider_own":    "Insider Own",
    "inst_own":       "Inst Own",
}


def _parse_float(value: Optional[str]) -> Optional[float]:
    if not value or value == "-":
        return None
    try:
        return float(value.replace(",", "").replace("%", "").strip())
    except (ValueError, AttributeError):
        return None


# ── Main entry point ───────────────────────────────────────────────────────────

def fetch_finviz(ticker: str) -> FinvizData:
    """
    Fetch Finviz fundamentals and peer list for *ticker*.
    Returns a FinvizData with empty/None fields on any error.
    """
    ticker = ticker.upper()
    empty  = FinvizData(ticker=ticker)

    try:
        from finvizfinance.quote import finvizfinance  # local import — optional dep

        fv = finvizfinance(ticker)

        # ── Fundamentals dict (90+ key/value pairs) ────────────────────────
        fundament: Dict[str, str] = fv.ticker_fundament() or {}
        print(f"[Finviz] {ticker}: got {len(fundament)} fundamental keys")

        # ── Peer list ──────────────────────────────────────────────────────
        try:
            raw_peers = fv.ticker_peer() or []
            peers = [p for p in raw_peers if p and p != ticker]
        except Exception as exc:
            print(f"[Finviz] {ticker}: peer fetch failed — {exc}")
            peers = []

        print(f"[Finviz] {ticker}: {len(peers)} peers — {peers}")

        # ── Parse floats ───────────────────────────────────────────────────
        parsed_floats: Dict[str, Optional[float]] = {}
        for field_name, fv_key in _FLOAT_KEYS.items():
            val = _parse_float(fundament.get(fv_key))
            parsed_floats[field_name] = val

        # ── Keep strings ───────────────────────────────────────────────────
        parsed_strs: Dict[str, Optional[str]] = {}
        for field_name, fv_key in _STR_KEYS.items():
            raw = fundament.get(fv_key)
            parsed_strs[field_name] = raw if raw and raw != "-" else None

        # Be polite to Finviz servers
        time.sleep(1)

        return FinvizData(
            ticker        = ticker,
            peers         = peers,
            metrics       = fundament,
            analyst_target = parsed_floats["analyst_target"],
            analyst_recom  = parsed_floats["analyst_recom"],
            forward_pe     = parsed_floats["forward_pe"],
            peg            = parsed_floats["peg"],
            ps             = parsed_floats["ps"],
            pb             = parsed_floats["pb"],
            pfcf           = parsed_floats["pfcf"],
            beta           = parsed_floats["beta"],
            roe            = parsed_strs["roe"],
            dividend_yield = parsed_strs["dividend_yield"],
            insider_own    = parsed_strs["insider_own"],
            inst_own       = parsed_strs["inst_own"],
        )

    except Exception as exc:
        print(f"[Finviz] {ticker}: FAILED — {type(exc).__name__}: {exc}")
        return empty
