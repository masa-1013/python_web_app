import textwrap
import urllib.parse
from datetime import datetime
from pprint import pformat

from henango.http.request import HTTPRequest
from henango.http.response import HTTPResponse
from henango.template.renderer import render

def now(request: HTTPRequest) -> HTTPResponse:
  context = {"now": datetime.now()}
  body = render("now.html", context)

  return HTTPResponse(body=body)

def show_request(request: HTTPRequest) -> HTTPResponse:
  context = {"request": request, "headers": pformat(request.headers), "body": request.body.decode("utf-8", "ignore")}
  body = render("show_request.html", context)

  return HTTPResponse(body=body)

def parameters(request: HTTPRequest) -> HTTPResponse:
  if request.method == "GET":
    body = b"<html><body><h1>405 Method Not Allowed</h1></body></html>"
    status_code = 405

    return HTTPResponse(body=body, status_code=status_code)

  elif request.method == "POST":
    context = {"params": urllib.parse.parse_qs(request.body.decode())}
    body = render("parameters.html", context)
  
    return HTTPResponse(body=body)

def user_profile(request: HTTPRequest) -> HTTPResponse:
  context = {"user_id": request.params["user_id"]}
  body = render("user_profile.html", context)

  return HTTPResponse(body=body)


