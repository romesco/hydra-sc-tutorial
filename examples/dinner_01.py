from dataclasses import field, dataclass

from typing import List, Any

import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import OmegaConf, MISSING

# ---- L0 Configs for Low Level Tasks ----
@dataclass
class ShopConf:
    meats: List[str] = ('chicken',) 
    vegetables: List[str] = ('onions', 'peppers')

@dataclass
class CookConf:
    oven_temp: int = 350
    num_pans: int = 2

@dataclass
class DineConf:
    num_guests: int = MISSING 
    room: str = "dining"


# ---- L1 Config for Aggregating Tasks ----
@dataclass
class TasksConf:
    shop: ShopConf = ShopConf() 
    cook: CookConf = CookConf() 
    dine: DineConf = DineConf() 
 

# -------- Registration --------
cs = ConfigStore.instance()

# Top Level Config (in this example, L1 which is highest is `TasksConf`)
cs.store(name="toplvlconfig", node=TasksConf)


# -------- Hydra Entry Point --------
@hydra.main(config_name="toplvlconfig", config_path=None)
def dine(cfg):
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    dine()
