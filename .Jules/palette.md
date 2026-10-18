## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2026-07-16 - Safe XML-Only Search Filter Customization
**Learning:** For standalone tool views like the Lua IDE, search widgets of class `AzQtComponents::FilteredSearchWidget` lack default placeholders, which reduces screen reader friendliness and search discoverability. While programmatic C++ modifications can trigger extreme 330-minute CI rebuild timeouts on cold-cache branches, surgical XML property additions (e.g., `<property name="placeholderText">`) are perfectly parsed and compile cleanly.
**Action:** Prefer declaring `placeholderText` directly in the `.ui` file within the `FilteredSearchWidget` declaration to safely improve search box context without risks to build performance.

## 2026-07-17 - Robust Keyboard Dismissal and Cancelation for Modal Dialogs in Tkinter
**Learning:** For desktop utilities built with Tkinter, relying entirely on on-screen cancel buttons can result in orphaned background processes if a user closes the modal dialog via window manager decorations (clicking 'X' or pressing Alt+F4). Mapping keyboard escape/accelerator bindings and utilizing the `WM_DELETE_WINDOW` window protocol to trigger the official cancel callback guarantees graceful termination.
**Action:** Always bind `<Escape>` and accelerator shortcuts (e.g., `<Alt-c>`) to the cancel handler in modal dialogs, and explicitly map the `WM_DELETE_WINDOW` protocol to prevent orphaned threads/processes.

## 2026-07-18 - Read-Only Log Display with Programmatic Updates in Tkinter
**Learning:** Standard text widgets in Tkinter that display log outputs are editable by default, which can lead to accidental deletion or text modification by the user. Making the widget read-only (`state=tk.DISABLED`) prevents edits, but also blocks programmatic insertion. Dynamically toggling the widget's state to `tk.NORMAL` before inserting/clearing and reverting it back to `tk.DISABLED` immediately after allows safe updates.
**Action:** Configure the log display text widget as `state=tk.DISABLED` during initialization, and wrap programmatic insertions and deletions within temporary `self._report_text_widget.configure(state=tk.NORMAL)` and `self._report_text_widget.configure(state=tk.DISABLED)` blocks.
