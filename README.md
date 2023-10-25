# textual-plotext

![PlotextPlot in action](https://raw.githubusercontent.com/Textualize/textual-plotext/main/textual-plotext-example.png)

A Textual widget wrapper for the [Plotext plotting
library](https://github.com/piccolomo/plotext).

## Introduction

The library makes one widget available: `PlotextPlot`. This widget provides
a `plt` property, which should be used where you would normally use `plt` as
seen in the Plotext documentation.

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

class ScatterApp(App[None]):

    def compose(self) -> ComposeResult:
        yield PlotextPlot()

    def on_mount(self) -> None:
        plt = self.query_one(PlotextPlot).plt
        y = plt.sin() # sinusoidal test signal
        plt.scatter(y)
        plt.title("Scatter Plot") # to apply a title

if __name__ == "__main__":
    ScatterApp().run()
```

The main differences to note are:

- We're not directly importing `plotext`.
- We use `PlotextPlot.plt` rather than `plt`.
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
[`examples/textual_towers_weather.py`](./examples/textual_towers_weather.py).
As a bonus it also shows an example of using Textual's [worker
API](https://textual.textualize.io/guide/workers/) to create a [threaded
worker](https://textual.textualize.io/guide/workers/#thread-workers) to pull
the data from the backend.

## What is supported?

The following utility functions are provided (via `PlotextPlot.plt`):

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
too are designed for REPL-based interactive use and don't lend themselves to
being used in a Textual application:

- `plt.doc`
- `plt.markers`
- `plt.colors`
- `plt.styles`
- `plt.themes`

Also, currently, there is no support for [GIF
plots](https://github.com/piccolomo/plotext/blob/master/readme/image.md#gif-plot) or
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

## Themes

Plotext has [a system of
themes](https://github.com/piccolomo/plotext/blob/master/readme/aspect.md#themes).
The themes provided by Plotext are supported by `PlotextPlot`. However, some
of those themes use "ANSI colors" and so may end up looking different
depending on which terminal you use, and what terminal theme is in use (if
your terminal supports themes); the issue here is that your plots may look
very different in different environments.

To help with this `textual-plotext` provides an additional set of copies of
those themes, all prefixed with `textual-`, that use full RGB coloring to
ensure that, when using a given Plotext theme, it will look the same
everywhere.

In addition to the Plotext themes, `textual-plotext` also adds two themes
called:

- `textual-design-dark`
- `textual-design-light`

These are two similar themes designed to look good in dark mode and light
mode respectively. Out of the box, `PlotextPlot` will use these and will
switch between them when your [Textual application switches between dark and
light mode](https://textual.textualize.io/api/app/#textual.app.App.dark). If
you wish to turn off this behaviour, simply set the `auto_theme` property of
your plot to `False`.

## Known issues

At the moment, due to what appears to be a bug in Plotext when it comes to
repeated calls to `show` or `build`[^1] for a plot with x or y scales set to
`"log"`, it isn't possible to easily build such a plot. In other words, even
in the REPL with Plotext itself, a session such as this:

```python
>>> import plotext as plt
>>> plt.xscale("log")
>>> plt.plot(plt.sin(periods=2, length=10**4))
>>> plt.show()
<plot is drawn in the terminal here>
>>> plt.show()
```

results in a `ValueError: math domain error`.

There is a workaround for this, which will work for Plotext use in general
and would also work nicely in a Textual app. After the first `show` or
`build`, set the problematic scale back to `"linear"`. So the REPL session
should above would become:

```python
>>> import plotext as plt
>>> plt.xscale("log")
>>> plt.plot(plt.sin(periods=2, length=10**4))
>>> plt.show()
<plot is drawn in the terminal here>
>>> plt.xscale("linear")     # Note this here!
>>> plt.show()
<plot is drawn in the terminal here>
>>> plt.show()
<plot is drawn in the terminal here>
etc...
```

In a Textual app, this would mean adding (assuming the `xscale` was the
problem here) this at the end of the code to create the plot:

```python
_ = self.plt.build()
self.plt.xscale("linear")
```

## Need more help?

If you need help with this library, or with anything relating to Textual,
feel free to come join the [Textualize](https://www.textualize.io/)
[devs](https://www.textualize.io/about-us/) [on
Discord](https://discord.gg/Enf6Z3qhVr) or [the other places where we
provide support](https://textual.textualize.io/help/).

[^1]: Repeated calls to `build` will happen when the `PlottextPlot` widget
    needs to `render` the plot again, on resize for example.
