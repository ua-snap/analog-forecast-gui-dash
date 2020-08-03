# pylint: disable=C0103
"""
Common shared text strings and lookup tables.
"""
import os
from datetime import date

title = "Experimental Analog Forecast Tool"
url = "http://snap.uaf.edu/tools/demo"
preview = "http://snap.uaf.edu/tools/demo/assets/preview.png"
description = "Run an analog forecast tool to see future forecasts from past data."

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
    "SLP": 1,
    "Pressure level height": 2,
    "2-meter temps": 3,
    "Pressure level temp": 4,
    "SST": 5,
    "Precip": 6,
}

correlations = {
    "No": 0,
    "R-Value Maps": 1,
    "R2-Value Maps": 2,
    "Multiple R Correlation": 3,
}

# Selection for manual weighting
# TODO: x-ref `forecast_themes` to keep text aligned
# idx refers to the number that is postfixed to the control
# to get a unique element ID to process for the API
manual_weights = {
    "SLP": dict(default=100, idx=1),
    "Pressure level height": dict(default=0, idx=2),
    "2-meter temps": dict(default=0, idx=3),
    "Pressure level temp": dict(default=0, idx=4),
    "SST": dict(default=0, idx=5),
}
