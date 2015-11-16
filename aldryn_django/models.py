#######################
# apply monkeypatches #
#######################
from .monkeypatches import hide_secrets_in_debug_mode
hide_secrets_in_debug_mode.patch()
