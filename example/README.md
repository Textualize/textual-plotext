# `textual-plotext` example

![The example code in action](https://raw.githubusercontent.com/Textualize/textual-plotext/main/textual-plotext-example.png)

[This code](./textual_towers_weather.py) is provided as an example of how to
use the `PlotextPlot` widget provided by `textual-plotext`. The aim is to
demonstrate:

- Inheriting from `PlotextPlot` to make your plotting widget.
- Using the `plot` method to create the plot.
- Loading up the data outside of the `plot` method.

As a bonus it also shows an example of using Textual's [worker
API](https://textual.textualize.io/guide/workers/) to create a [threaded
worker](https://textual.textualize.io/guide/workers/#thread-workers) to pull
the data from the backend.
