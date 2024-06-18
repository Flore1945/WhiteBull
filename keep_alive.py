from flask import Flask
from threading import Thread
from flask import Flask, jsonify, request

app = Flask('')


@app.route('/')
def home():
  return 'Im in!'


@app.route('/update', methods=['POST'])
def update():
  if request.method == 'POST':
    type = request.headers.get('type')
    if type == "ip_modification":
      mod = request.json.get('mod')
      with open('ip.txt', 'w') as f:
        f.write(mod)
      return f"Updated IP in ip.txt to: {mod}", 200
    # elif type == "code_modification":
    #   mod = request.json.get('mod')

    #   # status = open('isUpdating.txt', 'r').read().strip() if open(
    #   #   'isUpdating.txt', 'r').read().strip() else None

    #   with open('code.txt', 'w') as f:
    #     f.write(mod)

    #   return f"Updated CODE in code.txt", 200
    else:
      return "Invalid request type", 400
  else:
    return "Method not allowed", 405


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  '''
  Creates and starts new thread that runs the function run.
  '''
  t = Thread(target=run)
  t.start()
