## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.
## 2025-05-14 - [Standardizing Search Inputs in Qt UI]
**Learning:** O3DE UI uses standard Qt .ui files where QLineEdit search fields often lack modern UX features like clear buttons and placeholders. Adding these properties directly in the .ui file is a safe, metadata-only way to improve UX without triggering large C++ recompilations.
**Action:** Always check for QLineEdit widgets used as filters and add 'placeholderText', 'clearButtonEnabled', and 'accessibleName' properties. Also, link accompanying labels using the 'buddy' property for accessibility.
