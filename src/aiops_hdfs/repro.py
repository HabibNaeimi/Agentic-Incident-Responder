"""
The idea is to set random seeds across Python/NumPy/PyTorch.
"""

from __future__ import annotations
import os
import random
from typing import Optional
import numpy as np

def set_global_seed(seed: int, torch_deterministic: bool = True) -> None:
    """Set seeds for reproducibility.

    torch_deterministic=True enables deterministic algorithms where possible.
    Note: full determinism can reduce performance and may not be supported for all ops.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    try:
        import torch

        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

        if torch_deterministic:
            torch.use_deterministic_algorithms(True)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except Exception:
        # Torch might not be installed yet; that's fine until Phase 3.
        pass
