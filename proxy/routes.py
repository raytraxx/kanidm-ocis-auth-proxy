import urllib.parse

import requests
from flask import request, Blueprint, redirect

from config import settings

api = Blueprint('api', __name__)


@api.get("/api/oidc/authorization")
def ui_oauth2():
    args = request.args.to_dict()
    args['scope'] = "openid offline_access email profile groups"
    args.pop('prompt', None)

    query = urllib.parse.urlencode(args)

    print(query)

    return redirect(f"{settings.IDM_BASE_URL}/api/oidc/authorization?{query}")


@api.post("/api/oidc/token")
def oidc_token():
    headers = dict(request.headers)
    headers["User-Agent"] = "Python/Requests"

    form = request.form.to_dict()
    form["scope"] = "openid offline_access email profile groups"

    resp = requests.post(f"{settings.IDM_BASE_URL}/api/oidc/token",
                         data=form,
                         headers=headers)

    print(resp.content, resp.status_code, resp.headers.items())

    return resp.content, resp.status_code, resp.headers.items()

