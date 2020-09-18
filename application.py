# pylint: disable=C0103,C0301,E0401
"""
Implements GUI controls for this app.

Note that some controls are here which aren't
currently exposed: this is delibrate, since we
found during development that some of the variables
didn't function in a way we expected with the
processing code, so we've pared it back to the
minimum.

"""
import os
import re
import urllib.parse
from datetime import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import luts
from gui import layout, path_prefix

# URL base to API glue.
EAPI_API_URL = os.getenv("EAPI_API_URL")
if EAPI_API_URL is None:
    raise RuntimeError("EAPI_API_URL environment variable not set.")

app = dash.Dash(__name__, requests_pathname_prefix=path_prefix)

# AWS Elastic Beanstalk looks for application by default,
# if this variable (application) isn't set you will get a WSGI error.
application = app.server
app.title = luts.title
app.index_string = luts.index_string
app.layout = layout

# Not exposed in current version of app.
@app.callback(
    Output("manual-weights-form-wrapper", "className"), [Input("auto-weight", "value")]
)
def toggle_manual_weights_form(method):
    """ Hide/show field based on other values """
    # 0=override weights, 1=auto match
    if method == 0:
        return "visible"

    return "hidden"


@app.callback(
    Output("analog-start-date", "value"),
    [Input("analog-start-month", "value"), Input("analog-start-year", "value"),],
)
def update_analog_start_date(month, year):
    return datetime(month=month, year=year, day=1).strftime("%Y-%m-%d")


@app.callback(
    Output("analog-end-date", "value"),
    [Input("analog-end-month", "value"), Input("analog-end-year", "value"),],
)
def update_analog_end_date(month, year):
    return datetime(month=month, year=year, day=1).strftime("%Y-%m-%d")


@app.callback(
    Output("forecast-start-date", "value"),
    [Input("forecast-start-month", "value"), Input("forecast-start-year", "value"),],
)
def update_forecast_start_date(month, year):
    return datetime(month=month, year=year, day=1).strftime("%Y-%m-%d")


@app.callback(
    Output("forecast-end-date", "value"),
    [Input("forecast-end-month", "value"), Input("forecast-end-year", "value"),],
)
def update_forecast_end_date(month, year):
    return datetime(month=month, year=year, day=1).strftime("%Y-%m-%d")


def datetime_from_input(date):
    """ Tiny helper to convert from string to datetime. """
    return datetime.strptime(date, "%Y-%m-%d")


@app.callback(
    [
        Output("analog-daterange-validation", "children"),
        Output("forecast-daterange-validation", "children"),
        Output("submit-validation", "children"),
        Output("api-button", "disabled"),
    ],
    [
        Input("analog-start-date", "value"),
        Input("analog-end-date", "value"),
        Input("forecast-start-date", "value"),
        Input("forecast-end-date", "value"),
    ],
)
def validate_analog_dates(analog_start, analog_end, forecast_start, forecast_end):
    """
    Test the analog date spans.  If invalid, let the user know.

    Rules to test for Analogs:
        1. start date must not be after end date
        2. start date must be no more than 12 months before date.
        3. end date must be equal to or less than the current data
        availability date.
        4. end date must come before the forecast start date.
    Rules to test for Forecast:
        5. start date must not be after end date
        6. end month must be <= 12 months after start date
    """
    analog_start = datetime_from_input(analog_start)
    analog_end = datetime_from_input(analog_end)
    forecast_start = datetime_from_input(forecast_start)
    forecast_end = datetime_from_input(forecast_end)
    default_start_date, default_end_date = luts.get_default_analog_daterange()
    general_error = html.Span(
        "Please fix the invalid configurations elsewhere on this page before running this forecast."
    )

    # Case 3
    if analog_end > default_end_date:
        return (
            html.Span(
                "⚠️ Data aren't available after {}.  Please change the start date to be no later than that.".format(
                    default_start_date.strftime("%B, %Y")
                )
            ),
            None,
            general_error,
            "disabled",
        )

    # Case 1
    if analog_start > analog_end:
        return (
            html.Span(
                "⚠️ The start date must come before, or be the same as, the end date."
            ),
            None,
            general_error,
            "disabled",
        )

    # Case 2
    if analog_start < (analog_end - relativedelta(months=12)):
        return (
            html.Span("⚠️ Analog search range can only be up to 12 months total."),
            None,
            general_error,
            "disabled",
        )

    # Case 4
    if analog_end >= forecast_start:
        return (
            html.Span("⚠️ Analog search range must end before the start of the forecast date range."),
            None,
            general_error,
            "disabled",
        )

    # Case 5
    if forecast_start > forecast_end:
        return (
            None,
            html.Span(
                "⚠️ The start date must come before, or be the same as, the end date."
            ),
            general_error,
            "disabled",
        )

    # Case 6
    if forecast_start < (forecast_end - relativedelta(months=12)):
        return (
            None,
            html.Span("⚠️ Forecast range can only be up to 12 months total."),
            general_error,
            "disabled",
        )

    # 🏁 Valid!
    return None, None, None, False


