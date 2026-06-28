## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2025-05-15 - Promoting QLineEdit to SearchLineEdit in UI Files
**Learning:** In O3DE, it is cleaner and more efficient to promote `QLineEdit` widgets to `AzQtComponents::SearchLineEdit` directly within `.ui` files. This automatically applies the "Search" style and functionality (like the clear button) without needing extra manual C++ styling calls or including `AzQtComponents/Components/Widgets/LineEdit.h` in source files.
**Action:** In `.ui` files, change the `widget` class to `AzQtComponents::SearchLineEdit` and add a `<customwidget>` entry with header `AzQtComponents/Components/SearchLineEdit.h` and location `global`.
