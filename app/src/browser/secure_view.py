from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView

from src.widgets.icons import themed_icon

WebAction = QWebEnginePage.WebAction

HIDDEN_ACTIONS = (
    WebAction.SavePage,
    WebAction.ViewSource,
    WebAction.InspectElement,
    WebAction.OpenLinkInNewWindow,
    WebAction.OpenLinkInNewTab,
    WebAction.OpenLinkInNewBackgroundTab,
    WebAction.DownloadLinkToDisk,
    WebAction.DownloadImageToDisk,
    WebAction.DownloadMediaToDisk,
)
SPANISH_MENU_LABELS = {
    "Back": "Atrás",
    "Forward": "Adelante",
    "Reload": "Recargar",
    "Cut": "Cortar",
    "Copy": "Copiar",
    "Paste": "Pegar",
    "Undo": "Deshacer",
    "Redo": "Rehacer",
    "Select all": "Seleccionar todo",
    "Paste and match style": "Pegar con el mismo estilo",
    "Copy link address": "Copiar dirección del enlace",
    "Copy image": "Copiar imagen",
    "Copy image address": "Copiar dirección de la imagen",
    "Copy media address": "Copiar dirección del contenido multimedia",
    "Show controls": "Mostrar controles",
    "Loop": "Repetir",
    "Exit full screen": "Salir de pantalla completa",
}
ACTION_ICONS = {
    WebAction.Back: "arrow-left",
    WebAction.Forward: "arrow-right",
    WebAction.Reload: "rotate-cw",
}


class SecureWebView(QWebEngineView):
    def setPage(self, page: QWebEnginePage | None) -> None:
        super().setPage(page)
        if page is None:
            return
        for web_action, icon_name in ACTION_ICONS.items():
            page.action(web_action).setIcon(themed_icon(icon_name))

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = self.createStandardContextMenu()
        hidden = {self.pageAction(action) for action in HIDDEN_ACTIONS}
        for action in menu.actions():
            if action in hidden:
                menu.removeAction(action)
            else:
                action.setText(SPANISH_MENU_LABELS.get(action.text(), action.text()))
        menu.exec(event.globalPos())
        menu.deleteLater()