# Not exposed in current version of app.
@app.callback(
    Output("manual-match-form-wrapper", "className"), [Input("manual-match", "value")]
)
def toggle_manual_match_form(method):
    """ Hide/show field based on other values """
    # This one is for manually picking years.
    # 1=override (manual match).  0= auto match
    # Test
    if method == 1:
        return "visible"

    return "hidden"


# The next piece is slightly painful but at least it's explicit.
@app.callback(
    Output("api-button", "formAction"),
    [
        Input("analog_bbox_n", "value"),
        Input("analog_bbox_w", "value"),
        Input("analog_bbox_e", "value"),
        Input("analog_bbox_s", "value"),
        Input("forecast_bbox_n", "value"),
        Input("forecast_bbox_w", "value"),
        Input("forecast_bbox_e", "value"),
        Input("forecast_bbox_s", "value"),
        Input("analog-start-date", "value"),
        Input("analog-end-date", "value"),
        Input("forecast-start-date", "value"),
        Input("forecast-end-date", "value"),
        Input("num_analogs", "value"),
        Input("forecast-theme", "value"),
        Input("auto-weight", "value"),
        Input("manual_weight_1", "value"),
        Input("manual_weight_2", "value"),
        Input("manual_weight_3", "value"),
        Input("manual_weight_4", "value"),
        Input("manual_weight_5", "value"),
        Input("correlation", "value"),
        Input("manual-match", "value"),
        Input("override-year-1", "value"),
        Input("override-year-2", "value"),
        Input("override-year-3", "value"),
        Input("override-year-4", "value"),
        Input("override-year-5", "value"),
        Input("detrend-data", "value"),
        Input("pressure_height", "value"),
        Input("pressure_temp", "value"),
    ],
)
def update_api_url(
    analog_bbox_n,
    analog_bbox_w,
    analog_bbox_e,
    analog_bbox_s,
    forecast_bbox_n,
    forecast_bbox_w,
    forecast_bbox_e,
    forecast_bbox_s,
    analog_start_date,
    analog_end_date,
    forecast_start_date,
    forecast_end_date,
    num_analogs,
    forecast_theme,
    auto_weight,
    manual_weight_1,
    manual_weight_2,
    manual_weight_3,
    manual_weight_4,
    manual_weight_5,
    correlation,
    manual_match,
    override_year_1,
    override_year_2,
    override_year_3,
    override_year_4,
    override_year_5,
    detrend_data,
    pressure_height,
    pressure_temp,
):
    """ Build API URL string from GUI """
    params = urllib.parse.urlencode(
        dict(
            analog_bbox_n=analog_bbox_n,
            analog_bbox_w=analog_bbox_w,
            analog_bbox_e=analog_bbox_e,
            analog_bbox_s=analog_bbox_s,
            forecast_bbox_n=forecast_bbox_n,
            forecast_bbox_w=forecast_bbox_w,
            forecast_bbox_e=forecast_bbox_e,
            forecast_bbox_s=forecast_bbox_s,
            analog_daterange_start=analog_start_date,
            analog_daterange_end=analog_end_date,
            forecast_daterange_start=forecast_start_date,
            forecast_daterange_end=forecast_end_date,
            num_analogs=num_analogs,
            forecast_theme=forecast_theme,
            auto_weight=auto_weight,
            manual_weight_1=manual_weight_1,
            manual_weight_2=manual_weight_2,
            manual_weight_3=manual_weight_3,
            manual_weight_4=manual_weight_4,
            manual_weight_5=manual_weight_5,
            correlation=correlation,
            manual_match=manual_match,
            override_year_1=override_year_1,
            override_year_2=override_year_2,
            override_year_3=override_year_3,
            override_year_4=override_year_4,
            override_year_5=override_year_5,
            detrend_data=detrend_data,
            pressure_height=pressure_height,
            pressure_temp=pressure_temp,
        )
    )
    url = EAPI_API_URL + "/forecast?" + params
    return url


if __name__ == "__main__":
    application.run(debug=os.getenv("FLASK_DEBUG", default=False), port=8080)
