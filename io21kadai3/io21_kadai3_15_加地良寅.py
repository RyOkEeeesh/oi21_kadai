from flask import Flask, request, jsonify
from flask_cors import CORS
import RPi.GPIO as GPIO

class status:
  def __init__(self):
    self.working = False
    self.status = None
    self.port = [13, 19, 26]
  def	setstatus(self, s):
    self.status = s
  def	getstatus(self):
    return self.status
  def changeWorkStatus(self, bool):
    self.working = bool

c = status()
app = Flask(__name__)
CORS(app)
GPIO.setmode(GPIO.BCM)
GPIO.setup(c.port, GPIO.OUT, initial=GPIO.LOW)

@app.route('/api/echo', methods=['POST'])
def echo():
  data = request.json
  status = int(data.get('status', ''))

  if (status == 4 and not(c.working)):
    c.setstatus(status)
  elif status != c.status and status >= 0 and status < 4:
    GPIO.output(c.port, GPIO.LOW)
    c.setstatus(status)
    c.changeWorkStatus(True)
    if c.status != 3: GPIO.output(c.port[c.status], GPIO.HIGH)

  return jsonify({'status': c.status})


if __name__ == '__main__':
  try:
    app.run(host='0.0.0.0', port=5000)
  except KeyboardInterrupt:
    pass
  finally:
    GPIO.cleanup()
