## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2025-05-15 - Surgical UI Promotion for Search Fields
**Learning:** Promoting `QLineEdit` to `AzQtComponents::SearchLineEdit` directly within `.ui` files is a surgical way to implement standard O3DE search styling (clear button, magnifying glass) without modifying C++ translation units. This is particularly valuable in large Gems to avoid triggering massive rebuilds and potential CI timeouts.
**Action:** In `.ui` files, change the widget class to `AzQtComponents::SearchLineEdit`, add properties for `placeholderText`, `clearButtonEnabled`, and `accessibleName`, and ensure `AzQtComponents/Components/SearchLineEdit.h` is added to the `<customwidgets>` section with `location="global"`.
