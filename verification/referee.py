from checkio import api
from checkio.signals import ON_CONNECT
from checkio.referees.io import CheckiOReferee

from tests import TESTS


right_keys = {'ListComp', 'SetComp', 'DictComp', 'GeneratorExp'}


def checker(answer, counts):
    try:
        assert isinstance(counts, dict), f'Return a dict, not {type(counts)}.'
        wrong_keys = list(counts.keys() - right_keys)
        assert not wrong_keys, f'Wrong dict keys: {wrong_keys}.'
        # Check for equality but ignore authorized keys with a count of zero.
        counts = {k: v for k, v in counts.items() if v != 0}
        assert counts == answer, 'Wrong counts.'
    except AssertionError as err:
        return False, err.args[0]
    return True, 'OK'


api.add_listener(
    ON_CONNECT,
    CheckiOReferee(
        tests=TESTS,
        function_name={'python': 'count_comprehensions'},
        checker=checker,
    ).on_ready,
)
