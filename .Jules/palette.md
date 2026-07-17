## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure `<AzQtComponents/Components/Widgets/LineEdit.h>` is included, then call `setPlaceholderText()`, `setClearButtonEnabled(true)`, and `AzQtComponents::LineEdit::applySearchStyle()`.

## 2026-07-16 - Accessibility Mnemonics and Buddy Relationships in .ui Files
**Learning:** Adding keyboard mnemonics (using `&`) to labels and establishing `buddy` relationships in Qt `.ui` files provides immediate keyboard accessibility (e.g., Alt+Key) to focus corresponding input widgets, improving the experience for power users and those using assistive technologies.
**Action:** Always check if a `QLabel` has a corresponding input widget and set the `buddy` property and a mnemonic in the `text` property (e.g., `&Name:`).

## 2026-07-17 - Tkinter Keyboard Mnemonics and Index Alignment in Python Tools
**Learning:** Tkinter labels and buttons can be configured with keyboard mnemonics using the `underline` property (which indicates the index of the character to underline). Unlike other frameworks, standard Tkinter/ttk labels do not automatically strip or process raw underscores or ampersands, so the underline index must align directly with the character index of the raw text (e.g. underline `4` for 's' in "Namespace" for Alt-S).
**Action:** Configure the `underline` attribute to point to the exact character index, bind both lower and uppercase Alt keys (e.g., `<Alt-s>` and `<Alt-S>`), and ensure no visual mismatch between the underlined letter and the actual bound shortcut.
