from decimal import Decimal
from enum import Enum

from tortoise import Model, fields

class kUSDHolder(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=36, unique=True, index=True)
    kusd_holdings = fields.DecimalField(max_digits=1000, decimal_places=0)

class LiquidityPoolHolder(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=36, unique=True, index=True)
    qlkusd_holdings = fields.DecimalField(max_digits=1000, decimal_places=0)

class SavingsRateHolder(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=36, unique=True, index=True)
    ksr_holdings = fields.DecimalField(max_digits=1000, decimal_places=0)

class TokenSnapshot(Model):
    class Contract(str, Enum):
        KUSD = 'kUSD'
        KDAO = 'kDAO'
        KSR = 'KSR'
        QLKUSD = 'QLkUSD'

    id = fields.IntField(pk=True)
    type = fields.CharEnumField(Contract)
    address = fields.CharField(max_length=36, index=True)
    level = fields.IntField()
    hash = fields.TextField()
    holdings = fields.DecimalField(max_digits=1000, decimal_places=0)

    def holdings_without_mantissa(self):
        if self.type in [self.Contract.KUSD, self.Contract.KDAO]:
            return self.holdings / Decimal(1e18)
        elif self.type in [self.Contract.KSR, self.Contract.QLKUSD]:
            return self.holdings / Decimal(1e36)
        else:
            raise Exception("Unknown contract {}".format(self.type))

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
    address = fields.CharField(max_length=36, index=True)
    created = fields.DatetimeField()
    borrowed_tokens = fields.DecimalField(max_digits=1000, decimal_places=0)
    interest_index = fields.DecimalField(max_digits=1000, decimal_places=0)
    is_liquidated = fields.BooleanField()
    owner = fields.CharField(max_length=36, index=True)
    stability_fee_tokens = fields.DecimalField(max_digits=1000, decimal_places=0)
    current_delegate = fields.TextField(null=True)
    tez_deposited = fields.DecimalField(max_digits=1000, decimal_places=0)

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

        KUSD_MINT = 'KUSD_MINT'
        KUSD_BURN = 'KUSD_BURN'
        KUSD_TRANSFER = 'KUSD_TRANSFER'

        SAVINGS_POOL_DEPOSIT = 'SAVINGS_POOL_DEPOSIT'
        SAVINGS_POOL_REDEEM = 'SAVINGS_POOL_REDEEM'
        SAVINGS_POOL_TRANSFER = 'SAVINGS_POOL_TRANSFER'

        ACCRUE_INTEREST_CALL = 'ACCRUE_INTEREST_CALL'

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
