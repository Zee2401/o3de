## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2025-05-15 - Accessibility for Icon-Only Buttons and Form Inputs
**Learning:** O3DE UI components often use icon-only QToolButtons or QPushButtons that lack descriptive text. Accessibility for these components is improved by explicitly setting both a tooltip (for visual feedback) and an accessible name (for screen readers). Additionally, programmatic association of labels with their target inputs using `setBuddy()` ensures correct focus and announcement.
**Action:** For every icon-only button, call `setToolTip()` and `setAccessibleName()` with localized strings. For every label/input pair, call `label->setBuddy(input)` during UI initialization.
