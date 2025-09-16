import smbus
from time import sleep

i2c = smbus.SMBus(1)
addr = 0x3e
_command = 0x00
_data = 0x40


def command(code):
  i2c.write_byte_data(addr, _command, code)
  sleep(0.05)


def writeLCD(message):
  strlist = [ord(c) for c in message]
  maxDisLen = 16

  if len(strlist) == 0:
    command(0x01)
    return

  if len(strlist) < maxDisLen:
    strlist += [ord(' ')] * (maxDisLen - len(strlist))

  def display(displayText):
    command(0x80)
    for i in range(maxDisLen // 2):
      i2c.write_byte_data(addr, _data, displayText[i])

    command(0xC0)
    for i in range(maxDisLen // 2, maxDisLen):
      i2c.write_byte_data(addr, _data, displayText[i])

  if len(strlist) <= maxDisLen:
    display(strlist)
  else:
    # strlist += [ord(' ')] * 2
    # strlist += strlist
    # strlist += [ord(' ')] * maxDisLen
    for i in range(len(strlist) - maxDisLen + 1):
      display(strlist[i:i+maxDisLen])
      sleep(0.3)

def init():
  command(0x38)
  command(0x39)
  command(0x14)
  command(0x73)
  command(0x56)
  command(0x6c)
  sleep(0.1)
  command(0x38)
  command(0x0C)
  command(0x01)
  sleep(0.1)

if __name__ == "__main__":
  init()
  text = input("text : ")
  writeLCD(text)
