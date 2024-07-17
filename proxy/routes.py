import base64
import urllib.parse

import requests
from flask import request, redirect, session, Blueprint

from config import settings


api = Blueprint('api', __name__)


@api.get("/redirect-request")
def ui_oauth2():
    args = request.args.to_dict()

    session["original_redirect_uri"] = args["redirect_uri"]

    args['client_id'] = settings.CLIENT_ID
    args['redirect_uri'] = f"{settings.BASE_URL}/redirect-response"

    query = urllib.parse.urlencode(args)

    return redirect(f"{settings.IDM_BASE_URL}/ui/oauth2?{query}")


@api.get("/redirect-response")
def do_redirect():
    redirect_uri = session["original_redirect_uri"]
    args = request.args.to_dict()
    query = urllib.parse.urlencode(args)

    return redirect(f"{redirect_uri}?{query}")


@api.post("/oauth2/token")
def oauth2_token():
    form = request.form.to_dict()
    headers = dict(request.headers)

    if "redirect_uri" in form.keys() and ("localhost" in form["redirect_uri"] or "127.0.0.1" in form["redirect_uri"]):
        auth_value = bytes(f"{settings.CLIENT_ID}:{settings.CLIENT_SECRET}", encoding="utf-8")
        headers["Authorization"] = b"Basic " + base64.b64encode(auth_value)

        form["redirect_uri"] = f"{settings.BASE_URL}/redirect-response"
        headers["Host"] = "auth.alejandroavila.com"

        del headers["Content-Length"]

    resp = requests.post("https://localhost:8443/oauth2/token",
                         data=form,
                         headers=headers,
                         verify=False)

    return resp.content, resp.status_code, resp.headers.items()

