from decimal import Decimal

from dipdup.models import Transaction
from tortoise.exceptions import DoesNotExist

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import kUSDHolder, Event, kUSDHolderSnapshot
from kolibri_indexer.types.fa12_token.storage import Fa12TokenStorage
from kolibri_indexer.types.fa12_token.parameter.mint import MintParameter
from dipdup.context import HandlerContext

async def on_kusd_mint(
    _ctx: HandlerContext,
    mint: Transaction[MintParameter, Fa12TokenStorage],
) -> None:
    try:
        mint_holder = await kUSDHolder.get(address=mint.parameter.address)
        mint_holder.kusd_holdings += Decimal(mint.parameter.value)
        await mint_holder.save()
    except DoesNotExist:
        mint_holder = await kUSDHolder.create(address=mint.parameter.address, kusd_holdings=Decimal(mint.parameter.value))

    await kUSDHolderSnapshot.create(
        address=mint_holder.address,
        level=mint.data.level,
        hash=mint.data.hash,
        kusd_holdings=mint_holder.kusd_holdings
    )

    print("Minted {:0.2f} to {}".format(Decimal(mint.parameter.value) / Decimal(1e18), mint.parameter.address))

    await log_event(
        mint,
        Event.KolibriAction.KUSD_MINT,
        {
            'minted': mint.parameter.value,
            'address': mint.parameter.address,
        }
    )
