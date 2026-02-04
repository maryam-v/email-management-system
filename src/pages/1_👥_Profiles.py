import streamlit as st

from utils.db import DatabaseManager

db = DatabaseManager()


def main():
    st.title("👥 Profiles")
    st.caption("Add team members, then use them as recipients across the app.")
    st.divider()

    st.info(
        "Save names, emails, titles, and professions. These profiles appear in recipient pickers on "
        "the Send Email page.",
        icon="ℹ️",
    )

    with st.container(border=True):
        st.subheader("Add New Profile")
        with st.form("add_profile_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name", placeholder="Ada Lovelace")
                email = st.text_input("Email", placeholder="ada@example.com")
            with col2:
                title = st.text_input("Title", placeholder="Research Lead")
                profession = st.text_input("Profession", placeholder="Software Engineer")

            submitted = st.form_submit_button("➕ Add Profile", use_container_width=True)

            if submitted:
                if name and email and title and profession:
                    db.add_profile(name, email, title, profession)
                    st.success("Profile added successfully")
                    st.rerun()
                else:
                    st.error("Please fill in all fields")

    st.divider()
    st.subheader("Existing Profiles")
    profiles = db.get_all_profiles()

    if not profiles:
        st.info("No profiles yet. Add a profile above to get started.")
    else:
        for profile in profiles:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{profile['name']}**")
                    st.markdown(f"{profile['email']}")
                    st.caption(f"{profile['title']} · {profile['profession']}")
                with col2:
                    st.caption(f"ID: {profile.doc_id}")
                    if st.button("🗑️ Delete", key=f"delete_{profile.doc_id}", use_container_width=True):
                        db.delete_profile(profile.doc_id)
                        st.success("Profile deleted")
                        st.rerun()


if __name__ == "__main__":
    main()