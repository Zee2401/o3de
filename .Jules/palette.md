## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2025-05-15 - Surgical Search Improvements via UI Promotion
**Learning:** In large O3DE Gems, promoting `QLineEdit` to `AzQtComponents::SearchLineEdit` directly within `.ui` files is preferred over C++ modifications. This applies standard search styling (magnifying glass, clear button) and accessibility properties without triggering expensive C++ recompilation or potential CI timeouts.
**Action:** Promote search widgets in `.ui` files, add `placeholderText`, `clearButtonEnabled`, and `accessibleName` properties, and register the custom widget with header `AzQtComponents/Components/SearchLineEdit.h` (location: global).
