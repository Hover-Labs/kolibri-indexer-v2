
from dipdup.models import Transaction
from dipdup.context import HandlerContext

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import Event
from kolibri_indexer.types.kolibri_oven.parameter.liquidate import LiquidateParameter
from kolibri_indexer.types.kolibri_oven.storage import KolibriOvenStorage

async def on_kolibri_oven_liquidate(
    _ctx: HandlerContext,
    liquidate: Transaction[LiquidateParameter, KolibriOvenStorage],
) -> None:
    event = await log_event(liquidate, Event.KolibriAction.OVEN_LIQUIDATE, {'params': None})

    print("Created event {} - OVEN_LIQUIDATE - {}".format(event.id, event.target))
