from enum import Enum

from tortoise import Model, fields

class kUSDHolder(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=36, unique=True)
    kusd_holdings = fields.DecimalField(max_digits=1000, decimal_places=0)

class kUSDHolderSnapshot(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=36, index=True)
    level = fields.IntField()
    hash = fields.TextField()
    kusd_holdings = fields.DecimalField(max_digits=1000, decimal_places=0)

class LiquidityPoolHolder(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=36, unique=True)
    qlkusd_holdings = fields.DecimalField(max_digits=1000, decimal_places=0)

class LiquidityPoolHolderSnapshot(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=36, index=True)
    level = fields.IntField()
    hash = fields.TextField()
    qlkusd_holdings = fields.DecimalField(max_digits=1000, decimal_places=0)

class HarbingerPrice(Model):
    id = fields.IntField(pk=True)
    timestamp = fields.DatetimeField()
    last_update_time = fields.DatetimeField()
    level = fields.IntField()
    computed_price = fields.DecimalField(max_digits=18, decimal_places=0)
    prices = fields.JSONField()
    volumes = fields.JSONField()

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

        LP_DEPOSIT = 'LP_DEPOSIT'
        LP_REDEEM = 'LP_REDEEM'
        LP_TRANSFER = 'LP_TRANSFER'

        KUSD_TRANSFER = 'KUSD_TRANSFER'
        KUSD_MINT = 'KUSD_MINT'
        KUSD_BURN = 'KUSD_BURN'

    id = fields.IntField(pk=True)
    level = fields.IntField()
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
