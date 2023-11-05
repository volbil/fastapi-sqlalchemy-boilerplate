from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.database import sessionmanager
from app.settings import get_settings
from app.models import EmailMessage
from sqlalchemy import select
from datetime import datetime


# Note: This can (and probably should) be moved to settings
email_from = "Website Title <noreply@example.com>"

templates = {
    "activation": {
        "subject": "Account activation",
        "template": "https://example.com/activation/CONTENT",
    },
    "password_reset": {
        "subject": "Password reset",
        "template": "https://example.com/reset/CONTENT",
    },
}


async def send_email(session: AsyncSession, email: EmailMessage):
    email_subject = templates[email.type]["subject"]
    email_content = templates[email.type]["template"].replace(
        "CONTENT", email.content
    )

    # Note: Add email sending code here
    print(f"From: {email_from}")
    print(f"Subject: {email_subject}")
    print(f"Content: {email_content}")

    email.sent_time = datetime.utcnow()
    email.sent = True

    session.add(email)

    print(f"Sent email: {email.type}")


# This task responsible for fetching pending emails from database
# And processing them via send_email function
async def send_emails():
    settings = get_settings()

    sessionmanager.init(settings.database.endpoint)

    async with sessionmanager.session() as session:
        emails = await session.scalars(
            select(EmailMessage)
            .filter_by(sent=False)
            .options(selectinload(EmailMessage.user))
            .limit(100)
        )

        for email in emails:
            await send_email(session, email)

        await session.commit()

    await sessionmanager.close()
