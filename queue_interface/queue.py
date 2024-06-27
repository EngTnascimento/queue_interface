from abc import ABC, abstractmethod
from typing import Generator

from .queue_setup import QueueSetup


class Queue(ABC):
    def __init__(self, setup: QueueSetup) -> None:
        super().__init__()
        self.setup: QueueSetup = setup

    @abstractmethod
    def send(self, message):
        pass

    @abstractmethod
    def receive(self) -> Generator:
        pass

    @abstractmethod
    def close(self):
        pass
