from decimal import Decimal

from dipdup.models import Transaction
from tortoise.exceptions import DoesNotExist

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import kUSDHolder, Event, TokenSnapshot
from kolibri_indexer.types.fa12_token.parameter.burn import BurnParameter
from dipdup.context import HandlerContext
from kolibri_indexer.types.fa12_token.storage import Fa12TokenStorage

async def on_kusd_burn(
    _ctx: HandlerContext,
    burn: Transaction[BurnParameter, Fa12TokenStorage],
) -> None:
    mint_holder = await kUSDHolder.get(address=burn.parameter.address)
    mint_holder.kusd_holdings -= Decimal(burn.parameter.value)
    await mint_holder.save()

    print("Burned {:0.2f} to {}".format(Decimal(burn.parameter.value) / Decimal(1e18), burn.parameter.address))

    await TokenSnapshot.create(
        type=TokenSnapshot.Contract.KUSD,
        address=mint_holder.address,
        level=burn.data.level,
        hash=burn.data.hash,
        holdings=mint_holder.kusd_holdings
    )

    await log_event(
        burn,
        Event.KolibriAction.KUSD_BURN,
        {
            'burned': burn.parameter.value,
            'address': burn.parameter.address,
        }
    )
