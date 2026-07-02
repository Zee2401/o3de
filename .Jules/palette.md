## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2025-05-15 - Accessibility for Search and Filter Inputs
**Learning:** Visual search styling is insufficient for accessibility. Screen readers require explicit accessible names, and keyboard users benefit from buddy relationships between labels and inputs.
**Action:** Always call `setAccessibleName(tr("Search"))` (or "Filter") on search inputs and use `label->setBuddy(lineEdit)` to associate external labels with their corresponding input fields.
