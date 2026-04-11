from typing import List, Dict, Union, Optional
from pydantic import Field, RootModel
from .base_config import BaseConfig

class UpgradeEffect(BaseConfig):
    stat: str = Field(description="Attribute name on the Player class")
    op: str = Field(description="Operator: add, mul, set")
    value: Union[float, int, bool] = Field(description="Value to apply")

class UpgradeLimit(BaseConfig):
    stat: str = Field(description="Stat to check for limit")
    value: Union[float, int] = Field(description="Maximum or Minimum value allowed")

class UpgradeDefinition(BaseConfig):
    name: str
    description: str
    likelihood: int = 100
    is_active: bool = True
    effects: List[UpgradeEffect]
    one_time: bool = False
    limit: Optional[UpgradeLimit] = None

class UpgradesConfig(RootModel):
    root: Dict[str, Dict[str, UpgradeDefinition]]
    
    def __getattr__(self, name):
        # Proxies attribute access to the root dict
        return getattr(self.root, name)
    
    def __iter__(self):
        return iter(self.root)
        
    def __getitem__(self, item):
        return self.root[item]

    @property
    def categories(self):
        return self.root

    @classmethod
    def from_json(cls, path):
        import json
        with open(path, 'r') as f:
            data = json.load(f)
        return cls(root=data)
