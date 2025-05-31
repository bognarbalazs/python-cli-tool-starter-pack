import os
from check_duplicated_envs import logger
import sys

def validate_config(config: dict) -> list:
    """
    Check that the listed env variables exist.

    Returns:
        list: List of values with None values
    """
    null_keys = []
    for key in config.keys():
        if config.get(key) is None:
            null_keys.append(key)
    if len(null_keys) > 0:
      raise ValueError(f"Missing required parameters: {', '.join(null_keys)}") 
    else:
      logger.info("Configuration validation successful")
      return []


try:
    mr_config = {
      "ENV1": os.environ.get("ENV1"),
      "ENV2": os.environ.get("ENV2"),
    }
    validate_config(mr_config)


except Exception as e:
    logger.exception(f"Error validating config: {e}")
    sys.exit(1)