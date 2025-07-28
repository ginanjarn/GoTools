from collections import namedtuple
from functools import wraps
from typing import Any

from ....plugin_core.lsp_client import Response
from ....plugin_core.session import Session
from ....plugin_core.fetures.document.code_action import DocumentCodeActionMixins
from ....plugin_core.fetures.workspace.edit import WorkspaceEdit


LineCharacter = namedtuple("LineCharacter", ["line", "character"])


def must_initialized(func):
    """exec if initialized"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.session.is_initialized():
            return None
        return func(self, *args, **kwargs)

    return wrapper


class CodeActionResolveMixins:

    @must_initialized
    def code_action_resolve(self, params: Any):
        self.message_pool.send_request("codeAction/resolve", params)

    def handle_code_action_resolve(self, session: Session, params: Response):
        if err := params.error:
            print(err["message"])

        elif result := params.result:
            if command := result.get("command"):
                self.workspace_executecommand(command)
            else:
                raise Exception(f"error handle resolve: {result}")


class GoplsDocumentCodeActionMixins(DocumentCodeActionMixins, CodeActionResolveMixins):

    def _handle_selected_action(self, session: Session, action: dict) -> None:
        if edit := action.get("edit"):
            WorkspaceEdit(session).apply_changes(edit)
        elif "command" in action:
            self.code_action_resolve(action)
        else:
            raise Exception(f"error handle action: {action}")
