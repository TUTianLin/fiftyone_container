class bcolors:
  DEBUG = "\033[92m"
  WARN = "\033[93m"
  ERR = "\033[91m"
  ENDC = "\033[0m"

class log:
  @staticmethod
  def debug(msg: str):
    print(bcolors.DEBUG + f"{msg}" + bcolors.ENDC)

  @staticmethod
  def info(msg: str):
    print(f"{msg}")

  @staticmethod
  def warn(msg: str):
    print(bcolors.WARN + f"{msg}" + bcolors.ENDC)

  @staticmethod
  def err(msg: str):
    print(bcolors.ERR + f"{msg}" + bcolors.ENDC)