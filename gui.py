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

# Used in some fields & copyright date
current_year = datetime.now().year

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


def wrap_in_field(label, control, className=""):
    """
    Returns the control wrapped
    in Bulma-friendly markup.
    """
    return html.Div(
        className="field " + className,
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

analog_bbox_fields = html.Div(
    children=[
        wrap_in_field(
            "North", dcc.Input(id="analog_bbox_n", type="number", value=90), "inline"
        ),
        wrap_in_field(
            "West", dcc.Input(id="analog_bbox_w", type="number", value=0), "inline"
        ),
        wrap_in_field(
            "South", dcc.Input(id="analog_bbox_s", type="number", value=0), "inline"
        ),
        wrap_in_field(
            "East", dcc.Input(id="analog_bbox_e", type="number", value=360), "inline"
        ),
    ]
)

forecast_bbox_fields = html.Div(
    children=[
        wrap_in_field(
            "North", dcc.Input(id="forecast_bbox_n", type="number", value=90), "inline"
        ),
        wrap_in_field(
            "West", dcc.Input(id="forecast_bbox_w", type="number", value=0), "inline"
        ),
        wrap_in_field(
            "South", dcc.Input(id="forecast_bbox_s", type="number", value=70), "inline"
        ),
        wrap_in_field(
            "East", dcc.Input(id="forecast_bbox_e", type="number", value=360), "inline"
        ),
    ]
)


# TODO default these to moving window that makes sense
# TODO these may suck for year/month entry without day
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
    [html.H3("Spatial extent of forecast", className="subtitle is-4")]
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

num_of_analogs = wrap_in_field(
    "Number of analogs",
    dcc.Dropdown(
        id="num_analogs",
        options=[{"label": value, "value": value} for value in range(1, 6)],
        value=5,
    ),
)

correlations_control = wrap_in_field(
    "Just plot correlations?",
    dcc.Dropdown(
        id="correlation",
        options=[
            {"label": theme, "value": value}
            for theme, value in luts.correlations.items()
        ],
        value=0,
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

# TODO need to make this indexed so the IDs aren't clobbered,
# or slugify or something


def get_method_weight_field(param, config):
    return wrap_in_field(
        param,
        dcc.Input(id="manual_weight_" + str(config["idx"]), value=config["default"]),
    )


manual_weight_controls = [html.P("Info about manual weighting")]
for param, config in luts.manual_weights.items():
    manual_weight_controls.append(get_method_weight_field(param, config))

manual_weights_form = html.Div(
    id="manual-weights-form-wrapper",
    className="hidden",
    children=manual_weight_controls,
)

if_detrend_data = wrap_in_field(
    "Detrend data?",
    dcc.RadioItems(
        id="detrend-data",
        options=[{"label": "Yes", "value": 1}, {"label": "No", "value": 0}],
        value=1,
    ),
)


override_years = wrap_in_field(
    "Automatically choose match years?",
    dcc.RadioItems(
        id="manual-match",
        options=[{"label": "Yes", "value": 1}, {"label": "No", "value": 0}],
        value=1,
    ),
)


def get_override_year_dropdown(field_id, year):
    """ Build standard list of dropdowns for manual match years """
    return dcc.Dropdown(
        id=field_id,
        options=[
            {"label": value, "value": value} for value in range(1949, current_year + 1)
        ],
        value=year,
    )


manual_match_years = {
    "override-year-1": 1949,
    "override-year-2": 1959,
    "override-year-3": 1969,
    "override-year-4": 1979,
    "override-year-5": 1989,
}
manual_match_fields = [
    html.P(
        "All years must be different, and not in the future.",
        className="content is-size-6",
    )
]
for field_id, year in manual_match_years.items():
    manual_match_fields.append(get_override_year_dropdown(field_id, year))

manual_match_fields_wrapper = html.Div(
    id="manual-match-form-wrapper", className="hidden", children=manual_match_fields
)

run_section = wrap_in_section(
    [
        dcc.Markdown(
            """
Click the button below to launch a new window that will run the analog forecast with the parameters you have selected.

It may take a few minutes for the results to be available.
""",
            className="content is-size-5",
        ),
        html.A(
            "Run analog forecast",
            id="api-button",
            href="#",
            className="button is-primary is-large",
            target="_blank",
        ),
        html.Div("cats and dogs", id="textarea-example-output", style={"white-space": "pre-line"}),
    ]
)

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
            f"""
<p>UA is an AA/EO employer and educational institution and prohibits illegal discrimination against any individual.
<br><a href="https://www.alaska.edu/nondiscrimination/">Statement of Nondiscrimination</a></p>
<p class="copyright">Copyright &copy; {current_year} University of Alaska Fairbanks.  All rights reserved.</p>
            """
        ),
    ],
)

left_column = [
    html.H4("Spatial & temporal extents", className="subtitle is-4"),
    html.H5("Analog match search area & time", className="subtitle is-5"),
    analog_bbox_fields,
    analog_temporal_daterange,
    html.H5("Forecast area & time", className="subtitle is-5"),
    forecast_bbox_fields,
    forecast_temporal_daterange,
]

right_column = [
    html.H4("Output parameter configuration", className="subtitle is-4"),
    num_of_analogs,
    forecast_theme_control,
    method_weight_auto_weight,
    manual_weights_form,
    correlations_control,
    override_years,
    manual_match_fields_wrapper,
]

layout = html.Div(
    children=[
        header,
        # Main app wrapper starts here
        html.Div(
            children=[
                about,
                wrap_in_section(  # gives us section & container
                    html.Div(  # Form & Column wrapper
                        className="columns",
                        children=[
                            # Left column
                            html.Div(
                                className="column",
                                children=[html.Form(children=left_column)],
                            ),
                            # Right columns
                            html.Div(
                                className="column",
                                children=[html.Form(children=right_column)],
                            ),
                        ],
                    )
                ),  # end column structure
            ]
        ),
        run_section,
        footer,
    ]
)
