# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from typing import Dict, Optional

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


class LiquidityPoolStorage(BaseModel):
    class Config:
        extra = Extra.forbid

    balances: Dict[str, Balances]
    governorAddress: str
    metadata: Dict[str, str]
    ovenRegistryAddress: str
    quipuswapAddress: str
    rewardChangeAllowedLevel: str
    rewardPercent: str
    savedState_depositor: Optional[str]
    savedState_redeemer: Optional[str]
    savedState_tokensToDeposit: Optional[str]
    savedState_tokensToRedeem: Optional[str]
    state: str
    tokenAddress: str
    token_metadata: Dict[str, TokenMetadata]
    totalSupply: str
