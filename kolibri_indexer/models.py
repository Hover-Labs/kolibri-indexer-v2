from enum import IntEnum, Enum

from tortoise import Model, fields

class Transfer(Model):
    id = fields.IntField(pk=True)
    to_address = fields.TextField()
    from_address = fields.TextField()
    amount = fields.JSONField()
    from_alias = fields.TextField(default=None, null=True)
    timestamp = fields.DatetimeField()
    op_hash = fields.TextField()

class KolibriOven(Model):
    id = fields.IntField(pk=True)
    address = fields.TextField()
    created = fields.DatetimeField()
    borrowed_tokens = fields.JSONField()
    interest_index = fields.JSONField()
    is_liquidated = fields.BooleanField()
    owner = fields.TextField()
    stability_fee_tokens = fields.JSONField()
    current_delegate = fields.TextField(null=True)
    tez_deposited = fields.JSONField()

class Event(Model):
    class KolibriAction(str, Enum):
        OVEN_BORROW = 'OVEN_BORROW'
        OVEN_WITHDRAW = 'OVEN_WITHDRAW'
        OVEN_REPAY = 'OVEN_REPAY'
        OVEN_LIQUIDATE = 'OVEN_LIQUIDATE'
        OVEN_DEPOSIT = 'OVEN_DEPOSIT'
        OVEN_SET_DELEGATE = 'OVEN_SET_DELEGATE'
        OVEN_CREATE = 'OVEN_CREATE'

    id = fields.IntField(pk=True)
    sender = fields.TextField(null=True)
    target = fields.TextField(null=True)
    initiator = fields.TextField(null=True)
    action = fields.CharEnumField(KolibriAction)
    timestamp = fields.DatetimeField()
    data = fields.JSONField()

class OvenFactory(Model):
    address = fields.TextField()
    created = fields.DatetimeField()
    initial_delegate = fields.TextField(null=True)
