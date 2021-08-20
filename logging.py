class Logger:
  name = ""
  infoLogTemplate = "\x1b[0;36;40m[{}/INFO] {}"
  def __init__(this, name):
    this.name = name
  def info(this, message)