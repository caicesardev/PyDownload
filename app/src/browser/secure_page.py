from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtWebEngineCore import (
    QWebEngineCertificateError,
    QWebEngineFileSystemAccessRequest,
    QWebEngineNewWindowRequest,
    QWebEnginePage,
    QWebEnginePermission,
    QWebEngineProfile,
    QWebEngineRegisterProtocolHandlerRequest,
)

from src.browser.navigation_policy import (
    NavigationDecision,
    decide_embedded_frame_navigation,
    decide_main_frame_navigation,
)


class SecurePage(QWebEnginePage):
    external_link_requested = Signal(QUrl)
    navigation_blocked = Signal(QUrl)

    def __init__(self, profile: QWebEngineProfile, parent: QObject | None = None) -> None:
        super().__init__(profile, parent)
        self.permissionRequested.connect(self._deny_permission)
        self.fileSystemAccessRequested.connect(self._reject_file_system_access)
        self.registerProtocolHandlerRequested.connect(self._reject_protocol_handler)
        self.certificateError.connect(self._reject_certificate)
        self.newWindowRequested.connect(self._handle_new_window)

    def acceptNavigationRequest(self, url: QUrl, navigation_type: QWebEnginePage.NavigationType, is_main_frame: bool) -> bool:
        if not is_main_frame:
            return decide_embedded_frame_navigation(url.toString()) is NavigationDecision.ALLOW
        user_initiated = navigation_type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked
        return self._apply_decision(url, decide_main_frame_navigation(url.toString(), user_initiated))

    def javaScriptConsoleMessage(self, level: QWebEnginePage.JavaScriptConsoleMessageLevel, message: str, line: int, source: str) -> None:
        pass

    def _handle_new_window(self, request: QWebEngineNewWindowRequest) -> None:
        url = request.requestedUrl()
        decision = decide_main_frame_navigation(url.toString(), request.isUserInitiated())
        if self._apply_decision(url, decision):
            self.setUrl(url)

    def _apply_decision(self, url: QUrl, decision: NavigationDecision) -> bool:
        if decision is NavigationDecision.OPEN_EXTERNALLY:
            self.external_link_requested.emit(url)
        elif decision is NavigationDecision.BLOCK:
            self.navigation_blocked.emit(url)
        return decision is NavigationDecision.ALLOW

    @staticmethod
    def _deny_permission(permission: QWebEnginePermission) -> None:
        permission.deny()

    @staticmethod
    def _reject_file_system_access(request: QWebEngineFileSystemAccessRequest) -> None:
        request.reject()

    @staticmethod
    def _reject_protocol_handler(request: QWebEngineRegisterProtocolHandlerRequest) -> None:
        request.reject()

    @staticmethod
    def _reject_certificate(error: QWebEngineCertificateError) -> None:
        error.rejectCertificate()
