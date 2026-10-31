from pathlib import Path

from PySide6.QtCore import QObject
from PySide6.QtWebEngineCore import (
    QWebEngineDownloadRequest,
    QWebEngineProfile,
    QWebEngineSettings,
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)

PROFILE_NAME = "PyDownload"
BLOCKED_REQUEST_SCHEMES = frozenset({"http", "file", "ftp"})

DISABLED_ATTRIBUTES = (
    QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows,
    QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard,
    QWebEngineSettings.WebAttribute.JavascriptCanPaste,
    QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls,
    QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls,
    QWebEngineSettings.WebAttribute.AllowRunningInsecureContent,
    QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins,
    QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript,
    QWebEngineSettings.WebAttribute.PluginsEnabled,
    QWebEngineSettings.WebAttribute.PdfViewerEnabled,
    QWebEngineSettings.WebAttribute.ScreenCaptureEnabled,
    QWebEngineSettings.WebAttribute.HyperlinkAuditingEnabled,
    QWebEngineSettings.WebAttribute.DnsPrefetchEnabled,
    QWebEngineSettings.WebAttribute.NavigateOnDropEnabled,
)
ENABLED_ATTRIBUTES = (
    QWebEngineSettings.WebAttribute.JavascriptEnabled,
    QWebEngineSettings.WebAttribute.WebRTCPublicInterfacesOnly,
    QWebEngineSettings.WebAttribute.FullScreenSupportEnabled,
)


class InsecureRequestBlocker(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:
        if info.requestUrl().scheme().lower() in BLOCKED_REQUEST_SCHEMES:
            info.block(True)


class SecureProfile(QWebEngineProfile):
    def __init__(self, storage_directory: Path, parent: QObject | None = None) -> None:
        super().__init__(PROFILE_NAME, parent)
        self.setPersistentStoragePath(str(storage_directory / "storage"))
        self.setCachePath(str(storage_directory / "cache"))
        self.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        self.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        self.setPersistentPermissionsPolicy(QWebEngineProfile.PersistentPermissionsPolicy.AskEveryTime)
        self.setPushServiceEnabled(False)
        self.setSpellCheckEnabled(False)
        self._request_blocker = InsecureRequestBlocker(self)
        self.setUrlRequestInterceptor(self._request_blocker)
        self.downloadRequested.connect(self._reject_browser_download)
        self._harden_settings()

    def clear_browsing_data(self) -> None:
        self.clearHttpCache()
        self.clearAllVisitedLinks()
        self.cookieStore().deleteAllCookies()

    def _harden_settings(self) -> None:
        settings = self.settings()
        for attribute in DISABLED_ATTRIBUTES:
            settings.setAttribute(attribute, False)
        for attribute in ENABLED_ATTRIBUTES:
            settings.setAttribute(attribute, True)

    @staticmethod
    def _reject_browser_download(download: QWebEngineDownloadRequest) -> None:
        download.cancel()
