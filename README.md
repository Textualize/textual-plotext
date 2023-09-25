# textual-plotext

A Textual widget wrapper for the [Plotext plotting
library](https://github.com/piccolomo/plotext).

## Introduction

The library makes one widget available: `PlotextPlot`. Your plots are made
inheriting from `PlotextPlot` and implementing the `plot` method. Within the
`plot` method you can reference the `plt` property (`self.plt`) and, with
some caveats (see below), write plotting code just as you would when using
Plotext.

Let's take [the first
example](https://github.com/piccolomo/plotext/blob/master/readme/basic.md#scatter-plot)
from [the Plotext README](https://github.com/piccolomo/plotext#readme):

```python
import plotext as plt
y = plt.sin() # sinusoidal test signal
plt.scatter(y)
plt.title("Scatter Plot") # to apply a title
plt.show() # to finally plot
```

The Textual equivalent of this (including everything needed to make this a
fully-working Textual application) is:

```python
from textual.app import App, ComposeResult
from textual_plotext import PlotextPlot

class ScatterPlot(PlotextPlot):

    def plot(self) -> None:
        y = self.plt.sin() # sinusoidal test signal
        self.plt.scatter(y)
        self.plt.title("Scatter Plot") # to apply a title

class ScatterApp(App[None]):

    def compose(self) -> ComposeResult:
        yield ScatterPlot()

if __name__ == "__main__":
    ScatterApp().run()
```

The main differences to note are:

- We're not directly importing `plotext`.
- We use `self.plt` rather than `plt`.
- We don't call Plotext's `show` method, `PlotextPlot` takes care of this.

## Installation

The library can be installed from PyPi:

```sh
$ pip install textual-plotext
```

Once installed you can quickly test the library by running the demo:

```sh
$ python -m textual_plotext
```

The demo app includes many of the examples shown in the Plotext README.

## Longer example

For a longer example of how to use the `PlotextPlot` widget, take a look at
[`example/textual_towers_weather.py`](./example/textual_towers_weather.py);
this provides examples of key points such as:

- Inheriting from `PlotextPlot` to make your plotting widget.
- Using the `plot` method to create the plot.
- Loading up the data outside of the `plot` method.

As a bonus it also shows an example of using Textual's [worker
API](https://textual.textualize.io/guide/workers/) to create a [threaded
worker](https://textual.textualize.io/guide/workers/#thread-workers) to pull
the data from the backend.

## Performance considerations

Because your `plot` method will be called each time the plot needs to be
rendered (if the widget's size changes, for example), it's best to do as
little processing as possible in the method. If you want to create your
plotting widget so that it gathers up and processes the data it wants to
show do *not* do this inside `plot`; instead consider doing it inside the
widget's `on_mount` method (perhaps making use of the [Textual worker
API](https://textual.textualize.io/guide/workers/) to gather the data in the
background).

In other words: only use the `plot` method to configure and declare the
plot, don't do any other work in there.

## What is supported?

The following utility functions are provided (via `self.plt`):

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

Also, currently, there is no support for [image
plots](https://github.com/piccolomo/plotext/blob/master/readme/image.md) or
[playing
videos](https://github.com/piccolomo/plotext/blob/master/readme/video.md);
one or both could follow at some point in the future.

## What functions are no-ops?

Some functions are supported as calls but are redefined to be
non-operations; these are the sorts of code that wouldn't generally have a
negative side-effect but which don't make sense for a Textual application.
These include:

- `plt.clear_terminal`
- `plt.show`
- `plt.save_fig`
