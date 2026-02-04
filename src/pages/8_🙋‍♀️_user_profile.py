import streamlit as st

from utils.db import DatabaseManager

db = DatabaseManager()


def main():
    st.title("🙋‍♀️ User Profile")

    user_profile = db.get_user_profile()

    with st.form("user_profile_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Name", value=user_profile.get("name", "") if user_profile else "")
            degree = st.text_input(
                "Degree", value=user_profile.get("degree", "") if user_profile else ""
            )
        with col2:
            title = st.text_input(
                "Title", value=user_profile.get("title", "") if user_profile else ""
            )
            university = st.text_input(
                "University", value=user_profile.get("university", "") if user_profile else ""
            )
        with col3:
            profession = st.text_input(
                "Profession", value=user_profile.get("profession", "") if user_profile else ""
            )

        st.subheader("Social Media")
        col1, col2 = st.columns(2)
        with col1:
            linkedin = st.text_input(
                "Linkedin",
                value=user_profile.get("social_media", {}).get("linkedin", "")
                if user_profile
                else "",
            )
            x = st.text_input(
                "X", value=user_profile.get("social_media", {}).get("x", "") if user_profile else ""
            )
        with col2:
            github = st.text_input(
                "GitHub",
                value=user_profile.get("social_media", {}).get("github", "")
                if user_profile
                else "",
            )
            personal_website = st.text_input(
                "Personal Website",
                value=user_profile.get("social_media", {}).get("personal website", "")
                if user_profile
                else "",
            )

        signature = st.text_area(
            "Email Signature", value=user_profile.get("signature", "") if user_profile else ""
        )

        submit_button = st.form_submit_button("Save Profile")

        if submit_button:
            social_media = {
                "linkedin": linkedin,
                "x": x,
                "github": github,
                "personal website": personal_website,
            }
            if user_profile:
                db.update_user_profile(
                    name, title, degree, university, profession, social_media, signature
                )
            else:
                db.set_user_profile(
                    name, title, degree, university, profession, social_media, signature
                )
            st.success("Profile updated successfully")

    # col1, col2 = st.columns([1, 3])
    # with col1:
    #     if st.button("Delete Profile", type="secondary", disabled=not user_profile):
    #         db.delete_user_profile()
    #         st.success("Profile deleted")


if __name__ == "__main__":
    main()
