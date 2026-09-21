from abc import ABC, abstractmethod
from typing import List
from src.models.packet import PacketData

class IDataSource(ABC):
    @abstractmethod
    def start(self) -> None:
        pass
    
    @abstractmethod
    def stop(self) -> None:
        pass
    
    @abstractmethod
    def get_packets(self, count: int = 100) -> List[PacketData]:
        pass
    
    @abstractmethod
    def is_active(self) -> bool:
        pass
