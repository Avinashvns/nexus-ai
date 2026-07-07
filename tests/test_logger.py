from core.logger import app_logger


def main():
    app_logger.info("Nexus AI Started")
    app_logger.warning("Logger Working")
    app_logger.error("Test Error")


if __name__ == "__main__":
    main()