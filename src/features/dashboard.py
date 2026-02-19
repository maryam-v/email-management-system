from __future__ import annotations

"""Dashboard analytics feature for sent-email reporting."""

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from utils.db import DatabaseManager


@dataclass(frozen=True)
class SentEmailView:
    """Normalized sent-email record used by dashboard and home pages."""

    email_id: int
    subject: str
    recipients: list[str]
    sent_at: datetime | None
    body_excerpt: str


@dataclass(frozen=True)
class DashboardSummary:
    """Aggregate KPIs shown in Home and Dashboard pages."""

    total_sent: int
    sent_today: int
    sent_last_7_days: int
    sent_previous_7_days: int
    week_delta: int
    unique_recipients: int


def _parse_iso_datetime(raw_value: str | None) -> datetime | None:
    if not raw_value:
        return None
    try:
        return datetime.fromisoformat(raw_value)
    except (TypeError, ValueError):
        return None


def _build_excerpt(text: str | None, max_chars: int = 160) -> str:
    if not text:
        return ""
    compact = " ".join(text.split())
    if len(compact) <= max_chars:
        return compact
    return f"{compact[: max_chars - 3]}..."


def _normalize_sent_emails(records: list[dict]) -> list[SentEmailView]:
    normalized: list[SentEmailView] = []
    for record in records:
        normalized.append(
            SentEmailView(
                email_id=record.doc_id,
                subject=str(record.get("subject", "(No subject)")),
                recipients=[str(item) for item in record.get("recipients", [])],
                sent_at=_parse_iso_datetime(record.get("sent_date")),
                body_excerpt=_build_excerpt(record.get("body", "")),
            )
        )
    return normalized


def load_sent_email_views(db: DatabaseManager) -> list[SentEmailView]:
    """Load and normalize sent emails, newest first."""
    views = _normalize_sent_emails(db.get_all_sent_emails())
    views.sort(key=lambda item: item.sent_at or datetime.min, reverse=True)
    return views


def compute_summary(views: list[SentEmailView], today: date | None = None) -> DashboardSummary:
    """Compute top-level KPIs from normalized sent-email records."""
    today = today or datetime.now().date()
    week_start = today - timedelta(days=6)
    prev_week_start = today - timedelta(days=13)
    prev_week_end = today - timedelta(days=7)

    sent_today = 0
    sent_last_7_days = 0
    sent_previous_7_days = 0
    recipients_set: set[str] = set()

    for item in views:
        for recipient in item.recipients:
            recipients_set.add(recipient.lower())
        if item.sent_at is None:
            continue
        sent_date = item.sent_at.date()
        if sent_date == today:
            sent_today += 1
        if week_start <= sent_date <= today:
            sent_last_7_days += 1
        if prev_week_start <= sent_date <= prev_week_end:
            sent_previous_7_days += 1

    return DashboardSummary(
        total_sent=len(views),
        sent_today=sent_today,
        sent_last_7_days=sent_last_7_days,
        sent_previous_7_days=sent_previous_7_days,
        week_delta=sent_last_7_days - sent_previous_7_days,
        unique_recipients=len(recipients_set),
    )


def top_recipients(views: list[SentEmailView], limit: int = 5) -> list[tuple[str, int]]:
    """Return top recipients by sent-email count."""
    counter: Counter[str] = Counter()
    for item in views:
        for recipient in item.recipients:
            counter[recipient] += 1
    return counter.most_common(limit)


def daily_trend(views: list[SentEmailView], days: int = 14, today: date | None = None) -> list[dict[str, int | str]]:
    """Build a daily sent count trend for the requested trailing window."""
    today = today or datetime.now().date()
    start_day = today - timedelta(days=days - 1)
    counts: dict[date, int] = defaultdict(int)

    for item in views:
        if item.sent_at is None:
            continue
        sent_day = item.sent_at.date()
        if start_day <= sent_day <= today:
            counts[sent_day] += 1

    trend: list[dict[str, int | str]] = []
    cursor = start_day
    while cursor <= today:
        trend.append({"date": cursor.isoformat(), "sent_count": counts.get(cursor, 0)})
        cursor += timedelta(days=1)
    return trend

