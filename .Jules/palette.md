## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2025-05-15 - Surgical PRs for UX Improvements
**Learning:** Large repositories like O3DE have strict constraints on PR size (e.g., 50 lines) and are sensitive to build cache invalidation. Automated reformatting of large files can easily exceed these limits and trigger CI timeouts.
**Action:** Use surgical edits to apply only the necessary UX and accessibility changes. Avoid whole-file formatting and use `git diff --cached` to verify the line count of the actual changes.
