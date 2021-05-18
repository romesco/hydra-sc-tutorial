from dataclasses import field, dataclass

from typing import List, Any

import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import OmegaConf, MISSING

# ---- L0 Configs for Low Level Tasks ----
@dataclass
class DineConf:
    num_guests: int = MISSING 
    room: str = "dining"


# -------- Registration --------
cs = ConfigStore.instance()

# Top Level Config (in this example, L0 which is highest is `DineConf`)
cs.store(name="toplvlconfig", node=DineConf)


# -------- Hydra Entry Point --------
@hydra.main(config_name="toplvlconfig", config_path=None)
def dine(cfg):
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    dine()
