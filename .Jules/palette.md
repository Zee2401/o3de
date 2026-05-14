## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2025-05-15 - Promoting Search Inputs via .ui Files in O3DE
**Learning:** Promoting a standard `QLineEdit` to `AzQtComponents::SearchLineEdit` directly within a `.ui` file is a cleaner and more surgical way to implement the O3DE search styling compared to manual C++ calls. It automatically handles the magnifying glass icon, clear button, and placeholder styling while remaining compatible with existing C++ code that treats the widget as a `QLineEdit`.
**Action:** In `.ui` files, promote search `QLineEdit` widgets to `AzQtComponents::SearchLineEdit`, set the `header` to `AzQtComponents/Components/SearchLineEdit.h` (location="global"), and ensure `placeholderText` and `accessibleName` are defined.
