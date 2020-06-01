# pylint: disable=C0103,C0301,E0401
"""
Template for SNAP Dash apps.
"""
import os
import urllib.parse
import dash
from dash.dependencies import Input, Output
import luts
from gui import layout

# URL base to API glue.
EAPI_API_URL = os.getenv("EAPI_API_URL")
if EAPI_API_URL is None:
    raise RuntimeError("EAPI_API_URL environment variable not set.")

app = dash.Dash(
    __name__, requests_pathname_prefix=os.environ["REQUESTS_PATHNAME_PREFIX"]
)

# AWS Elastic Beanstalk looks for application by default,
# if this variable (application) isn't set you will get a WSGI error.
application = app.server
app.title = luts.title
app.index_string = luts.index_string
app.layout = layout


@app.callback(
    Output("manual-weights-form-wrapper", "className"), [Input("auto-weight", "value")]
)
def toggle_manual_weights_form(method):
    """ Hide/show field based on other values """
    if method == 0:
        return "visible"

    return "hidden"


@app.callback(
    Output("manual-match-form-wrapper", "className"), [Input("manual-match", "value")]
)
def toggle_manual_match_form(method):
    """ Hide/show field based on other values """
    if method == 0:
        return "visible"

    return "hidden"


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
    detrend_data
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
            analog_daterange_start=analog_daterange_start,
            analog_daterange_end=analog_daterange_end,
            forecast_daterange_start=forecast_daterange_start,
            forecast_daterange_end=forecast_daterange_end,
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
    url = EAPI_API_URL + "/?" + params

    print(url)
    return url


if __name__ == "__main__":
    application.run(debug=os.getenv("FLASK_DEBUG", default=False), port=8080)
