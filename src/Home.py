import streamlit as st

from dotenv import load_dotenv 
load_dotenv()

st.set_page_config(page_title="Email Management System", page_icon="🏠", layout="wide")


def main():
    st.title("🏠 Email Management System")
    st.caption("Quick glance at your outreach, templates, and reminders.")
    st.divider()

    hero_left, hero_right = st.columns([1.2, 1])
    with hero_left:
        st.subheader("Today")
        col1, col2, col3 = st.columns(3)
        col1.metric("Emails Sent", "50", "+3 vs yesterday")
        col2.metric("Open Rate", "75%", "↑ 4%")
        col3.metric("Response Rate", "40%", "↑ 2%")
        st.write("Manage recipients, templates, schedules, and reminders from the sidebar pages.")
    with hero_right:
        st.image(
            "https://cdn.intheloop.io/blog/wp-content/uploads/2019/03/loop-email-shared-inbox-feature.jpg",
            width=600,
        )

    st.divider()
    st.subheader("Quick Actions")
    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        if st.button("📧 Compose & Send", use_container_width=True):
            st.switch_page("pages/3_📧_Send_Emails.py")
        st.caption("Go to Send Email page to send or schedule messages.")
    with qa2:
        if st.button("📄 Manage Templates", use_container_width=True):
            st.switch_page("pages/2_📄_Email_Templates.py")
        st.caption("Create or edit reusable templates.")
    with qa3:
        if st.button("👥 Manage Profiles", use_container_width=True):
            st.switch_page("pages/1_👥_Profiles.py")
        st.caption("Add recipients with names, emails, titles, and professions.")

    st.divider()
    st.subheader("Recent Emails")
    st.table(
        {
            "Recipient": ["John Doe", "Jane Smith", "Alex Lee"],
            "Subject": ["Meeting tomorrow", "Project update", "Follow-up"],
            "Date": ["2026-01-15", "2026-01-22", "2026-01-24"],
        }
    )


if __name__ == "__main__":
    main()
