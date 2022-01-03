from decimal import Decimal

from kolibri_indexer.types.kolibri_oven.parameter.default import DefaultParameter
from dipdup.models import Transaction
from kolibri_indexer.types.kolibri_oven.storage import KolibriOvenStorage
from dipdup.context import HandlerContext

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import Event, KolibriOven

async def on_kolibri_oven_deposit(
    _ctx: HandlerContext,
    default: Transaction[DefaultParameter, KolibriOvenStorage],
) -> None:
    oven = await KolibriOven.get(address=default.data.target_address)

    oven.tez_deposited += Decimal(default.data.amount)

    await oven.save()

    event = await log_event(default, Event.KolibriAction.OVEN_DEPOSIT, {'deposit_amt': default.data.amount})

    print("Created event {} - OVEN_DEPOSIT - {}".format(event.id, event.target))
