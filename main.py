from sanic import Sanic
from sanic.response import json
from password_generator import PasswordGenerator

app = Sanic("hello_example")
app.config.from_pyfile('generator.conf')

@app.route("/generate_password", version=1)
async def generate(request):
  pwo = PasswordGenerator()
  chars_allowed = app.config.CHARS_ALLOWED
  
  if 'chars_count' in request.args and request.args['chars_count'][0]:
      chars_count = app.config.CHARS_COUNT if int(request.args['chars_count'][0]) == 0 else int(request.args['chars_count'][0])
  else:
      chars_count = app.config.CHARS_COUNT
  newpass = pwo.shuffle_password(chars_allowed, chars_count)
  return json({"password": newpass, "chars_count": chars_count})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)