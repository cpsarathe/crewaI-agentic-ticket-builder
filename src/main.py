from dotenv import load_dotenv
 
from src.crew.app_review_crew import build_crew
from src.logging_utils import setup_logging, get_logger
 

logger = get_logger(__name__)
 
def main():
    setup_logging()
    load_dotenv()
    logger.info("main started")
    try:
        crew = build_crew()
        result = crew.kickoff()
        logger.info("crew kickoff finished")
        logger.info(str(result))
        return result
    except Exception:
        logger.exception("crew kickoff failed")
        raise
 
 
if __name__ == "__main__":
     main()
