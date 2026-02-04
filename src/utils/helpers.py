from __future__ import annotations

import os
from collections.abc import Iterable, Sequence

import yagmail
from loguru import logger


def send_email(
    to: str | Sequence[str],
    subject: str,
    contents: str | Iterable[str],
    attachments: str | Sequence[str] | None = None,
) -> bool:
    """
    Send an email using yagmail, with sender credentials from environment variables.

    Args:
        to: Recipient email or list of emails.
        subject: Email subject.
        contents: Email body or iterable of parts supported by yagmail.
        attachments: Optional file path or list of file paths to attach.

    Returns:
        True if the email was sent successfully, False otherwise.
    """
    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        logger.error("Sender email or password not found in environment variables")
        return False

    yag = None
    try:
        yag = yagmail.SMTP(sender_email, sender_password)
        yag.send(to=to, subject=subject, contents=contents, attachments=attachments)
        logger.success("Email sent successfully")
        return True
    except Exception as exc:
        logger.error(f"An error occurred while sending the email: {exc}")
        return False
    finally:
        if yag is not None:
            yag.close()
