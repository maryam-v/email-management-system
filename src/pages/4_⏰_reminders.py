
import streamlit as st
from datetime import datetime

from utils.db import DatabaseManager

db = DatabaseManager()


def main():
    st.title("⏰ Reminders")
    st.caption("View and manage your email reminders.")
    st.divider()

    reminders = db.get_all_reminders()

    if not reminders:
        st.info("No reminders set yet. Add some from the Send Email page.", icon="ℹ️")
        return

    st.subheader("Upcoming Reminders")

    for reminder in reminders:
        email = db.get_sent_email(reminder['email_id'])
        if not email:
            continue  # Skip if email not found

        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"**{email['subject']}**")
                due_date = datetime.fromisoformat(reminder['reminder_date']).strftime('%Y-%m-%d %H:%M')
                st.caption(f"Due: {due_date}")
                st.caption(f"Recipients: {', '.join(email['recipients'])}")

            with col2:
                if st.button("Mark Done", key=f"done_{reminder.doc_id}", use_container_width=True):
                    db.delete_reminder(reminder.doc_id)
                    st.success("Reminder marked as done!")
                    st.rerun()

            with col3:
                if st.button("Delete", key=f"delete_{reminder.doc_id}", use_container_width=True):
                    db.delete_reminder(reminder.doc_id)
                    st.success("Reminder deleted!")
                    st.rerun()


if __name__ == "__main__":
    main()