
from kolibri_indexer.types.quipu_fa12_pool.storage import QuipuFa12PoolStorage
from kolibri_indexer.types.fa12_token.parameter.transfer import TransferParameter
from kolibri_indexer.types.quipu_fa12_pool.parameter.invest_liquidity import InvestLiquidityParameter
from dipdup.models import Transaction
from dipdup.context import HandlerContext
from kolibri_indexer.types.fa12_token.storage import Fa12TokenStorage

async def on_quipuswap_invest_liquidity(
    ctx: HandlerContext,
    invest_liquidity: Transaction[InvestLiquidityParameter, QuipuFa12PoolStorage],
    transfer: Transaction[TransferParameter, Fa12TokenStorage],
) -> None:
    print(invest_liquidity, transfer)
