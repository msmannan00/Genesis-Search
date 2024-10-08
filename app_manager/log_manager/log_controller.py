import datetime
import inspect
import stat
import sys
import logging
import os
from termcolor import colored

if sys.platform == "win32":
  os.system('color')


class log:
  __server_instance = None

  def __configure_logs(self):
    self.__server_instance = logging.getLogger('genesis_logs')
    self.__server_instance.setLevel(logging.DEBUG)

    # File handler for logging to a file
    log_filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    log_filepath = os.path.join(os.path.join(os.getcwd(), 'logs'), log_filename)
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(logging.DEBUG)

    # Console handler for logging to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    self.__server_instance.addHandler(file_handler)
    self.__server_instance.addHandler(console_handler)

    self.__server_instance.propagate = False

  @staticmethod
  def g():
    if log.__server_instance is None:
      log()
    return log.__server_instance

  def __init__(self):
    log.__server_instance = self
    self.__configure_logs()

  def get_caller_info(self):
    frame = inspect.currentframe()
    while frame:
      frame = frame.f_back
      if frame:
        caller_class = frame.f_locals.get("self", None)
        if caller_class and caller_class.__class__.__name__ != self.__class__.__name__:
          caller_class = caller_class.__class__.__name__
          caller_file = os.path.abspath(frame.f_code.co_filename)
          caller_line = frame.f_lineno
          return caller_class, caller_file, caller_line
        elif not caller_class:
          caller_file = os.path.abspath(frame.f_code.co_filename)
          caller_line = frame.f_lineno
          return "Function", caller_file, caller_line
    return "Unknown", "Unknown", 0

  def __write_to_file(self, log_message):
    caller_class, caller_file, caller_line = self.get_caller_info()
    log_filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    log_filepath = os.path.join(os.path.join(os.getcwd(), 'logs'), log_filename)
    with open(log_filepath, 'a') as log_file:
      full_log_message = f"{log_message} - {caller_class} ({caller_file}:{caller_line})"
      log_file.write(full_log_message + "\n")
    os.chmod(log_filepath, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    with open(log_filepath, 'a') as log_file:
      full_log_message = f"{log_message} - {caller_class} ({caller_file}:{caller_line})"
      log_file.write(full_log_message + "\n")

  def __format_log_message(self, log_type, p_log, include_caller=False):
    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if include_caller:
      caller_class, caller_file, caller_line = self.get_caller_info()
      formatted_log = f"{log_type} - {current_time} : {p_log} - {caller_class} ({caller_file}:{caller_line})"
    else:
      formatted_log = f"{log_type} - {current_time} : {p_log}"
    return formatted_log

  def i(self, p_log):
    try:
      console_log = self.__format_log_message("INFO", p_log)
      self.__server_instance.info(console_log)
      self.__write_to_file(console_log)
      print(colored(console_log, 'cyan', attrs=['bold']))
    except Exception:
      pass

  def s(self, p_log):
    try:
      console_log = self.__format_log_message("SUCCESS", p_log)
      self.__server_instance.info(console_log)
      self.__write_to_file(console_log)
      print(colored(console_log, 'green'))
    except Exception:
      pass

  def w(self, p_log):
    try:
      console_log = self.__format_log_message("WARNING", p_log)
      self.__server_instance.warning(console_log)
      self.__write_to_file(console_log)
      print(colored(console_log, 'yellow'))
    except Exception:
      pass

  def e(self, p_log):
    try:
      console_log = self.__format_log_message("ERROR", p_log)
      self.__server_instance.error(console_log)
      self.__write_to_file(console_log)
      print(colored(console_log, 'blue'))
    except Exception:
      pass

  def c(self, p_log):
    try:
      console_log = self.__format_log_message("CRITICAL", p_log)
      self.__server_instance.critical(console_log)
      self.__write_to_file(console_log)
      print(colored(console_log, 'red'))
    except Exception:
      pass
