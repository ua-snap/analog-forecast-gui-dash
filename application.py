# pylint: disable=C0103,C0301,E0401
"""
Template for SNAP Dash apps.
"""
import os
from datetime import datetime
import dash
from dash.dependencies import Input, Output
import luts
from gui import layout

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
    Output("forecast-pressure-wrapper", "className"),
    [Input("forecast-theme", "value")],
)
def toggle_pressure_field(pressure):
    """ Hide/show field based on other values """
    if pressure == 2 or pressure == 4:
        return "visible"
    else:
        return "hidden"


@app.callback(
    Output("forecast-match-index-wrapper", "className"),
    [Input("match_method", "value")],
)
def toggle_index_match_field(method):
    """ Hide/show field based on other values """
    if method == "index":
        return "visible"

    return "hidden"


@app.callback(
    Output("manual-weights-form-wrapper", "className"),
    [Input("auto-weight", "value")],
)
def toggle_manual_weights_form(method):
    """ Hide/show field based on other values """
    if method == 0:
        return "visible"

    return "hidden"



@app.callback(
    Output("manual-match-form-wrapper", "className"),
    [Input("manual-match", "value")],
)
def toggle_manual_match_form(method):
    """ Hide/show field based on other values """
    if method == 1:
        return "visible"

    return "hidden"


# @app.callback(Output("tally", "figure"), [Input("day_range", "value")])
# def update_api_url(day_range):
#     """ Build API URL string from GUI """
#     return


if __name__ == "__main__":
    application.run(debug=os.getenv("FLASK_DEBUG", default=False), port=8080)
