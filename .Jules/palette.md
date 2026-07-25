## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2026-07-16 - Safe XML-Only Search Filter Customization
**Learning:** For standalone tool views like the Lua IDE, search widgets of class `AzQtComponents::FilteredSearchWidget` lack default placeholders, which reduces screen reader friendliness and search discoverability. While programmatic C++ modifications can trigger extreme 330-minute CI rebuild timeouts on cold-cache branches, surgical XML property additions (e.g., `<property name="placeholderText">`) are perfectly parsed and compile cleanly.
**Action:** Prefer declaring `placeholderText` directly in the `.ui` file within the `FilteredSearchWidget` declaration to safely improve search box context without risks to build performance.

## 2026-07-24 - Headless Mocking and Scope Restrictions of Tkinter Keyboard Mnemonics
**Learning:** Keyboard-bound accelerators in Python Tkinter should use window-scoped bindings (`self.bind`) rather than application-wide shortcuts (`self.bind_all`) to prevent event collisions between active dialogs. Testing Tkinter components under headless Linux CI environments requires robust mock subclass definitions to satisfy Tk's internal child-lookup mechanics without invoking `__init__` on headless display drivers.
**Action:** Implement button-specific `underline` property and window-level bindings with case fallback (e.g., `<Alt-c>` and `<Alt-C>`). In unit tests, use patch context managers or custom dummy classes with standard Tk structure (like `DummyTk` with attributes like `_last_child_ids`) to safely isolate and test UI interactions.
