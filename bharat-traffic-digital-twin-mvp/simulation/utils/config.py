from dataclasses import dataclass
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[2]

@dataclass(frozen=True)
class SignalConfig:
    min_green: int = int(os.getenv("MIN_GREEN", "10"))
    max_green: int = int(os.getenv("MAX_GREEN", "60"))
    yellow: int = int(os.getenv("YELLOW_TIME", "3"))
    all_red: int = int(os.getenv("ALL_RED_TIME", "1"))

SIGNAL = SignalConfig()
