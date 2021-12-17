
from dipdup.models import Transaction

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.types.kolibri_oven.storage import KolibriOvenStorage
from dipdup.context import HandlerContext
from kolibri_indexer.types.kolibri_oven.parameter.set_delegate import SetDelegateParameter

from kolibri_indexer.models import KolibriOven, Event


async def on_kolibri_oven_set_delegate(
    _ctx: HandlerContext,
    set_delegate: Transaction[SetDelegateParameter, KolibriOvenStorage],
) -> None:
    kolibri_oven = await KolibriOven.get(address=set_delegate.data.target_address)
    kolibri_oven.current_delegate = set_delegate.parameter.__root__
    await kolibri_oven.save()

    event = await log_event(set_delegate, Event.KolibriAction.OVEN_SET_DELEGATE, {'params': set_delegate.parameter.__root__, })
    print("Created event {} - OVEN_SET_DELEGATE - {}".format(event.id, event.target))

    print("Oven {} updated delegate to {}".format(kolibri_oven.address, kolibri_oven.current_delegate))
