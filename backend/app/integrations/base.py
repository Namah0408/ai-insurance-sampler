from abc import ABC, abstractmethod
from typing import Any
import uuid


class ExternalIntegration(ABC):

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def check(self, proposal_id: uuid.UUID) -> dict[str, Any]:
        pass