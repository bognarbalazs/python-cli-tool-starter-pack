from .argument_parser import parser_arguments
from .log_setup import setup_logging


args = parser_arguments()

if args.verbose:
  log_level_name = "DEBUG"
elif args.quiet:
  log_level_name = "WARN"
else:
  log_level_name = "INFO"

logger = setup_logging(
    log_level_name=log_level_name,
    log_to_file=args.log_to_file,
    log_file_path=args.log_file_path,
)

from .config import mr_config
from .main import main