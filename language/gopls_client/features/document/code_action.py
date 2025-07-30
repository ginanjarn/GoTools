from collections import namedtuple
from functools import wraps

from ....plugin_core.session import Session
from ....plugin_core.features.document.code_action import (
    DocumentCodeActionMixins,
    CodeActionResolveMixins,
)
from ....plugin_core.features.workspace.edit import WorkspaceEdit


LineCharacter = namedtuple("LineCharacter", ["line", "character"])


def must_initialized(func):
    """exec if initialized"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.session.is_initialized():
            return None
        return func(self, *args, **kwargs)

    return wrapper


class GoplsCodeActionResolveMixins(CodeActionResolveMixins):

    def _handle_action(self, session: Session, action: dict) -> None:
        if edit := action.get("edit"):
            WorkspaceEdit(session).apply_changes(edit)
        if command := action.get("command"):
            self.workspace_executecommand(command)


class GoplsDocumentCodeActionMixins(
    DocumentCodeActionMixins,
    GoplsCodeActionResolveMixins,
):

    def _handle_selected_action(self, session: Session, action: dict) -> None:
        if edit := action.get("edit"):
            WorkspaceEdit(session).apply_changes(edit)
        if _ := action.get("command"):
            self.code_action_resolve(action)
