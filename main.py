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
  return jinja.render("index.html", request, api_url=api_url, policies=app.config.POLICY)

@app.route("/generate_password", version=1)
async def generate(request):
  pwo = PasswordGenerator()

  # Получаем политику, если передали в запросе
  if 'policy' in request.args and request.args['policy'][0]:
    if request.args['policy'][0].upper() in app.config.POLICY:
      # Есть в списке, выбираем ее
      policy = request.args['policy'][0].upper()
    else:
      # Не нашли, выбираем политику по-умолчанию
      policy = 'DEFAULT'
  else:
    # Политику не передали, выбираем политику по-умолчанию
    policy = 'DEFAULT'

  # Получаем список символов, которые нужно избегать при генерации пароля
  # Большие буквы
  if 'excludeuchars' in request.args and request.args['excludeuchars'][0]:
    excludeuchars = request.args['excludeuchars'][0]
  else:
    # Не переданы, берем из выбранной политики
    excludeuchars = app.config.POLICY[policy]['excludeuchars']
  
  # Маленькие буквы
  if 'excludelchars' in request.args and request.args['excludelchars'][0]:
    excludelchars = request.args['excludelchars'][0]
  else:
    # Не переданы, берем из выбранной политики
    excludelchars = app.config.POLICY[policy]['excludelchars']
  
  # Цифры
  if 'excludenumbers' in request.args and request.args['excludenumbers'][0]:
    excludenumbers = request.args['excludenumbers'][0]
  else:
    # Не переданы, берем из выбранной политики
    excludenumbers = app.config.POLICY[policy]['excludenumbers']
  
  # Специальные символы
  if 'excludeschars' in request.args and request.args['excludeschars'][0]:
    excludeschars = request.args['excludeschars'][0]
  else:
    # Не переданы, берем из выбранной политики
    excludeschars = app.config.POLICY[policy]['excludeschars']

  # Проверяем, если не указана минимальная длина пароля
  if 'minlen' in request.args and request.args['minlen'][0]:
    minlen = int(request.args['minlen'][0]) if int(request.args['minlen'][0]) > 0 else int(app.config.POLICY[policy]['minlen'])
  else:
    # Не указана, берем из выбранной политики
    minlen = int(app.config.POLICY[policy]['minlen'])
  
  # Проверяем, если не указана максимальная длина пароля
  if 'maxlen' in request.args and request.args['maxlen'][0]:
    maxlen = int(request.args['maxlen'][0]) if int(request.args['maxlen'][0]) > 0 else int(app.config.POLICY[policy]['maxlen'])
  else:
    # Не указана, берем из выбранной политики
    maxlen = int(app.config.POLICY[policy]['maxlen'])
  
  # Если минимальная длина пароля больше максимальной, тогда приравниваем их
  if minlen > maxlen:
    maxlen = minlen

  # Проверяем, если не указано минимальное число прописных символов в пароле
  if 'minuchars' in request.args and request.args['minuchars'][0]:
    minuchars = int(request.args['minuchars'][0])
  else:
    # Не указана, берем из выбранной политики
    minuchars = int(app.config.POLICY[policy]['minuchars'])

  # Проверяем, если не указано минимальное число строчных символов в пароле
  if 'minlchars' in request.args and request.args['minlchars'][0]:
    minlchars = int(request.args['minlchars'][0])
  else:
    # Не указана, берем из выбранной политики
    minlchars = int(app.config.POLICY[policy]['minlchars'])
  
  # Проверяем, если не указано минимальное число цифр в пароле
  if 'minnumbers' in request.args and request.args['minnumbers'][0]:
    minnumbers = int(request.args['minnumbers'][0])
  else:
    # Не указана, берем из выбранной политики
    minnumbers = int(app.config.POLICY[policy]['minnumbers'])

  # Проверяем, если не указано минимальное число специальных символов в пароле
  if 'minschars' in request.args and request.args['minschars'][0]:
    minschars = int(request.args['minschars'][0])
  else:
    # Не указана, берем из выбранной политики
    minschars = int(app.config.POLICY[policy]['minschars'])

  ret = {}
  # Генерируем пароль
  try:
    pwo.minlen = minlen
    pwo.maxlen = maxlen
    pwo.minuchars = minuchars
    pwo.minlchars = minlchars
    pwo.minnumbers = minnumbers
    pwo.minschars = minschars
    pwo.excludelchars = excludelchars
    pwo.excludeuchars = excludeuchars
    pwo.excludenumbers = excludenumbers
    pwo.excludeschars = excludeschars

    newpass = pwo.generate()
    ret = {'status': 'success', 'password': newpass, "policy": policy, 'length': len(newpass)}
  except ValueError as e:
    ret = {'status': 'fail', 'password': '', "policy": policy, 'error': e}
  return json(ret)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)