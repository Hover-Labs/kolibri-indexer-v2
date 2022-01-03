
from dipdup.models import OperationData
from kolibri_indexer.types.quipu_fa12_pool.parameter.divest_liquidity import DivestLiquidityParameter
from dipdup.models import Transaction
from kolibri_indexer.types.fa12_token.parameter.transfer import TransferParameter
from kolibri_indexer.types.fa12_token.storage import Fa12TokenStorage
from dipdup.context import HandlerContext
from kolibri_indexer.types.quipu_fa12_pool.storage import QuipuFa12PoolStorage

async def on_quipuswap_divest_liquidity(
    ctx: HandlerContext,
    divest_liquidity: Transaction[DivestLiquidityParameter, QuipuFa12PoolStorage],
    transfer: Transaction[TransferParameter, Fa12TokenStorage],
    transaction_2: OperationData,
) -> None:
    print(divest_liquidity, transfer, transaction_2)
