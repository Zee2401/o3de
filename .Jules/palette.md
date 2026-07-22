## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2026-07-16 - Safe XML-Only Search Filter Customization
**Learning:** For standalone tool views like the Lua IDE, search widgets of class `AzQtComponents::FilteredSearchWidget` lack default placeholders, which reduces screen reader friendliness and search discoverability. While programmatic C++ modifications can trigger extreme 330-minute CI rebuild timeouts on cold-cache branches, surgical XML property additions (e.g., `<property name="placeholderText">`) are perfectly parsed and compile cleanly.
**Action:** Prefer declaring `placeholderText` directly in the `.ui` file within the `FilteredSearchWidget` declaration to safely improve search box context without risks to build performance.

## 2026-10-24 - Headless Tkinter Component Testing
**Learning:** For Tkinter-based helper tools like the Android Project Generator, verifying UI event bindings (Escape, Alt-mnemonics, and protocols) in a headless CI/CD container requires decoupling tests from the window subsystem (X11) by mocking the entire `tkinter` module rather than trying to instantiate actual GUI elements.
**Action:** Use a complete patch/mock strategy on the `tkinter` module within standard pytest unit tests to verify widget interactions, layout properties, and bound key-sequencing without triggering display-initialization failures.
