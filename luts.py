# pylint: disable=C0103
"""
Common shared text strings and lookup tables.
"""
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

title = "Analog Forecast Tool"
url = "http://snap.uaf.edu/tools/demo"
path_prefix = os.getenv("REQUESTS_PATHNAME_PREFIX") or "/"
preview = path_prefix + "assets/preview.png"
description = "The Analog forecast tool enables users to use the state of the climate in one time and area in the past to develop a forecast for a different time and area in the future. The user defines a search area and time and the tool finds years in the past where conditions were most similar. The top 5 match years are then used to find conditions in the forecast area in those years during the forecast time, and a composite of those results is automatically produced."

# Customize this layout to include Google Analytics
# and opengraph tags
gtag_id = os.getenv("GTAG_ID", default="")

index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={gtag_id}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());

          gtag('config', '{gtag_id}');
        </script>
        {{%metas%}}
        <title>{{%title%}}</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Schema.org markup for Google+ -->
        <meta itemprop="name" content="{title}">
        <meta itemprop="description" content="{description}">
        <meta itemprop="image" content="{preview}">

        <!-- Twitter Card data -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:site" content="@SNAPandACCAP">
        <meta name="twitter:title" content="{title}">
        <meta name="twitter:description" content="{description}">
        <meta name="twitter:creator" content="@SNAPandACCAP">
        <!-- Twitter summary card with large image must be at least 280x150px -->
        <meta name="twitter:image:src" content="{preview}">

        <!-- Open Graph data -->
        <meta property="og:title" content="{title}" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="{url}" />
        <meta property="og:image" content="{preview}" />
        <meta property="og:description" content="{description}" />
        <meta property="og:site_name" content="{title}" />

        <link rel="alternate" hreflang="en" href="{url}" />
        <link rel="canonical" href="{url}"/>
        {{%favicon%}}
        {{%css%}}
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

# Determines which forecast theme to run
# x-ref manual_weights if updating this to keep
# text aligned.
forecast_themes = {
    "Sea level pressure": 1,
    "Pressure level height": 2,
    "2-meter temperatures": 3,
    "Pressure level temperatures": 4,
    "Sea surface temperature": 5,
    "Precipitation": 6,
}

correlations = {
    "No": 0,
    "R-Value Maps": 1,
    "R2-Value Maps": 2,
    "Multiple R Correlation": 3,
}

# Selection for manual weighting
# TODO: x-ref `forecast_themes` to keep text aligned(?)
# idx refers to the number that is postfixed to the control
# to get a unique element ID to process for the API
manual_weights = {
    "SLP": dict(default=100, idx=1),
    "Pressure level height": dict(default=0, idx=2),
    "2-meter temps": dict(default=0, idx=3),
    "Pressure level temp": dict(default=0, idx=4),
    "SST": dict(default=0, idx=5),
}

# These correlate to the custom ncar library file BB_Utils,
# in the function getlev()
pressure_levels = {1: "925mb", 5: "500mb", 9: "200mb"}

months = {i: datetime(2020, i, 1).strftime("%B") for i in range(1, 13)}


def get_default_analog_daterange():
    """
    Data are SOMETIMES available after the 10th each month.
    So, until then, the most-current-available-month is
    the prior month.

    Known issue is that the datasets can lag by more than 3 months, 
    causing the processing API to crash when NCL is invoked.

    Not much we can do about this.
    """
    current_date = datetime.now()
    if current_date.day > 10:
        analog_start_default = current_date.replace(day=1) - relativedelta(months=4)
        analog_end_default = current_date.replace(day=2) - relativedelta(months=2)
    else:
        analog_start_default = current_date.replace(day=1) - relativedelta(months=5)
        analog_end_default = current_date.replace(day=2) - relativedelta(months=3)
    return analog_start_default, analog_end_default


# Set the analog end year to be the effectively-computed end year
analog_start_default, analog_end_default = get_default_analog_daterange()

analog_years = []
for i in range(1949, analog_end_default.year + 1):
    analog_years.append(i)

# This and next year.
forecast_years = []
for i in range(1949, datetime.now().year + 2):
    forecast_years.append(i)
