# Changelog

All notable changes to this project will be documented in this file.

## [0.3.5] - 2025-12-02

### Added
- **Default Window Icon**: The NEUI logo is now set as the default window icon for all applications.
- **Assets**: Included `neui.png` in the package distribution.

### Fixed
- **Toggle Component**: Fixed `AttributeError: 'Toggle' object has no attribute 'value'` crash. Added `value` property alias for `checked`.

## [0.3.0] - 2025-12-02

### Added
- **Dropdown Widget**: New `neui.cui.Dropdown` component with overlay menu support.
- **Text Wrapping**: Added `wrap` style property to `Text` component. Supports `'word'` and `'char'` wrapping modes.
- **Interactive Scrollbar**: `ScrollView` now has a draggable scrollbar with hover effects.
- **Overflow Control**: Added `overflow_x` and `overflow_y` style properties to `ScrollView`. Horizontal scrolling is now locked (`hidden`) by default.
- **App Singletons**: `App` class now supports singleton access via `App.get_instance()`, enabling global overlay management.

### Changed
- Updated `DOCUMENTATION.md` with comprehensive details on new features.
- Updated `README.md` feature lists.

## [0.2.2] - 2025-12-02

### Fixed
- Removed emojis from PyPI description for better rendering.
- Fixed `DOCUMENTATION.md` link in PyPI metadata.

## [0.2.1] - 2025-12-02

### Changed
- **Branding**: Standardized project name to "NEUI" (removed "Neo UI").
- **Documentation**: Updated PyPI project URLs to point to the correct documentation file.
- **Cleanup**: Removed "Show Your Support" section and emojis from README headers.

## [0.2.0] - 2025-12-02

### Added
- **Form Example**: Comprehensive registration form demo (`examples/form_example.py`) showcasing inputs, checkboxes, radios, and layout.
- **Documentation**: Created `DOCUMENTATION.md` with full API reference and usage guides.
- **PyPI Metadata**: Enhanced `pyproject.toml` with proper classifiers, keywords, and author info.

### Changed
- **README**: Completely rewritten to focus on features, installation, and modern examples.
- **Architecture**: Refined component hierarchy and export structure.

## [0.1.1] - 2025-12-01

### Added
- **Interactive Components**: Added `Button`, `Input` (text/password), `Checkbox`, `Radio`, `Toggle`, `Slider`.
- **Event System**: Implemented `EventManager` for handling mouse (click, hover, drag) and keyboard events.
- **Layout Engine**: Added `compute_layout` supporting Flexbox-like `row`/`col` layouts, alignment, and justification.

## [0.1.0] - 2025-11-30

### Added
- **Core Engine**: Initial release of the NEUI core.
- **Renderer**: GPU-accelerated rendering using `skia-python` and `glfw`.
- **Base Classes**: `App`, `Element`, and `Box` classes.
- **Basic Styling**: Support for background colors, borders, and rounded corners.
