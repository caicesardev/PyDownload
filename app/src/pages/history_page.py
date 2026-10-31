from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QMessageBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.models.history_entry import HistoryEntry
from src.services.history_store import HistoryStore
from src.utils.file_browser import open_file, reveal_in_file_manager
from src.widgets.buttons import icon_button
from src.widgets.empty_state import EmptyState
from src.widgets.icons import themed_icon
from src.widgets.labels import page_title
from src.widgets.theme import DANGER

COLUMNS = ("Título", "Formato", "Fecha")
DATE_FORMAT = "%d/%m/%Y %H:%M"


class HistoryPage(QWidget):
    def __init__(self, store: HistoryStore, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Page")
        self._store = store

        self._table = self._build_table()
        self._stack = QStackedWidget(self)
        self._stack.addWidget(EmptyState(
            "history",
            "El historial está vacío",
            "Las descargas completadas aparecerán aquí para que puedas abrirlas cuando quieras.",
            self,
        ))
        self._stack.addWidget(self._table)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)
        layout.addLayout(self._build_header())
        layout.addWidget(self._stack, stretch=1)
        self.refresh()

    def add_entry(self, entry: HistoryEntry) -> None:
        self._store.add(entry)
        self.refresh()

    def refresh(self) -> None:
        entries = self._store.entries
        self._table.setRowCount(len(entries))
        for row, entry in enumerate(entries):
            self._fill_row(row, entry)
        self._stack.setCurrentIndex(1 if entries else 0)
        self._update_buttons()

    def _build_header(self) -> QHBoxLayout:
        self._open_file_button = icon_button(themed_icon("external-link"), "Abrir archivo", self)
        self._open_file_button.clicked.connect(self._open_selected_file)
        self._reveal_button = icon_button(themed_icon("folder-open"), "Mostrar en la carpeta", self)
        self._reveal_button.clicked.connect(self._reveal_selected_file)
        self._remove_button = icon_button(themed_icon("x"), "Quitar del historial", self)
        self._remove_button.clicked.connect(self._remove_selected_entry)
        self._clear_button = icon_button(themed_icon("trash-2", DANGER), "Limpiar historial", self)
        self._clear_button.setProperty("variant", "danger")
        self._clear_button.clicked.connect(self._confirm_clear)

        header = QHBoxLayout()
        header.addWidget(page_title("Historial", self))
        header.addStretch()
        for button in (self._open_file_button, self._reveal_button, self._remove_button, self._clear_button):
            header.addWidget(button)
        return header

    def _build_table(self) -> QTableWidget:
        table = QTableWidget(0, len(COLUMNS), self)
        table.setHorizontalHeaderLabels(COLUMNS)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setShowGrid(False)
        table.setAlternatingRowColors(False)
        table.verticalHeader().hide()
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        table.itemSelectionChanged.connect(self._update_buttons)
        table.cellDoubleClicked.connect(lambda _row, _column: self._open_selected_file())
        return table

    def _fill_row(self, row: int, entry: HistoryEntry) -> None:
        title = QTableWidgetItem(entry.title)
        title.setData(Qt.ItemDataRole.UserRole, entry)
        title.setToolTip(entry.filepath)
        self._table.setItem(row, 0, title)
        self._table.setItem(row, 1, QTableWidgetItem(entry.summary))
        self._table.setItem(row, 2, QTableWidgetItem(self._format_date(entry.completed_at)))

    @staticmethod
    def _format_date(iso_date: str) -> str:
        try:
            return datetime.fromisoformat(iso_date).strftime(DATE_FORMAT)
        except ValueError:
            return iso_date

    def _selected_entry(self) -> HistoryEntry | None:
        rows = self._table.selectionModel().selectedRows()
        if not rows:
            return None
        entry = self._table.item(rows[0].row(), 0).data(Qt.ItemDataRole.UserRole)
        return entry if isinstance(entry, HistoryEntry) else None

    def _update_buttons(self) -> None:
        has_selection = self._selected_entry() is not None
        for button in (self._open_file_button, self._reveal_button, self._remove_button):
            button.setEnabled(has_selection)
        self._clear_button.setEnabled(bool(self._store.entries))

    def _open_selected_file(self) -> None:
        entry = self._selected_entry()
        if entry is not None and not open_file(entry.filepath):
            self._warn_missing_file()

    def _reveal_selected_file(self) -> None:
        entry = self._selected_entry()
        if entry is not None and not reveal_in_file_manager(entry.filepath):
            self._warn_missing_file()

    def _remove_selected_entry(self) -> None:
        if entry := self._selected_entry():
            self._store.remove(entry)
            self.refresh()

    def _confirm_clear(self) -> None:
        answer = QMessageBox.question(
            self,
            "Limpiar historial",
            "¿Borrar todo el historial? Los archivos descargados no se eliminarán.",
        )
        if answer == QMessageBox.StandardButton.Yes:
            self._store.clear()
            self.refresh()

    def _warn_missing_file(self) -> None:
        QMessageBox.warning(self, "Archivo no encontrado", "El archivo se ha movido o eliminado.")
