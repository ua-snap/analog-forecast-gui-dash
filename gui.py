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
analog_start_default, analog_end_default = luts.get_default_analog_daterange()
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

<p>This tool uses current atmospheric and sea surface temperature to identify the five best historical matches (analogs) as far back as 1949.  The analog identification is based on six variables from a current atmospheric reanalysis: surface air temperature, sea level pressure, precipitation, upper&ndash;air pressure (geopotential height), upper&ndash;air temperature, and sea surface temperature.</p>
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


def get_month_year_widget(name, id, years, default):
    return html.Div(
        children=[
            wrap_in_field(
                name + " month",
                dcc.Dropdown(
                    id=id + "-month",
                    options=[
                        {"label": month, "value": number}
                        for number, month in luts.months.items()
                    ],
                    value=default.month,
                ),
                "inline-date",
            ),
            wrap_in_field(
                name + " year",
                dcc.Dropdown(
                    id=id + "-year",
                    options=[{"label": year, "value": year} for year in years],
                    value=default.year,
                ),
                "inline-date",
            ),
            dcc.Input(id=id+"-date",className="hidden",value=default.strftime("%Y-%m-%d"))
        ]
    )


analog_temporal_start = get_month_year_widget(
    "Start", "analog-start", luts.analog_years, analog_start_default
)
analog_temporal_end = get_month_year_widget(
    "End", "analog-end", luts.analog_years, analog_end_default
)
analog_temporal_daterange = html.Div(
    children=[analog_temporal_start, analog_temporal_end],
    className="temporal-daterange",
)
forecast_temporal_start = get_month_year_widget(
    "Start", "forecast-start", luts.forecast_years, current_date
)
forecast_temporal_end = get_month_year_widget(
    "End", "forecast-end", luts.forecast_years, forecast_end_default
)
forecast_temporal_daterange = html.Div(
    children=[forecast_temporal_start, forecast_temporal_end],
    className="temporal-daterange",
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
    html.Div(id="forecast-daterange-validation", className="validation", children=[]),
    forecast_temporal_daterange,
]

left_column = [
    html.H5("Analog match search area & time", className="title is-5"),
    html.P(
        "The analog match search area is the spatial region that is analyzed for statistical matches.  This defaults to a region in the South Pacific which was empirically determined to correlate well with Alaska.    Longitudes go from 0-360E, and latitudes go from 0-90N.",
        className="content is-size-6",
    ),
    analog_bbox_fields,
    html.Div(id="analog-daterange-validation", className="validation", children=[]),
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
    ddsih.DangerouslySetInnerHTML("""
<div class="launch-notes content is-size-6">
    <p>Clicking the button below will open a new window that will run the analog forecast.</p>
    <p>⚠️ <strong>It may take up to three minutes for the results to be available.</strong>  Leave the window open until the processes completes.</p>
</div>
    """),
    html.Div(id="submit-validation", className="validation", children=[]),
    html.Button(
        "Run analog forecast",
        id="api-button",
        className="button is-primary",
        disabled=False,
        type="submit",
        formTarget="_blank",
        formAction="#",
        formMethod="POST"
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

<h3 class="title is-4">How does this tool work?</h3>

<p>First, a search area and time is defined. Data are available for entire months so the time can be defined as a single month (ie: August 2020) or a month range (ie: June through August 2020). The spatial bounds should be an area the user believes is climatologically predictive of the intended forecast area. The default is a region in the Pacific Ocean near the equator which climatologists have determined to be highly correlated with weather in Alaska.</p>
<p>Second, the model will compare the search range and area to other years’ data to find the closest matches. This is done by comparing the climate pattern across six variables in the search area to those patterns in the same area during the same period in past years. Root mean squared error (RMSE) between each past year and the search period is performed by grid cell and then weighted across each variable using an auto-weighting calculation. The sum of the weighted mean squared errors across all variables is the “Match Score” with low match scores corresponding to high levels of similarity between that year and the search year. The top five years by match score are displayed by default.</p>
<p>Third, a forecast area and time must be defined. Similar to the search area, data are available for entire months or month periods, and a forecast area should be chosen which the user believes to be highly correlated with past conditions in the search area. The default is a region over the state of Alaska which climatologists have determined to be highly correlated with conditions in the default search area over the Pacific Ocean.</p>
<p>Fourth, climate conditions in the forecast area during the forecast period are returned for each of the top five years by match score calculated during step 2. These display what the climate conditions looked like in the forecast area when conditions in the search area were similar to conditions during the search period.</p>
<p>Finally, the conditions returned during the top five match years in the forecast area are averaged to produce a composite forecast for the forecast period. This is a prediction of what climate conditions may look like in the forecast area during the forecast period based on conditions in the search area, during the search period.</p>
<div class="diagram">
<img src="{path_prefix}assets/AnalogForecastExplainerGraphic.jpg"/>
</div>
<h4 class="title is-5">Auto&ndash;weighting process</h4>
<p>The Root Mean Squared Error is computed for each variable and each year, which is then weighted for each variable according to the predictive power of that variable for the parameters input. The weight for each variable is determined by an algorithm developed by the tool’s initial developer Brian Brettschneider.  For each of the 5 variables a standard anomaly transformation is conducted with all values having 5.0 subtracted from them to retain the distinction between positive and negative values. RMSE with climatology is then conducted for each variable and eventually pattern match scores (RMSEs) of the forecast area compared to climatology are then built.</p>
<p>The relationship between each of the six constituent variables can then be compared to the dependent variable of the forecast area RMEs. A multiple linear regression determines the weighting of each variable with positive and negative values possible. That weight is then used as the coefficient for each RMSE value for each variable to get coefficient-adjusted root mean squared error values, or weighted RMSEs. It is this sum of weighted RMSEs which acts as the Match Score for each year.</p>

<h3 class="title is-4">Credits &amp; source code</h3>

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
