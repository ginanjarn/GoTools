"""client"""

import logging
import shlex

from typing import Optional

from ..constant import LOGGING_CHANNEL
from ..plugin_core.transport import StandardIO
from ..plugin_core.client import BaseClient, ServerArguments
from ..plugin_core.sublime_settings import Settings

LOGGER = logging.getLogger(LOGGING_CHANNEL)


from ..plugin_core.features.initializer import InitializerMixins
from ..plugin_core.features.document.synchronizer import DocumentSynchronizerMixins

from ..plugin_core.features.document.completion import DocumentCompletionMixins
from ..plugin_core.features.document.definition import DocumentDefinitionMixins
from ..plugin_core.features.document.diagnostics import DocumentDiagnosticsMixins
from ..plugin_core.features.document.formatting import DocumentFormattingMixins
from ..plugin_core.features.document.hover import DocumentHoverMixins
from ..plugin_core.features.document.rename import DocumentRenameMixins
from ..plugin_core.features.document.signature_help import DocumentSignatureHelpMixins

from ..plugin_core.features.workspace.command import WorkspaceExecuteCommandMixins
from ..plugin_core.features.workspace.edit import WorkspaceApplyEditMixins

from ..plugin_core.features.window.message import WindowMessageMixins

from .features.document.code_action import GoplsDocumentCodeActionMixins


class GoplsClient(
    BaseClient,
    InitializerMixins,
    DocumentSynchronizerMixins,
    DocumentCompletionMixins,
    DocumentDefinitionMixins,
    DocumentDiagnosticsMixins,
    DocumentFormattingMixins,
    DocumentHoverMixins,
    DocumentRenameMixins,
    DocumentSignatureHelpMixins,
    GoplsDocumentCodeActionMixins,
    WorkspaceExecuteCommandMixins,
    WorkspaceApplyEditMixins,
    WindowMessageMixins,
):
    """Gopls Client"""


def log_flags() -> str:
    """return logging flag"""
    if LOGGER.level == logging.DEBUG:
        return "-rpc.trace"
    return ""


def get_client() -> GoplsClient:
    """"""
    command = shlex.split(f"gopls {log_flags()}")
    return GoplsClient(ServerArguments(command, None), StandardIO)


def get_envs_settings() -> Optional[dict]:
    """get environments defined in '*.sublime-settings'"""

    with Settings() as settings:
        if envs := settings.get("envs"):
            return envs
