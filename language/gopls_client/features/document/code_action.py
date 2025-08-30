from ....plugin_core.session import Session
from ....plugin_core.features.document.code_action import (
    DocumentCodeActionMixins,
    CodeActionResolveMixins,
)
from ....plugin_core.features.workspace.edit import WorkspaceEdit


class GoplsDocumentCodeActionMixins(
    DocumentCodeActionMixins,
    CodeActionResolveMixins,
):
    """"""

    def _handle_selected_action(self, session: Session, action: dict) -> None:
        if edit := action.get("edit"):
            WorkspaceEdit(session).apply_changes(edit)
        if _ := action.get("command"):
            self.codeaction_resolve(action)
