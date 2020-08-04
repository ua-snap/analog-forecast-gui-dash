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
from datetime import datetime as dt
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import dash
from dash.dependencies import Input, Output
import luts
from gui import layout, path_prefix

# URL base to API glue.
EAPI_API_URL = "localhost:3000"  # os.getenv("EAPI_API_URL")
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
    [
        Output("analog_daterange", "start_date"),
        Output("analog_daterange", "end_date"),
        Output("analog_daterange", "max_date_allowed"),
    ],
    [Input("analog_date_check", "value")],
)
def update_analog_date(nonce):
    current_date = dt.now()
    if current_date.day > 10:
        analog_start_default = current_date.replace(day=1) - relativedelta(months=3)
        analog_end_default = (
            current_date - relativedelta(months=1) + relativedelta(day=31)
        )

        # Trick to get last day of any month for maximum date
        last_day_of_last_month = current_date.replace(
            month=(current_date.month - 1)
        ) + relativedelta(day=31)

        return analog_start_default, analog_end_default, last_day_of_last_month
    else:
        analog_start_default = current_date.replace(day=1) - relativedelta(months=4)
        analog_end_default = (
            current_date - relativedelta(months=2) + relativedelta(day=31)
        )

        # Trick to get last day of any month for maximum date
        last_day_of_month_before_last = current_date.replace(
            month=(current_date.month - 2)
        ) + relativedelta(day=31)

        return analog_start_default, analog_end_default, last_day_of_month_before_last


@app.callback(
    [
        Output("forecast_daterange", "start_date"),
        Output("forecast_daterange", "end_date"),
    ],
    [Input("forecast_date_check", "value")],
)
def update_forecast_date(nonce):
    current_date = dt.now()
    forecast_end_default = current_date + relativedelta(months=2)
    return current_date, forecast_end_default


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


def ymd_from_dash(d):
    """ Helper function to return Y-m-d from Dash date GUI picker """
    date = dt.strptime(re.split("T| ", d)[0], "%Y-%m-%d")
    return date.strftime("%Y-%m-%d")


# The next piece is slightly painful but at least it's explicit.
@app.callback(
    Output("api-button", "href"),
    [
        Input("analog_bbox_n", "value"),
        Input("analog_bbox_w", "value"),
        Input("analog_bbox_e", "value"),
        Input("analog_bbox_s", "value"),
        Input("forecast_bbox_n", "value"),
        Input("forecast_bbox_w", "value"),
        Input("forecast_bbox_e", "value"),
        Input("forecast_bbox_s", "value"),
        Input("analog_daterange", "start_date"),
        Input("analog_daterange", "end_date"),
        Input("forecast_daterange", "start_date"),
        Input("forecast_daterange", "end_date"),
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
    analog_daterange_start,
    analog_daterange_end,
    forecast_daterange_start,
    forecast_daterange_end,
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
            analog_daterange_start=ymd_from_dash(analog_daterange_start),
            analog_daterange_end=ymd_from_dash(analog_daterange_end),
            forecast_daterange_start=ymd_from_dash(forecast_daterange_start),
            forecast_daterange_end=ymd_from_dash(forecast_daterange_end),
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
        )
    )
    url = EAPI_API_URL + "/forecast?" + params
    return url


if __name__ == "__main__":
    application.run(debug=os.getenv("FLASK_DEBUG", default=False), port=8080)
