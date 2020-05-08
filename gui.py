# pylint: disable=C0103,C0301
"""
GUI for app
"""

import os
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html as ddsih
import luts

# For hosting
path_prefix = os.getenv("REQUESTS_PATHNAME_PREFIX") or "/"

# Helper functions
def wrap_in_section(content, section_classes="", container_classes="", div_classes=""):
    """
    Helper function to wrap sections.
    Accepts an array of children which will be assigned within
    this structure:
    <section class="section">
        <div class="container">
            <div>[children]...
    """
    return html.Section(
        className="section " + section_classes,
        children=[
            html.Div(
                className="container " + container_classes,
                children=[html.Div(className=div_classes, children=content)],
            )
        ],
    )


def wrap_in_field(label, control):
    """
    Returns the control wrapped
    in Bulma-friendly markup.
    """
    return html.Div(
        className="field",
        children=[
            html.Label(label, className="label"),
            html.Div(className="control", children=control),
        ],
    )


header = ddsih.DangerouslySetInnerHTML(
    f"""
<div class="container">
<nav class="navbar" role="navigation" aria-label="main navigation">

  <div class="navbar-brand">
    <a class="navbar-item" href="https://www.snap.uaf.edu">
      <img src="{path_prefix}assets/IARC_color_square_acronym-2.svg">
    </a>

    <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div class="navbar-menu">
    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <a target="_blank" rel="noopener noreferrer" href="https://uaf-iarc.typeform.com/to/UCZcRB" class="button is-primary">
            <strong>Feedback</strong>
          </a>
        </div>
      </div>
    </div>
  </div>
</nav>
</div>
"""
)

about = wrap_in_section(
    [
        ddsih.DangerouslySetInnerHTML(
            f"""
<h1 class="title is-3">{luts.title}</h1>
<p>Explain app here.</p>
"""
        )
    ],
    div_classes="content is-size-5",
)


analog_bbox_n = wrap_in_field(
    "North", dcc.Input(id="analog_bbox_n", type="number", value=90)
)
analog_bbox_w = wrap_in_field(
    "West", dcc.Input(id="analog_bbox_w", type="number", value=0)
)
analog_bbox_s = wrap_in_field(
    "South", dcc.Input(id="analog_bbox_s", type="number", value=0)
)
analog_bbox_e = wrap_in_field(
    "East", dcc.Input(id="analog_bbox_e", type="number", value=360)
)

analog_bbox_form = wrap_in_section(
    [
        html.H3("Spatial extent of analog search area", className="subtitle is-4"),
        analog_bbox_n,
        analog_bbox_w,
        analog_bbox_s,
        analog_bbox_e,
    ]
)

forecast_bbox_n = wrap_in_field(
    "North", dcc.Input(id="forecast_bbox_n", type="number", value=90)
)
forecast_bbox_w = wrap_in_field(
    "West", dcc.Input(id="forecast_bbox_w", type="number", value=0)
)
forecast_bbox_s = wrap_in_field(
    "South", dcc.Input(id="forecast_bbox_s", type="number", value=70)
)
forecast_bbox_e = wrap_in_field(
    "East", dcc.Input(id="forecast_bbox_e", type="number", value=360)
)

forecast_bbox_form = wrap_in_section(
    [
        html.H3("Spatial extent of forecast", className="subtitle is-4"),
        forecast_bbox_n,
        forecast_bbox_w,
        forecast_bbox_s,
        forecast_bbox_e,
    ]
)

# TODO default these to moving window that makes sense
analog_temporal_daterange = wrap_in_field(
    "Date range for analog search",
    dcc.DatePickerRange(
        id="analog_daterange",
        display_format="MMMM YYYY",
        min_date_allowed=datetime(1950, 1, 1),
        max_date_allowed=datetime(2022, 12, 31),
        initial_visible_month=datetime(2017, 8, 5),
        end_date=datetime(2018, 8, 25).date(),
    ),
)

