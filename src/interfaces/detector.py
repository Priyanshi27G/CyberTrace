from abc import ABC, abstractmethod
from typing import Optional
from src.models.packet import PacketData
from src.models.alert import Alert

class IDetector(ABC):
    @abstractmethod
    def detect(self, packet: PacketData) -> Optional[Alert]:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def reset(self) -> None:
        pass
