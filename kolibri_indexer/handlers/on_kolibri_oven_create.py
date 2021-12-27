from dipdup.models import Origination

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import KolibriOven, OvenFactory, Event
from kolibri_indexer.types.kolibri_oven.storage import KolibriOvenStorage
from dipdup.context import HandlerContext

async def on_kolibri_oven_create(
    ctx: HandlerContext,
    kolibri_oven_factory_origination: Origination[KolibriOvenStorage],
) -> None:
    created_oven = await KolibriOven.create(
        address = kolibri_oven_factory_origination.data.originated_contract_address,
        created = kolibri_oven_factory_origination.data.timestamp,
        borrowed_tokens = kolibri_oven_factory_origination.storage.borrowedTokens,
        interest_index = kolibri_oven_factory_origination.storage.interestIndex,
        is_liquidated = kolibri_oven_factory_origination.storage.isLiquidated,
        owner = kolibri_oven_factory_origination.storage.owner,
        stability_fee_tokens = kolibri_oven_factory_origination.storage.stabilityFeeTokens,
        current_delegate = (await OvenFactory.first()).initial_delegate,
        tez_deposited = 0
    )

    oven_key = 'kolibri_oven_{}'.format(kolibri_oven_factory_origination.data.originated_contract_address)

    # Dev shim to only watch one oven
    # if kolibri_oven_factory_origination.data.originated_contract_address == 'KT1KH3wH4sneEevPVW7AACiVKMjhTvmXLSK6':

    await ctx.add_contract(
        name=oven_key,
        address=kolibri_oven_factory_origination.data.originated_contract_address,
        typename='kolibri_oven'
    )

    # Start indexing this new oven immediately
    await ctx.add_index(
        oven_key,
        template='kolibri_oven',
        values={
            'kolibri_oven': oven_key
        }
    )

    event = await log_event(kolibri_oven_factory_origination, Event.KolibriAction.OVEN_CREATE, {"created_oven": created_oven.address})

    print("Created event {} - OVEN_CREATE - {}".format(event.id, event.target))

    print("Created oven {} owned by {}".format(created_oven.address, created_oven.owner))
