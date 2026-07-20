## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2026-07-16 - Safe XML-Only Search Filter Customization
**Learning:** For standalone tool views like the Lua IDE, search widgets of class `AzQtComponents::FilteredSearchWidget` lack default placeholders, which reduces screen reader friendliness and search discoverability. While programmatic C++ modifications can trigger extreme 330-minute CI rebuild timeouts on cold-cache branches, surgical XML property additions (e.g., `<property name="placeholderText">`) are perfectly parsed and compile cleanly.
**Action:** Prefer declaring `placeholderText` directly in the `.ui` file within the `FilteredSearchWidget` declaration to safely improve search box context without risks to build performance.

## 2026-07-20 - Tkinter Modal Accessibility and Headless Testing
**Learning:** When developing Python Tkinter desktop applications like the Android Project Generator, adding `<Escape>` key bindings to modal dialogs like `WaitDialog` provides critical accessibility dismissal behavior. Testing these GUI components in headless CI requires mock patching (like mocking `tkinter.Toplevel`) to avoid Tcl/Tk graphic device errors while still validating that the key bindings successfully invoke the cancel callback.
**Action:** Use `.bind("<Escape>", ...)` to dismissed modal dialogs, and test with python unittest/pytest by mocking the tkinter frame classes and verifying that bound callable triggers the callback.
