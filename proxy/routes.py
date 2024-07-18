import base64
import urllib.parse

import requests
from flask import request, redirect, session, Blueprint

from config import settings

api = Blueprint('api', __name__)


@api.get("/oauth2/openid/ocis/.well-known/openid-configuration")
def openid_configuration():
    r = requests.get(f"https://localhost:8443/oauth2/openid/ocis/.well-known/openid-configuration", verify=False)
    data = r.json()

    data["jwks_uri"] = f"https://auth.alejandroavila.com/oauth2/openid/{settings.CLIENT_ID}/public_key.jwk"
    data["userinfo_endpoint"] = f"https://auth.alejandroavila.com/oauth2/openid/{settings.CLIENT_ID}/userinfo"

    return data


@api.get(f"/oauth2/openid/{settings.CLIENT_ID}/public_key.jwk")
def public_keys():
    key1 = requests.get(f"https://localhost:8443/oauth2/openid/ocis/public_key.jwk", verify=False).json()
    key2 = requests.get(f"https://localhost:8443/oauth2/openid/{settings.CLIENT_ID}/public_key.jwk",
                        verify=False).json()

    return {
        "keys": key1["keys"] + key2["keys"],
    }


@api.get("/oauth2/openid/ocis/userinfo")
def userinfo():
    headers = dict(request.headers)

    resp = requests.get(f"https://localhost:8443/oauth2/openid/{settings.CLIENT_ID}/userinfo",
                        headers=headers,
                        verify=False)

    return resp.content, resp.status_code, resp.headers.items()


@api.get("/api/oidc/authorization")
def ui_oauth2():
    args = request.args.to_dict()
    args['scopes'] = "openid offline_access email profile groups"
    args.pop('prompt', None)

    query = urllib.parse.urlencode(args)

    resp = requests.get(f"https://localhost:8443/api/oidc/authorization?{query}", verify=False)

    return resp.content, resp.status_code, resp.headers.items()


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


@api.post("/api/oidc/token")
def oidc_token():
    headers = dict(request.headers)

    form = request.form.to_dict()
    form["scopes"] = "openid offline_access email profile groups"

    resp = requests.post("https://localhost:8443/oauth2/token",
                         data=form,
                         headers=headers,
                         verify=False)

    return resp.content, resp.status_code, resp.headers.items()

