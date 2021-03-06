# generated by datamodel-codegen:
#   filename:  assetMap_value.json

from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, Extra


class Prices(BaseModel):
    class Config:
        extra = Extra.forbid

    first: str
    last: str
    saved: Dict[str, str]
    sum: str


class Volumes(BaseModel):
    class Config:
        extra = Extra.forbid

    first: str
    last: str
    saved: Dict[str, str]
    sum: str


class AssetMapValue(BaseModel):
    class Config:
        extra = Extra.forbid

    computedPrice: str
    lastUpdateTime: str
    prices: Prices
    volumes: Volumes
