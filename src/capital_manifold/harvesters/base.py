from __future__ import annotations
import abc
import logging
from typing import List, Dict, Any
import httpx
from capital_manifold.core.schema import FlowEvent

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("capital_manifold.harvester")

class BaseHarvester(abc.ABC):
    """Abstract base class for high-frequency and low-frequency balance sheet harvesters."""
    
    def __init__(self, name: str, user_agent: str = "CapitalManifold/1.0 (Macro Research Autonomous Engine)"):
        self.name = name
        self.user_agent = user_agent
        self.client = httpx.Client(
            headers={
                "User-Agent": self.user_agent,
                "Accept": "*/*",
            },
            timeout=30.0,
            follow_redirects=True,
        )

    @abc.abstractmethod
    def harvest(self) -> List[FlowEvent]:
        """Execute extraction and return standardized FlowEvents."""
        pass

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
