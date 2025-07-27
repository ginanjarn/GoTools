"""client"""

import time
import logging

from pathlib import Path
from typing import Optional
import sublime

from ..constant import (
    COMMAND_PREFIX,
    LOGGING_CHANNEL,
    PACKAGE_NAME,
)
from ..plugin_core.lsp_client import StandardIO
from ..plugin_core.client import BaseClient, ServerArguments
from ..plugin_core.sublime_settings import Settings

LOGGER = logging.getLogger(LOGGING_CHANNEL)


from ..plugin_core.fetures.initializer import InitializerMixins
from ..plugin_core.fetures.document.synchronizer import DocumentSynchronizerMixins

from ..plugin_core.fetures.document.completion import DocumentCompletionMixins
from ..plugin_core.fetures.document.definition import DocumentDefinitionMixins
from ..plugin_core.fetures.document.diagnostics import DocumentDiagnosticsMixins
from ..plugin_core.fetures.document.formatting import DocumentFormattingMixins
from ..plugin_core.fetures.document.hover import DocumentHoverMixins
from ..plugin_core.fetures.document.rename import DocumentRenameMixins
from ..plugin_core.fetures.document.signature_help import DocumentSignatureHelpMixins

from ..plugin_core.fetures.workspace.command import WorkspaceExecuteCommandMixins
from ..plugin_core.fetures.workspace.edit import WorkspaceApplyEditMixins

from ..plugin_core.fetures.window.message import WindowMessageMixins


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
    WorkspaceExecuteCommandMixins,
    WorkspaceApplyEditMixins,
    WindowMessageMixins,
):
    def _set_default_handler(self):
        default_handlers = {
            "initialize": self.handle_initialize,
            # window
            "window/logMessage": self.handle_window_logmessage,
            "window/showMessage": self.handle_window_showmessage,
            # workspace
            "workspace/applyEdit": self.handle_workspace_applyedit,
            "workspace/executeCommand": self.handle_workspace_executecommand,
            # textDocument
            "textDocument/hover": self.handle_textdocument_hover,
            "textDocument/completion": self.handle_textdocument_completion,
            "textDocument/signatureHelp": self.handle_textdocument_signaturehelp,
            "textDocument/publishDiagnostics": self.handle_textdocument_publishdiagnostics,
            "textDocument/formatting": self.handle_textdocument_formatting,
            "textDocument/definition": self.handle_textdocument_definition,
            "textDocument/prepareRename": self.handle_textdocument_preparerename,
            "textDocument/rename": self.handle_textdocument_rename,
        }
        self.handler_map.update(default_handlers)


def get_client() -> GoplsClient:
    """"""
    command = ["gopls"]
    return GoplsClient(ServerArguments(command, None), StandardIO)


def get_envs_settings() -> Optional[dict]:
    """get environments defined in '*.sublime-settings'"""

    with Settings() as settings:
        if envs := settings.get("envs"):
            return envs
