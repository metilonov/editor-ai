from dataclasses import dataclass


@dataclass(frozen=True,slots=True)
class Effect:
    key:str
    description:str
