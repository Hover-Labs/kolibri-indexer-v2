
from dipdup.models import Transaction

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import Event, KolibriOven
from kolibri_indexer.types.kolibri_oven.storage import KolibriOvenStorage
from dipdup.context import HandlerContext
from kolibri_indexer.types.kolibri_oven.parameter.default import DefaultParameter

async def on_kolibri_oven_deposit(
    _ctx: HandlerContext,
    default: Transaction[DefaultParameter, KolibriOvenStorage],
) -> None:
    print('This never appears D:')

    # TODO: Update oven tez_balance
    #oven = await KolibriOven.get(address=default.data.target_address)

    event = await log_event(default, Event.KolibriAction.OVEN_DEPOSIT, {'params': default.parameter.__root__,})

    print("Created event {} - OVEN_DEPOSIT - {}".format(event.id, event.target))
