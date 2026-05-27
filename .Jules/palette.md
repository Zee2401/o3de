## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2025-05-22 - Surgical UI Property Additions for Large O3DE Gems
**Learning:** In large O3DE Gems (like ScriptCanvas or LyShine), promoting widgets to `AzQtComponents` classes or adding C++ includes can trigger 330-minute CI timeouts due to cache invalidation. Standard `QLineEdit` properties like `clearButtonEnabled` and `accessibleName` can be set directly in the `.ui` file to achieve similar UX benefits without triggering a full rebuild.
**Action:** Prefer metadata-only additions to `.ui` files for search styling and accessibility in large Gems to maintain build performance while improving UX.
