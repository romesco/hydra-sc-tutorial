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
    defaults: List[Any] = field(
        default_factory=lambda: [
            "_self_",
            {"shop": "default"},
            {"cook": "default"},
            {"dine": "default"},
        ]
    )
    shop: ShopConf = MISSING
    cook: CookConf = MISSING
    dine: DineConf = MISSING


# ---- L2 Config for Tasks and Dinner Details ----
@dataclass
class DinnerConf:
    defaults: List[Any] = field(
        default_factory=lambda: [
            {"tasks": "default"},
            "_self_",
        ]
    )
    weekday: str = "Monday"
    organizer: str = "Alice"


# ---- Override Configs with 'Project' Configs ----
@dataclass
class ProjDinnerConf(DinnerConf):
    defaults: List[Any] = field(
        default_factory=lambda: [
            {"tasks": "default"},
            {"override tasks/cook": "proj"},
            "_self_",
        ]
    )
    weekday: str = "Monday"
    organizer: str = "Bob"

@dataclass
class ProjCookConf(CookConf):
    oven_temp = 400
    num_pans = 1


# -------- Registration --------
cs = ConfigStore.instance()

# Top Level Config (in this example, L2 which is highest is `DinnerConf`)
# It is then overriden by `ProjDinnerConf` which is a `DinnerConf`
cs.store(name="toplvlconfig", node=ProjDinnerConf)

# Default `TasksConf`
# Each of the default task nodes, `[Shop, Cook, Dine]Conf`
cs.store(group="tasks", name="default", node=TasksConf)
cs.store(group="tasks/shop", name="default", node=ShopConf)
cs.store(group="tasks/cook", name="default", node=CookConf)
cs.store(group="tasks/dine", name="default", node=DineConf)

# The overriding task node for the cook task, `ProjCookConf`
cs.store(group="tasks/cook", name="proj", node=ProjCookConf)


# -------- Hydra Entry Point --------
@hydra.main(config_name="toplvlconfig", config_path=None)
def dine(cfg):
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    dine()
