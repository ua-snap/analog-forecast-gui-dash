# pylint: disable=C0103,C0301
"""
GUI for app
"""

import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html as ddsih
import luts

# Used in some fields & copyright date
current_year = datetime.now().year

# Compute default date ranges.
current_date = datetime.now()
analog_start_default = current_date - relativedelta(months=3)
analog_end_default = current_date - relativedelta(months=1)
forecast_end_default = current_date + relativedelta(months=2)
max_analog_date_allowed = current_date

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
    <a class="navbar-item" href="https://uaf-iarc.org">
      <img src="{path_prefix}assets/IARC_2020_color_horiz.svg">
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
          <a target="_blank" rel="noopener noreferrer" href="https://uaf-iarc.typeform.com/to/mN7J5cCK#tool=Analog%20Forecast" class="button is-link">
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

<p>This tool uses current atmospheric and sea surface temperature to identify the five best historical matches (analogs) as far back as 1949.  The analog identification is based on up to six variables from a current atmospheric reanalysis: surface air temperature, sea level pressure, precipitation, upper-air pressure (geopotential height), upper-air temperature, and sea surface temperature.</p>
<p>The tool then provides a forecast based on how the weather patterns evolved in those analog years.  The forecasts are for 1 to 12 months into the future.  Users specify the areas from which the analogs are determined.  The areas can include the Arctic, middle latitudes, and even tropics, where ocean temperatures and pressures correlate with future weather over large parts of the Northern Hemisphere. The area covered by the forecast is also selected by the user, and it can be different from the area of the predictors.</p>
<p><strong>This tool is designed for trained professionals and others with experience in the use of climate data for planning.</strong>  It can also be used by broader audiences who are familiar with atmospheric data and who understand the limitations of the analog method of forecasting.</p>
<p>Date ranges can be chosen with the popup calendar <strong>or by typing in the boxes directly</strong>.  Only month/year is used for analysis purposes.</p>

"""
        )
    ],
    div_classes="content is-size-5 narrow",
)

analog_bbox_fields = html.Div(
    children=[
        wrap_in_field(
            "North", dcc.Input(id="analog_bbox_n", type="number", value=20), "inline"
        ),
        wrap_in_field(
            "West", dcc.Input(id="analog_bbox_w", type="number", value=110), "inline"
        ),
        wrap_in_field(
            "South", dcc.Input(id="analog_bbox_s", type="number", value=10), "inline"
        ),
        wrap_in_field(
            "East", dcc.Input(id="analog_bbox_e", type="number", value=140), "inline"
        ),
    ]
)

forecast_bbox_fields = html.Div(
    children=[
        wrap_in_field(
            "North", dcc.Input(id="forecast_bbox_n", type="number", value=72), "inline"
        ),
        wrap_in_field(
            "West", dcc.Input(id="forecast_bbox_w", type="number", value=180), "inline"
        ),
        wrap_in_field(
            "South", dcc.Input(id="forecast_bbox_s", type="number", value=53), "inline"
        ),
        wrap_in_field(
            "East", dcc.Input(id="forecast_bbox_e", type="number", value=230), "inline"
        ),
    ]
)


analog_temporal_daterange = html.Div(
    children=[
        wrap_in_field(
            "Date range for analog search",
            dcc.DatePickerRange(
                id="analog_daterange",
                display_format="MMMM YYYY",
                min_date_allowed=datetime(1950, 1, 1),
                max_date_allowed=max_analog_date_allowed,
                start_date=analog_start_default,
                end_date=analog_end_default,
            ),
        ),
        dcc.Input(id="analog_date_check", type="text", placeholder="analog_date"),
    ]
)

forecast_temporal_daterange = html.Div(
    children=[
        wrap_in_field(
            "Date range for forecast",
            dcc.DatePickerRange(
                id="forecast_daterange",
                display_format="MMMM YYYY",
                start_date=current_date,
                end_date=forecast_end_default,
            ),
        ),
        dcc.Input(id="forecast_date_check", type="text", placeholder="forecast_date"),
    ]
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
        value=3,
    ),
)

# Not exposed in current version of app.
num_of_analogs = wrap_in_field(
    "Number of analogs",
    dcc.Dropdown(
        id="num_analogs",
        options=[{"label": value, "value": value} for value in range(1, 6)],
        value=5,
    ),
    className="hidden",
)

pressure_height = wrap_in_field(
    "Pressure level for height analysis",
    dcc.Dropdown(
        id="pressure_height",
        options=[
            {"label": label, "value": value}
            for value, label in luts.pressure_levels.items()
        ],
        value=5,
    ),
)

pressure_temp = wrap_in_field(
    "Pressure level for temperature analysis",
    dcc.Dropdown(
        id="pressure_temp",
        options=[
            {"label": label, "value": value}
            for value, label in luts.pressure_levels.items()
        ],
        value=5,
    ),
)
# Not exposed in current version of app.
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
    className="hidden",
)

# Not exposed in current version of app.
method_weight_auto_weight = wrap_in_field(
    "Automatically calculate weightings?",
    dcc.RadioItems(
        id="auto-weight",
        options=[{"label": "Yes", "value": 1}, {"label": "No", "value": 0}],
        value=1,
    ),
    className="hidden",
)

# Not exposed in current version of app.
def get_method_weight_field(param, config):
    return wrap_in_field(
        param,
        dcc.Input(id="manual_weight_" + str(config["idx"]), value=config["default"]),
    )


# Not exposed in current version of app.
manual_weight_controls = [html.P("Info about manual weighting")]
for param, config in luts.manual_weights.items():
    manual_weight_controls.append(get_method_weight_field(param, config))

manual_weights_form = html.Div(
    id="manual-weights-form-wrapper",
    className="hidden",
    children=manual_weight_controls,
)

# Not exposed in current version of app.
if_detrend_data = wrap_in_field(
    "Detrend data?",
    dcc.RadioItems(
        id="detrend-data",
        options=[{"label": "Yes", "value": 1}, {"label": "No", "value": 0}],
        value=0,
    ),
    className="hidden",
)

# Not exposed in current version of app.
override_years = wrap_in_field(
    "Automatically choose match years?",
    dcc.RadioItems(
        id="manual-match",
        options=[{"label": "Yes", "value": 0}, {"label": "No", "value": 1}],
        value=0,
    ),
    className="hidden",
)

# Not exposed in current version of app.
def get_override_year_dropdown(field_id, year):
    """ Build standard list of dropdowns for manual match years """
    return dcc.Dropdown(
        id=field_id,
        options=[
            {"label": value, "value": value} for value in range(1949, current_year + 1)
        ],
        value=year,
    )


# Not exposed in current version of app.
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

center_column = [
    html.H5("Forecast theme, area, and time span", className="title is-5"),
    html.P(
        "Forecast area defaults to approximately the spatial extent of Alaska. Longitudes go from 0-360E, and latitudes go from 0-90N.",
        className="content is-size-6",
    ),
    forecast_theme_control,
    forecast_bbox_fields,
    forecast_temporal_daterange,
]

left_column = [
    html.H5("Analog match search area & time", className="title is-5"),
    html.P(
        "The analog match search area is the spatial region that is analyzed for statistical matches.  This defaults to a region in the South Pacific which was empirically determined to correlate well with Alaska.    Longitudes go from 0-360E, and latitudes go from 0-90N.",
        className="content is-size-6",
    ),
    analog_bbox_fields,
    analog_temporal_daterange,
    num_of_analogs,
    method_weight_auto_weight,
    manual_weights_form,
    correlations_control,
    override_years,
    manual_match_fields_wrapper,
    if_detrend_data,
    pressure_height,
    pressure_temp,
]

right_column = [
    html.H5("Run analog forecast", className="title is-5"),
    html.P(
        """
