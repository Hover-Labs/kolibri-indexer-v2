# generated by datamodel-codegen:
#   filename:  mint.json

from __future__ import annotations

from pydantic import BaseModel, Extra


class MintParameter(BaseModel):
    class Config:
        extra = Extra.forbid

    address: str
    value: str
