from dataclasses import dataclass
from BuildingUtil.building import Building
from typing import Generic, TypeVar
from abc import ABC, abstractmethod


@dataclass
class BuildEvent:
    """Event for building a building"""
    building: Building


@dataclass
class UpgradeEvent:
    """Event for upgrading a building"""
    building: Building


E = TypeVar('E', BuildEvent, UpgradeEvent)
"""Generic type for event"""


class Observer(ABC, Generic[E]):
    """Observer class for observer pattern"""
    @abstractmethod
    def update(self, event: E):
        pass


class Subject(Generic[E]):
    """Subject class for observer pattern"""

    def __init__(self):
        self._observers = set[Observer[E]]()

    def attach(self, observer: Observer[E]):
        self._observers.add(observer)

    def detach(self, observer: Observer[E]):
        self._observers.remove(observer)

    def notify(self, event: E):
        for observer in self._observers:
            observer.update(event)
