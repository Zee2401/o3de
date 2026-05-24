## 2025-05-14 - Standard Search/Filter Input Pattern in O3DE
**Learning:** O3DE (Open 3D Engine) uses a consistent UX pattern for search and filter fields in the Editor to improve usability and visual consistency. This involves setting localized placeholder text, enabling the built-in clear button, and applying the "Search" style class through the AzQtComponents framework.
**Action:** When implementing or enhancing search/filter inputs, ensure <AzQtComponents/Components/Widgets/LineEdit.h> is included, then call setPlaceholderText(), setClearButtonEnabled(true), and AzQtComponents::LineEdit::applySearchStyle().

## 2025-05-15 - Avoiding Build Timeouts in Large O3DE Gems
**Learning:** In large O3DE Gems (like LyShine or AudioSystem), promoting widgets to specialized classes (e.g., AzQtComponents::SearchLineEdit) in .ui files can trigger full rebuilds and CI timeouts (330+ minutes) if it invalidates build caches (indicated by 100% 'Preprocessing failed' ccache stats).
**Action:** For surgical UX wins in large Gems, apply standard properties (placeholderText, clearButtonEnabled, accessibleName) directly to existing QLineEdit widgets in .ui files instead of promoting to specialized classes.