Clicking the button below will open a new window that will run the analog forecast.  It may take a few minutes for the results to be available.
""",
        className="content is-size-6",
    ),
    html.A(
        "Run analog forecast",
        id="api-button",
        href="#",
        className="button is-primary",
        target="_blank",
    ),
]

# Main app wrapper starts here
main_section = html.Div(
    children=[
        wrap_in_section(  # gives us section & container
            html.Form(
                children=[
                    html.Div(  # Form & Column wrapper
                        className="columns",
                        children=[
                            html.Div(className="column", children=left_column),
                            html.Div(className="column", children=center_column),
                            html.Div(className="column", children=right_column),
                        ],
                    )
                ]
            )  # end column structure
        )
    ]
)

about_data = wrap_in_section(
    [
        ddsih.DangerouslySetInnerHTML(
            f"""
<h2 class="title is-3">About this tool</h2>
<h3 class="title is-4">Data source</h3>
<p>The data comes from the NCEI/NCAR R1 reanalysis. Although now superseded by more modern reanalysis, R1 is used because it offers the longest period of record (since 1949) and is kept up to date.</p>

<h3 class="title is-4">What algorithm is used?</h3>

<p>The criterion for the selection of the analogs is the closeness of the match to the present atmospheric conditions over the area selected by the user.  The metric of the closeness of fit is the root-mean-square difference (current state minus analog candidate) of the predictor variables summed over all grid points in the user-selected area of the predictor variables.</p>

<h3 class="title is-4">Credits & source code</h3>

<p>Brian Brettschneider with the <a href="https://uaf-accap.org">Alaska Center for Climate Assessment and Policy</a> (ACCAP) developed the science and code for this tool.  Brian now works with the National Weather Service, Anchorage.</p>

<p>Source code is available on Github:</p>
<ul>
<li><a href="https://github.com/ua-snap/analog-forecast-gui-dash">Front-end user interface code</a> (this page)</li>
<li><a href="https://github.com/ua-snap/eapi-api">API code</a>.  The API takes information from the user interface and executes the NCL scientific code and presents results.</li>
<li><a href="https://github.com/ua-snap/eapi-analogs">Scientific processing code</a>.  This is the original source code which contains the NCL processing scripts.</li>
</ul>

"""
        )
    ],
    div_classes="content is-size-5 narrow",
)
footer = html.Footer(
    className="footer",
    children=[
        ddsih.DangerouslySetInnerHTML(
            f"""
 <div class="container">
    <div class="wrapper is-size-6">
        <img src="{path_prefix}assets/UAF.svg"/>
        <div class="wrapped">
        <p>Multiple individuals and groups supported the development of the Analog Forecast Tool. Brian Brettschneider developed the science and code for the tool, with guidance from the National Weather Service Alaska Region and <a href="https://uaf-accap.org">Alaska Center for Climate Assessment and Policy</a> (ACCAP). Website development was supported by ACCAP and the <a href="https://www.snap.uaf.edu/" title="👍">Scenarios Network for Alaska and Arctic Planning</a> (SNAP). Financial support for the tool was provided by the <a href="https://cpo.noaa.gov">NOAA Climate Program Office</a>, <a href="https://sites.google.com/alaska.edu/eapi">Experimental Arctic Prediction Initiative</a>, and ACCAP.</p>
            <p>Copyright &copy; {current_year} University of Alaska Fairbanks.  All rights reserved.</p>
            <p>UA is an AA/EO employer and educational institution and prohibits illegal discrimination against any individual.  <a href="https://www.alaska.edu/nondiscrimination/">Statement of Nondiscrimination</a></p>
        </div>
    </div>
 </div>
            """
        ),
    ],
)


layout = html.Div(children=[header, about, main_section, about_data, footer])
