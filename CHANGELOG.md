# Changelog

## [2.0.1] - 2026-10-31

### Changed
- Unified icon set based on [Lucide](https://lucide.dev) (ISC license): sidebar, toolbar, format panel, download actions, page buttons, empty states and a new app logo. Old mixed PNG icons removed.
- Context menus, tooltips and spin boxes follow the light theme regardless of the Windows color mode.
- The browser context menu is translated to Spanish and no longer offers "Save page", "View page source", "Inspect", open in new window/tab or download actions.

### Fixed
- Empty-state descriptions were not centered.
- Spin box arrows in *Ajustes* were broken.
- Context menus were unreadable (dark text on dark background) when Windows uses dark mode.

## [2.0.0] - 2026-10-31

Complete rewrite. The previous version was never functional: downloads were simulated and several modules crashed on start.

### Added
- yt-dlp download engine (replaces `pytube`, which no longer works with YouTube).
- Side panel that detects the video open in the built-in browser and lists every video and audio format before queueing.
- Video in MP4, WEBM or MKV merged with the best matching audio; audio as MP3, M4A, Opus, FLAC, WAV or original.
- Download manager with a queue, configurable concurrency, pause, resume, cancel with cleanup of partial files, retry, speed limit, progress, speed and remaining time.
- Persistent download history with "open file" and "show in folder".
- Address bar that searches YouTube or opens video links, back/forward/reload/home and full-screen video.
- Hardened browser: YouTube-only HTTPS navigation, external links opened in the system browser after confirmation, HTTP/file requests blocked, every permission denied, browser downloads and pop-ups disabled, no JavaScript bridge, cookies never shared with yt-dlp, option to clear cookies and cache.
- Bundled FFmpeg and deno, Windows build script and unit tests.

### Fixed
- `YouTube` was used without being imported, so metadata and downloads always crashed.
- Video URL validation relied on fixed string offsets and failed for `youtu.be`, Shorts, mobile and playlist URLs.
- Download threads were destroyed while running and pause, resume and cancel did nothing.
- The download manager crashed reading preferences (stored strings used as integer dictionary keys).
- Videos queued after the manager window was first opened never appeared in it.
- Icons and images were loaded from paths relative to the working directory.

### Changed
- Single window with sidebar navigation instead of separate windows.
- Dependencies: PySide6 6.12.0, yt-dlp 2026.10.26, imageio-ffmpeg 0.7.0, PyInstaller 6.22.3.

### Removed
- `pytube`, the Qt Designer files and the deprecated download manager.
