# Analog Forecast GUI App

## Structure

 * `application.py` contains the main app loop code.
 * `gui.py` has most user interface elements.
 * `luts.py` has shared code & lookup tables and other configuration.
 * `assets/` has images and CSS (uses [Bulma](https://bulma.io))

## Local development

After cloning this template, run it this way:

```
pipenv install
export FLASK_APP=application.py
export FLASK_DEBUG=True
export EAPI_API_URL=http://localhost:3000
pipenv run flask run
```

The project is run through Flask and will be available at [http://localhost:5000](http://localhost:5000).

Env vars which must be set:

 * `EAPI_API_URL` - URL for API.

## Deploying to AWS Elastic Beanstalk:

Apps run via WSGI containers on AWS.

Before deploying, make sure and run `pipenv run pip freeze > requirements.txt` to lock current versions of everything.

```
eb init
eb deploy
```

The following env vars must be set:

 * `REQUESTS_PATHNAME_PREFIX` - URL fragment so requests are properly routed.
 * `GTAG_ID` - Google Tag Manager ID

For local development, set `FLASK_DEBUG` to `True`.  This will use a local file for source data and enable other debugging tools.