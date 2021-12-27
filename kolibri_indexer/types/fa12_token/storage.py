# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, Extra


class Balances(BaseModel):
    class Config:
        extra = Extra.forbid

    approvals: Dict[str, str]
    balance: str


class TokenMetadata(BaseModel):
    class Config:
        extra = Extra.forbid

    map: Dict[str, str]
    nat: str


class Fa12TokenStorage(BaseModel):
    class Config:
        extra = Extra.forbid

    administrator: str
    balances: Dict[str, Balances]
    debtCeiling: str
    governorContractAddress: str
    metadata: Dict[str, str]
    paused: bool
    token_metadata: Dict[str, TokenMetadata]
    totalSupply: str
