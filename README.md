# textual-plotext

A Textual widget wrapper for the [Plotext plotting
library](https://github.com/piccolomo/plotext).

## Introduction

TODO.

## What is supported?

The following utility functions are provided:

- `plt.sin`
- `plt.square`
- `plt.colorize`
- `plt.uncolorize`

## What isn't supported?

Some functions are not supported at all; mainly those that would not make
sense inside a Textual application. These include:

- `plt.interactive`
- `plt.script_folder`
- `plt.parent_folder`
- `plt.join_paths`
- `plt.save_text`
- `plt.read_data`
- `plt.write_data`
- `plt.download`
- `plt.delete_file`
- `plt.test`
- `plt.time`
- `plt.test_data_url`
- `plt.test_bar_data_url`
- `plt.test_image_url`
- `plt.test_gif_url`
- `plt.test_video_url`
- `plt.test_youtube_url`

The following properties and sub-modules also aren't exposed because they
also are intended more for REPL-based interactive use and so don't lend
themselves to being used in a Textual application:

- `plt.doc`
- `plt.markers`
- `plt.colors`
- `plt.styles`
- `plt.themes`

## What functions are no-ops?

Some functions are supported as calls but are redefined to be
non-operations; these are the sorts of code that wouldn't generally have a
negative side-effect but which don't make sense for a Textual application.
These include:

- `plt.clear_terminal`
- `plt.show`
- `plt.save_fig`
