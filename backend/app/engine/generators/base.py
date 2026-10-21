from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional
import random


@dataclass
class TypeSpec:
    name: str = "generic"


@dataclass
class IntegerType(TypeSpec):
    min_val: int = -10**9
    max_val: int = 10**9
    name: str = "integer"


@dataclass
class StringType(TypeSpec):
    min_len: int = 0
    max_len: int = 10**5
    charset: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    name: str = "string"


@dataclass
class ArrayType(TypeSpec):
    element_type: TypeSpec = field(default_factory=lambda: IntegerType())
    min_size: int = 1
    max_size: int = 10**5
    allow_duplicates: bool = True
    name: str = "array"


@dataclass
class MatrixType(TypeSpec):
    element_type: TypeSpec = field(default_factory=lambda: IntegerType())
    min_rows: int = 1
    max_rows: int = 100
    min_cols: int = 1
    max_cols: int = 100
    name: str = "matrix"


class BaseGenerator(ABC):
    @abstractmethod
    def generate(self, spec: TypeSpec, rng: random.Random) -> Any:
        pass
