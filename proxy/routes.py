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

    return redirect(f"{settings.IDM_BASE_URL}/api/oidc/authorization?{query}")


@api.post("/api/oidc/token")
def oidc_token():
    headers = dict(request.headers)

    form = request.form.to_dict()
    form["scopes"] = "openid offline_access email profile groups"

    resp = requests.post(f"{settings.IDM_INTERNAL_SERVER_URL}/oauth2/token",
                         data=form,
                         headers=headers)

    return resp.content, resp.status_code, resp.headers.items()