forecast_temporal_daterange = wrap_in_field(
    "Date range for forecast",
    dcc.DatePickerRange(
        id="forecast_daterange",
        display_format="MMMM YYYY",
        min_date_allowed=datetime(1950, 1, 1),
        max_date_allowed=datetime(2022, 12, 31),
        initial_visible_month=datetime(2017, 8, 5),
        end_date=datetime(2018, 8, 25).date(),
    ),
)

temporal_range_form = wrap_in_section(
    [
        html.H3("Spatial extent of forecast", className="subtitle is-4"),
        analog_temporal_daterange,
        forecast_temporal_daterange,
    ]
)

forecast_theme_control = wrap_in_field(
    "Forecast theme",
    dcc.Dropdown(
        id="forecast-theme",
        options=[
            {"label": theme, "value": value}
            for theme, value in luts.forecast_themes.items()
        ],
        value=1,
    ),
)

# TODO it looks like this field is only needed when
# "height" or "temp" forecast themes are used, and
# while the old interface had two drop-down, I think
# they weren't used in tandem.  Validate.
# Also make this reactive/hide when not needed if possible.
forecast_pressure = wrap_in_field(
    "Pressure",
    dcc.Dropdown(
        id="forecast-pressure",
        options=[
            {"label": pressure, "value": value}
            for pressure, value in luts.pressure_levels.items()
        ],
        value=1,
    ),
)

forecast_theme_section = wrap_in_section(
    [
        html.H3("Forecast theme", className="subtitle is-4"),
        forecast_theme_control,
        html.Div(
            id="forecast-pressure-wrapper",
            className="hidden",
            children=[forecast_pressure],
        ),
    ]
)

matching_method = wrap_in_field(
    "Method for matching",
    dcc.RadioItems(
        id="match_method",
        options=[
            {"label": "Match by parameter weights", "value": "weight"},
            {"label": "Match by index", "value": "index"},
        ],
        value="index",
    ),
)

method_weight_auto_weight = wrap_in_field(
    "Automatically calculate weightings?",
    dcc.RadioItems(
        id="auto-weight",
        options=[{"label": "Yes", "value": 1}, {"label": "No", "value": 0}],
        value=1,
    ),
)

def get_method_weight_field(param, weight):
    return wrap_in_field(param, dcc.Input(id="manual_weight_" + param, value=weight))


manual_weight_controls = []
for param, weight in luts.manual_weights.items():
    manual_weight_controls.append(get_method_weight_field(param, weight))
manual_weights_form = html.Div(
    id="manual-weights-form-wrapper", className="", children=manual_weight_controls
)

match_index_param = wrap_in_field(
    "Index for matching",
    dcc.Dropdown(
        id="forecast-match-index-param",
        options=[
            {"label": index, "value": value}
            for index, value in luts.match_indices.items()
        ],
        value=1,
    ),
)

match_parameter_form = html.Div(
    id="forecast-match-index-wrapper", className="", children=[match_index_param]
)

match_method_form = wrap_in_section([matching_method, manual_weights_form, match_parameter_form])

footer = html.Footer(
    className="footer has-text-centered",
    children=[
        html.Div(
            children=[
                html.A(
                    href="https://snap.uaf.edu",
                    className="snap",
                    children=[html.Img(src=path_prefix + "assets/SNAP_color_all.svg")],
                ),
                html.A(
                    href="https://snap.uaf.edu",
                    className="iarc",
                    children=[
                        html.Img(
                            src=path_prefix + "assets/IARC_color_square_acronym-2.svg"
                        )
                    ],
                ),
                html.A(
                    href="https://uaf.edu/uaf/",
                    children=[html.Img(src=path_prefix + "assets/UAF.svg")],
                ),
            ]
        ),
        ddsih.DangerouslySetInnerHTML(
            """
<p>UA is an AA/EO employer and educational institution and prohibits illegal discrimination against any individual.
<br><a href="https://www.alaska.edu/nondiscrimination/">Statement of Nondiscrimination</a></p>
            """
        ),
    ],
)

layout = html.Div(
    children=[
        header,
        html.Div(
            children=[
                match_method_form,
                about,
                analog_bbox_form,
                forecast_bbox_form,
                temporal_range_form,
                forecast_theme_section,
            ]
        ),
        footer,
    ]
)
