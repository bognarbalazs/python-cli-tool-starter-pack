from check_duplicated_envs import (
  args,
  logger)
import sys
        
def main():
  try:
    print("Starting the application...")
  except Exception as e:
    logger.exception(e)
    sys.exit(1)
    

if __name__ == "__main__":
  main()