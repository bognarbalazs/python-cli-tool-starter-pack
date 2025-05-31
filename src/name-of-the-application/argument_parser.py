import argparse
from datetime import datetime

def parser_arguments():
  """
  Parse command line arguments for the script.

  Returns:
      argparse.Namespace: Parsed command line arguments.
  """
  parser = argparse.ArgumentParser(
    prog="name-of-the-application",
    description="Description",
  )
  parser.add_argument("-v", "--verbose", help="Print debug logs. Overrides --quiet",action="store_true")
  parser.add_argument("-q", "--quiet", help="Do not print info logs.", action="store_true")
  parser.add_argument("-ltf", "--log-to-file", help="Print logs to file.", action="store_true")
  parser.add_argument("-lfp", "--log-file-path", help="Path of the log file",default=f"terminal_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log")

  return parser.parse_args()