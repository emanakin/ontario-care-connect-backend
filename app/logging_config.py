import logging

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for more verbose output
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()          # Also output to console
    ]
)

# Get the logger instance
logger = logging.getLogger(__name__)
