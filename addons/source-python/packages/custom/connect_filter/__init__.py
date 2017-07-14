# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module

# Source.Python
from core import AutoUnload, GAME_NAME
from translations.strings import TranslationStrings

# Connect Filter
from .paths import GAME_SPECIFIC_MODULES_PATH


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_connection_rejection_text(client):
    for connect_filter in _connect_filters:
        result = connect_filter(client)
        if result is None:
            continue

        if isinstance(result, TranslationStrings):
            result = result.get_string()

        return result

    # Return None, meaning that there's no reason to reject the SteamID
    return None


# =============================================================================
# >> CLASSES
# =============================================================================
class ConnectFilter(AutoUnload):
    def __init__(self, callback):
        self._callback = callback

        _connect_filters.append(self)

    def __call__(self, *args, **kwargs):
        return self._callback(*args, **kwargs)

    def _unload_instance(self):
        _connect_filters.remove(self)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_connect_filters = []


# =============================================================================
# >> GAME-SPECIFIC IMPORTS
# =============================================================================
if not (GAME_SPECIFIC_MODULES_PATH / (GAME_NAME + ".py")).isfile():
    raise RuntimeError(
        f"Couldn't locate game-specific module for game '{GAME_NAME}'")

import_module('.'.join(('connect_filter', 'games', GAME_NAME)))
