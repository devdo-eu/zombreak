from tests.common import helper_factory, dumper_factory
from zombreak import main
import pytest


@pytest.mark.asyncio
async def test_main_exceptions():
    try:
        await main(dumper_factory(), helper_factory(['1']))
    except Exception as ex:
        assert str(ex) == 'Wrong number of players!'

    try:
        await main(dumper_factory(), helper_factory(['7']))
    except Exception as ex:
        assert str(ex) == 'Wrong number of players!'

    try:
        await main(dumper_factory(), helper_factory(['6', '6']))
    except Exception as ex:
        assert str(ex) == 'Wrong number of initial survivors!'

    try:
        await main(dumper_factory(), helper_factory(['6', '0']))
    except Exception as ex:
        assert str(ex) == 'Wrong number of initial survivors!'


@pytest.mark.asyncio
async def test_main():
    await main(dumper_factory(), helper_factory(['2', '1', 'CPU_A', 'CPU_B']))
    await main(dumper_factory(), helper_factory(['3', '1', 'CPU_A', 'CPU_B', 'CPU_C']))
    await main(dumper_factory(), helper_factory(['4', '1', 'CPU_A', 'CPU_B', 'CPU_C', 'CPU_D']))
