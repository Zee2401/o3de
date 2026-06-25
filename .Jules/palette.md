## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2025-05-15 - Standard Inspector Panel Input Pattern
**Learning:** Standardizing property editors in Inspector-style panels improves accessibility and user guidance. Associating the label as a buddy to the input ensures screen readers identify the field and allows users to click the label to focus the input.
**Action:** For name editors or property inputs in O3DE panels, use `label->setBuddy(input)`, `input->setPlaceholderText(tr("Enter name..."))`, `input->setClearButtonEnabled(true)`, and `input->setAccessibleName(tr("Field Name"))`.
