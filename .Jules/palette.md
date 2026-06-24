## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2025-05-15 - EditorLib CI Stability with UX Improvements
**Learning:** Modifying large targets like `EditorLib` (e.g., `LevelFileDialog`) with `AzQtComponents` headers can trigger 330-minute CI timeouts on new branches due to ccache misses and large build graph churn. Standard `QLineEdit` methods (setPlaceholderText, setClearButtonEnabled) are safe and do not require extra headers that destabilize CI.
**Action:** For surgical UX improvements in `EditorLib`, prefer programmatic C++ changes using standard Qt methods over `AzQtComponents` styling or `.ui` file modifications to maintain CI stability.
