import base64
import urllib.parse

import requests
from flask import Flask, request, redirect, session

from config import settings


def create_app(settings_override=None):
    app = Flask(__name__)

    app.config.from_object("config.settings")

    if settings_override:
        app.config.update(settings_override)

    return app


app = create_app()


@app.get("/.well-known/webfinger")
def webfinger():
    resource = request.args.get("resource")
    return {
        "subject": resource,
        "links": [{
            "rel": "http://openid.net/specs/connect/1.0/issuer",
            "href": f"{settings.BASE_URL}/oauth2/openid/ocis"
        }]
    }


@app.get("/oauth2/openid/ocis/.well-known/openid-configuration")
def openid_configuration():
    r = requests.get(f"{settings.IDM_BASE_URL}/oauth2/openid/ocis/.well-known/openid-configuration")
    data = r.json()

    data["authorization_endpoint"] = f"{settings.BASE_URL}/ui/oauth2"
    data["token_endpoint"] = f"{settings.BASE_URL}/oauth2/token"

    return data


@app.get("/redirect-request")
def ui_oauth2():
    args = request.args.to_dict()

    session["original_redirect_uri"] = args["redirect_uri"]

    args['client_id'] = "ocis-desktop"
    args['redirect_uri'] = f"{settings.BASE_URL}/redirect-response"

    query = urllib.parse.urlencode(args)

    return redirect(f"{settings.IDM_BASE_URL}/ui/oauth2?{query}")


@app.get("/redirect-response")
def do_redirect():
    redirect_uri = session["original_redirect_uri"]
    args = request.args.to_dict()
    query = urllib.parse.urlencode(args)

    return redirect(f"{redirect_uri}?{query}")


@app.post("/oauth2/token")
def oauth2_token():
    form = request.form.to_dict()
    headers = dict(request.headers)

    if "redirect_uri" in form.keys() and ("localhost" in form["redirect_uri"] or "127.0.0.1" in form["redirect_uri"]):
        form["redirect_uri"] = f"{settings.BASE_URL}/redirect-response"
        headers["Authorization"] = b"Basic " + base64.b64encode(b"ocis-desktop:eDTxBa9aVQaCGPEkqQPUYf4vELWhqQpsP7pA8jpFrrryVcMG")
        headers["Host"] = "auth.alejandroavila.com"
        del headers["Content-Length"]

    resp = requests.post("https://localhost:8443/oauth2/token",
                         data=form,
                         headers=headers)

    return resp.content, resp.status_code, resp.headers.items()

