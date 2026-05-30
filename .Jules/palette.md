## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2025-05-30 - Surgical UI-only Improvements in Large O3DE Targets
**Learning:** In large O3DE targets like `EditorLib`, even minor C++ changes (like adding an include or a single function call) can trigger massive rebuilds and lead to CI timeouts or runner communication loss.
**Action:** Prefer "surgical" UI-only improvements by setting standard properties (placeholderText, clearButtonEnabled, accessibleName, buddy) directly in the `.ui` file when working with core Editor components. This improves UX and accessibility without affecting the build graph.
