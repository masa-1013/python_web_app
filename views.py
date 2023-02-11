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

def set_cookie(request: HTTPRequest) -> HTTPResponse:
  return HTTPResponse(headers={"Set-Cookie": "username=TARO"})

def login(request: HTTPRequest) -> HTTPResponse:
  if request.method == "GET":
    body = render("login.html", {})
    return HTTPResponse(body=body)
  
  elif request.method == "POST":
    post_params = urllib.parse.parse_qs(request.body.decode())
    user_name = post_params["username"][0]

    headers = {"Location": "/welcome", "Set-Cookie": f"username={user_name}"}
    return HTTPResponse(status_code=302, headers=headers)

def welcome(request: HTTPRequest) -> HTTPResponse:
  cookie_header = request.headers.get("Cookie", None)

  if not cookie_header:
    return HTTPResponse(status_code=302, headers={"Location": "/login"})

  cookie_strings = cookie_header.split("; ")

  cookies = {}
  for cookie_string in cookie_strings:
    name, value = cookie_string.split("=", maxsplit=1)
    cookies[name] = value

  if "username" not in cookies:
    return HTTPResponse(status_code=302, headers={"Location": "/login"})

  body = render("welcome.html", context={"username": cookies["username"]})

  return HTTPResponse(body=body)
