import streamlit as st

from utils.db import DatabaseManager

db = DatabaseManager()


def main():
    st.title("📄 Email Templates")
    st.caption("Create reusable templates to speed up sending.")
    st.divider()

    st.info(
        "Give each template a clear name and a body. These appear in the Send Email page dropdown.",
        icon="ℹ️",
    )

    with st.container(border=True):
        st.subheader("Add New Template")
        with st.form("add_template_form", clear_on_submit=True):
            template_name = st.text_input("Template Name", placeholder="Follow-up after meeting")
            template_body = st.text_area(
                "Template Body",
                height=220,
                placeholder="Hi {{name}},\nIt was great talking about ...",
            )
            submitted = st.form_submit_button("➕ Add Template", use_container_width=True)

            if submitted:
                if template_name and template_body:
                    db.add_template(template_name, template_body)
                    st.success("Template added successfully")
                    st.rerun()
                else:
                    st.error("Please fill in both the template name and body")

    st.divider()
    st.subheader("Existing Templates")
    templates = db.get_all_templates()

    if not templates:
        st.info("No templates yet. Add one above to get started.")
    else:
        for template in templates:
            with st.container(border=True):
                st.markdown(f"**{template['name']}**")
                st.text_area(
                    "",
                    value=template["body"],
                    height=160,
                    key=f"body_{template.doc_id}",
                    disabled=True,
                    label_visibility="collapsed",
                )
                if st.button("🗑️ Delete", key=f"delete_{template.doc_id}", use_container_width=True):
                    db.delete_template(template.doc_id)
                    st.success("Template deleted")
                    st.rerun()


if __name__ == "__main__":
    main()
