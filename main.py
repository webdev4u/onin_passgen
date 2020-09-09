from sanic import Sanic, response
from sanic.response import json
from password_generator import PasswordGenerator
from sanic_jinja2 import SanicJinja2

app = Sanic("OnIn Password Generator")
app.config.from_pyfile('generator.conf')
app.static('/static', './static')
jinja = SanicJinja2(app, pkg_name="main")

@app.route("/")
async def instructions(request):
  api_url = app.url_for('generate')
  return jinja.render("index.html", request, api_url=api_url)

@app.route("/generate_password", version=1)
async def generate(request):
  pwo = PasswordGenerator()

  if 'policy' in request.args and request.args['policy'][0]:
    if request.args['policy'][0].upper() in app.config.POLICY:
      policy = request.args['policy'][0].upper()
    else:
      policy = 'DEFAULT'
  else:
    policy = 'DEFAULT'
  chars_allowed = app.config.POLICY[policy]['CHARS_ALLOWED']
  
  if 'chars_count' in request.args and request.args['chars_count'][0]:
      chars_count = app.config.POLICY[policy]['CHARS_COUNT'] if int(request.args['chars_count'][0]) == 0 else int(request.args['chars_count'][0])
  else:
      chars_count = app.config.POLICY[policy]['CHARS_COUNT']
  
  ret = {}
  try:
    newpass = pwo.shuffle_password(chars_allowed, chars_count)
    ret = {'status': 'success', 'password': newpass, "policy": policy}
  except ValueError as e:
    ret = {'status': 'fail', 'password': '', "policy": policy, 'error': e}
  return json(ret)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)