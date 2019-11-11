import logging
# noinspection PyUnresolvedReferences
import os
import sys
# noinspection PyUnresolvedReferences
from pathlib import Path

# noinspection PyPackageRequirements
import IPython
# noinspection PyPackageRequirements
from IPython.core import interactiveshell
# noinspection PyPackageRequirements
from IPython.display import YouTubeVideo
# noinspection PyPackageRequirements

logging.warning("### AMC SPECIFIC SETUP STARTS ###")

def _error_only_traceback_to_stdout(*_, **__):
    excType, msg = sys.exc_info()[:2]
    sys.stderr.write(f"{excType.__name__}: {msg}")


def switch_traceback():
    if interactiveshell.InteractiveShell.showtraceback == _real_traceback:
        tb = _error_only_traceback_to_stdout
    else:
        tb = _real_traceback
    interactiveshell.InteractiveShell.showtraceback = tb
    logging.warning(f"traceback: use {tb}")


# "all", "last", "last_expr", "none", "last_expr_or_assign"
interactiveshell.InteractiveShell.ast_node_interactivity = "last_expr_or_assign"
_real_traceback = interactiveshell.InteractiveShell.showtraceback
interactiveshell.InteractiveShell.showtraceback = _error_only_traceback_to_stdout

logging.warning("### AMC SPECIFIC SETUP DONE ###")
