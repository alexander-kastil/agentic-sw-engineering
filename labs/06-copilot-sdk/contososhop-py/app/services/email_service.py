import logging

logger = logging.getLogger("contososhop.email")


class EmailServiceDev:
    async def send_email(self, to: str, subject: str, body: str) -> None:
        logger.info("EMAIL to %s | %s | %s", to, subject, body)
