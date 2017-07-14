# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from core import GAME_NAME
from engines.server import server
from memory import get_object_pointer, make_object
from memory.hooks import PostHook
from memory.manager import TypeManager
from players import Client

# Connect Filter
from .. import get_connection_rejection_text
from ..paths import CF_DATA_PATH


# =============================================================================
# >> CONSTANTS
# =============================================================================
MAX_REJECTION_TEXT_LENGTH = 64


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
manager = TypeManager()
server_ptr = get_object_pointer(server)

CustomServer = manager.create_type_from_file(
    'CBaseServer', CF_DATA_PATH / 'memory' / GAME_NAME / 'CBaseServer.ini')

custom_server = make_object(CustomServer, server_ptr)


# =============================================================================
# >> HOOKS
# =============================================================================
@PostHook(custom_server.check_challenge_type)
def post_check_challenge_type(args, ret_val):
    client = make_object(Client, args[1] + 4)

    rejection_text = get_connection_rejection_text(client)
    if rejection_text is None:
        return

    custom_server.reject_connection(
        args[3], args[7], rejection_text[:MAX_REJECTION_TEXT_LENGTH])

    return False
