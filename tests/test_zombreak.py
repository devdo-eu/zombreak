from tests.common import helper_factory, dumper_factory
from zombreak import main


def test_main():
    try:
        main(dumper_factory(), helper_factory(['1']))
    except Exception as ex:
        assert str(ex) == 'Wrong number of players!'

    try:
        main(dumper_factory(), helper_factory(['7']))
    except Exception as ex:
        assert str(ex) == 'Wrong number of players!'

    try:
        main(dumper_factory(), helper_factory(['6', '6']))
    except Exception as ex:
        assert str(ex) == 'Wrong number of initial survivors!'

    try:
        main(dumper_factory(), helper_factory(['6', '0']))
    except Exception as ex:
        assert str(ex) == 'Wrong number of initial survivors!'
