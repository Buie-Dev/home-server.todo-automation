import time
import logging
from datetime import datetime, timedelta

import requests

from config import config
from mqtt import run_mqtt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def seconds_until_next_1am():
    now = datetime.now()
    target = now.replace(hour=1, minute=0, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    return (target - now).total_seconds()


def run_automation():
    try:
        response = requests.post(f"{config.API_URL}/todo/automation", timeout=30)
        response.raise_for_status()
        data = response.json()
        logger.info("Automation complete — %d task(s) added", data.get("added", 0))
    except Exception as e:
        logger.error("Automation failed: %s", e)


if __name__ == "__main__":
    logger.info("Todo automation service started")
    run_mqtt()
    while True:
        wait = seconds_until_next_1am()
        next_run = datetime.now() + timedelta(seconds=wait)
        logger.info("Next run at %s (%ds)", next_run.strftime("%Y-%m-%d %H:%M:%S"), int(wait))
        time.sleep(wait)
        run_automation()
