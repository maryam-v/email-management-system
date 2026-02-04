from datetime import datetime, time, timedelta

import streamlit as st

from utils.db import DatabaseManager

from utils.helpers import send_email

db = DatabaseManager()


def main():
    st.title("📧 Send Email")
    st.caption("Compose, schedule, and set reminders with a live preview.")
    st.divider()

    # Preserve schedule inputs across reruns so users can change the time/date without it snapping back
    if "schedule_date" not in st.session_state:
        st.session_state["schedule_date"] = datetime.now().date()
    if "schedule_time" not in st.session_state:
        st.session_state["schedule_time"] = time(hour=datetime.now().hour, minute=datetime.now().minute)

    profiles = db.get_all_profiles()
    templates = db.get_all_templates()

    st.info(
        "Select recipients, pick a template, optionally add your signature, then choose Send Now, "
        "Schedule, or Add Reminder.",
        icon="ℹ️",
    )

    with st.container(border=True):
        st.subheader("Recipients & Template")
        col_left, col_right = st.columns([1.4, 1])

        with col_left:
            selected_profiles = st.multiselect(
                "Select Recipients",
                options=[p["name"] for p in profiles],
                format_func=lambda x: f"{x} ({next(p['email'] for p in profiles if p['name'] == x)})",
                placeholder="Choose one or more contacts…",
                help="You can select multiple recipients.",
            )
            st.caption(f"Selected: {len(selected_profiles)} • Total profiles: {len(profiles)}")

        with col_right:
            selected_template = st.selectbox(
                "Select Template",
                options=[t["name"] for t in templates],
                format_func=lambda x: x,
                index=0 if templates else None,
                placeholder="Pick a template…",
                help="Use a saved template to fill the email body.",
            )
            add_signature = st.toggle("Add Signature", help="Append your saved signature to the email.")

    template_body = next((t["body"] for t in templates if t["name"] == selected_template), "")

    user_profile = db.get_user_profile()
    signature = user_profile.get("signature", "") if user_profile else ""

    st.divider()
    st.subheader("Content & Preview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Raw Email Body**")
        st.text_area(
            "Edit the raw body if needed",
            value=template_body,
            height=320,
            key="raw_email",
            label_visibility="collapsed",
        )

    with col2:
        st.markdown("**Live Preview**")
        preview_body = template_body
        if add_signature:
            preview_body += f"\n\n{signature}"
        st.text_area(
            "Rendered preview",
            value=preview_body,
            height=320,
            key="preview email",
            label_visibility="collapsed",
        )

    st.divider()
    st.subheader("Actions")
    can_send = bool(selected_profiles and selected_template)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🚀 Send Now", use_container_width=True, disabled=not can_send):
            if can_send:
                errors = []
                for profile in selected_profiles:
                    recipient_email = next(p["email"] for p in profiles if p["name"] == profile)
                    subject = f"Email to {profile}"
                    success = send_email(
                        to=[recipient_email],
                        subject=subject,
                        contents=preview_body
                    )
                    if success:
                        email_id = db.add_sent_email(
                            [recipient_email], f"Email to {profile}", preview_body, datetime.now()
                        )
                        db.add_schedule(email_id, datetime.now())
                    else:
                        errors.append(recipient_email)
                if errors:
                    st.error("Failed to send to: {', '.join(errors)}")
                else: 
                    st.success("Emails sent successfully")
            else:
                st.error("Please select at least one recipient and a template")

    with col2:
        schedule_date = st.date_input(
            "Schedule Date",
            key="schedule_date",
            min_value=datetime.now().date(),
            help="Pick the date to send.",
        )
        schedule_time = st.time_input(
            "Schedule Time",
            key="schedule_time",
            value=st.session_state["schedule_time"],
            step=timedelta(minutes=5),
            help="Pick the time to send.",
        )
        if st.button("🗓️ Schedule", use_container_width=True, disabled=not can_send):
            if can_send:
                schedule_datetime = datetime.combine(schedule_date, schedule_time)
                for profile in selected_profiles:
                    recipient_email = next(p["email"] for p in profiles if p["name"] == profile)
                    email_id = db.add_sent_email(
                        [recipient_email], f"Email to {profile}", preview_body, schedule_datetime
                    )
                    db.add_schedule(email_id, schedule_datetime)
                st.success(f"Emails scheduled for {schedule_datetime}")
            else:
                st.error("Please select at least one recipient and a template")

    with col3:
        reminder_days = st.number_input(
            "Reminder (days from now)",
            min_value=1,
            value=3,
            step=1,
            help="Create a reminder after this many days.",
        )
        if st.button("⏰ Add Reminder", use_container_width=True, disabled=not can_send):
            if can_send:
                reminder_date = datetime.now() + timedelta(days=reminder_days)
                for profile in selected_profiles:
                    recipient_email = next(p["email"] for p in profiles if p["name"] == profile)
                    email_id = db.add_sent_email(
                        [recipient_email], f"Email to {profile}", preview_body, datetime.now()
                    )
                    db.add_reminder(email_id, reminder_date)
                st.success(f"Reminders set for {reminder_date}")
            else:
                st.error("Please select at least one recipient and a template")


if __name__ == "__main__":
    main()
