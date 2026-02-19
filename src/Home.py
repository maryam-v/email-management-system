from __future__ import annotations

"""App entrypoint and explicit sidebar navigation configuration."""

import streamlit as st
from dotenv import load_dotenv

from features.dashboard import compute_summary, daily_trend, load_sent_email_views, top_recipients
from utils.db import DatabaseManager

load_dotenv()

st.set_page_config(page_title="Email Management System", page_icon="🏠", layout="wide")


db = DatabaseManager()


def render_home() -> None:
    """Render Home analytics page using live sent-email records."""
    st.title("🏠 Email Management System")
    st.caption("Live overview of your sent-email activity.")
    st.divider()

    sent_views = load_sent_email_views(db)
    summary = compute_summary(sent_views)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Sent", f"{summary.total_sent}")
    k2.metric("Sent Today", f"{summary.sent_today}")
    k3.metric("Last 7 Days", f"{summary.sent_last_7_days}", f"{summary.week_delta:+d}")
    k4.metric("Unique Recipients", f"{summary.unique_recipients}")

    st.divider()

    left, right = st.columns([1.4, 1])
    with left:
        st.subheader("Daily Sent Trend (Last 14 Days)")
        trend_rows = daily_trend(sent_views, days=14)
        st.line_chart(
            {
                "date": [row["date"] for row in trend_rows],
                "sent_count": [row["sent_count"] for row in trend_rows],
            },
            x="date",
            y="sent_count",
            width="stretch",
        )

    with right:
        st.subheader("Top Recipients")
        top_rows = top_recipients(sent_views, limit=8)
        if not top_rows:
            st.info("No sent emails available yet.")
        else:
            st.table(
                {
                    "Recipient": [row[0] for row in top_rows],
                    "Count": [row[1] for row in top_rows],
                }
            )

    st.divider()
    st.subheader("Quick Actions")
    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        if st.button("📧 Compose & Send", width="stretch"):
            st.switch_page("pages/3_📧_Send_Emails.py")
    with qa2:
        if st.button("📄 Manage Templates", width="stretch"):
            st.switch_page("pages/2_📄_Email_Templates.py")
    with qa3:
        if st.button("👥 Manage Profiles", width="stretch"):
            st.switch_page("pages/1_👥_Profiles.py")

    st.divider()
    st.subheader("Recent Sent Emails")
    if not sent_views:
        st.info("No sent emails yet.")
    else:
        latest = sent_views[:20]
        st.dataframe(
            {
                "Email ID": [row.email_id for row in latest],
                "Subject": [row.subject for row in latest],
                "Recipients": [", ".join(row.recipients) if row.recipients else "N/A" for row in latest],
                "Sent At": [row.sent_at.strftime("%Y-%m-%d %H:%M") if row.sent_at else "Unknown" for row in latest],
                "Excerpt": [row.body_excerpt for row in latest],
            },
            width="stretch",
            hide_index=True,
        )


navigation = st.navigation(
    [
        st.Page(render_home, title="Home", icon="🏠", default=True),
        st.Page("pages/1_👥_Profiles.py", title="Profiles", icon="👥"),
        st.Page("pages/2_📄_Email_Templates.py", title="Email Templates", icon="📄"),
        st.Page("pages/3_📧_Send_Emails.py", title="Send Emails", icon="📧"),
        st.Page("pages/4_⏰_reminders.py", title="Reminders", icon="⏰"),
        st.Page("pages/5_📅_schedules.py", title="Schedules", icon="📅"),
        st.Page("pages/6_🔍_search.py", title="Search", icon="🔍"),
        st.Page("pages/7_🤖_email_chatbot.py", title="Email Chatbot", icon="🤖"),
        st.Page("pages/8_🙋‍♀️_user_profile.py", title="User Profile", icon="🙋‍♀️"),
    ]
)

navigation.run()
