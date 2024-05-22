from enum import Enum
from typing import Any, TypeVar, Generic, Type, Dict
from plsp.__Debug_Context import Debug_Context

E1 = TypeVar('E1', bound=Enum)
E2 = TypeVar('E2', bound=Enum)

class EXPERIMENTAL_LOGGER (Generic[E1, E2]):
	xs: Dict[E1, Debug_Context]

	def __init__(self, first: Type[E1], second: Type[E2]):
		self._second = [item for item in second]
		for item in first:
			self.__add_debug_context(item)

	def __add_debug_context(self, item:"E1"):
		if item in self.xs:
			raise Exception(f"Debug context {item} already exists.")
		self.xs[item] = Debug_Context(item.name)


# Example Enums
class Contexts (Enum):
    GENERIC = ()

class Modes (Enum):
    APPLE = 1
    BANANA = 2
    CHERRY = 3

# Using the generic class
duo = EXPERIMENTAL_LOGGER(Contexts, Modes)

my_context = duo.xs[Contexts.GENERIC]