# textual-plotext ChangeLog

## [0.2.1] - 2023-10-25

### Fixed

- Fixed an issue with plots' sizes capping at their last `clf` size.
  https://github.com/Textualize/textual-plotext/issues/5

## [0.2.0] - 2023-10-25

### Added

- Added a set of plot themes that are full-RGB versions of the [builtin
  plotext
  themes](https://github.com/piccolomo/plotext/blob/master/readme/aspect.md#themes).
  Each is prefixed with `textual-` followed by the plotext theme name.
- Added `textual-design-dark` as a Textual-friendly theme designed for use
  with dark mode.
- Added `textual-design-light` as a Textual-friendly theme designed for use
  with light mode.

### Changed

- Change the default dark and light mode themes in `PlotextPlot` to use
  `textual-design-dark` and `textual-design-light`.

## [0.1.0] - 2023-10-03

- Initial release.
