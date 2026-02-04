import streamlit as st
from utils.db import DatabaseManager

db = DatabaseManager()

def main():
    st.title("🤖 Email Chatbot")
    st.caption("Get help with composing emails, managing templates, and more!")
    st.divider()

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        # Add welcome message
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Hello! I'm your Email Assistant. I can help you:\n\n"
                      "• Compose emails using templates\n"
                      "• Suggest recipients for your emails\n"
                      "• Answer questions about your email management system\n"
                      "• Provide tips for better email communication\n\n"
                      "What would you like to do today?"
        })

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about emails..."):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Generate response
        response = generate_response(prompt.lower())

        # Add assistant response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)

        # Rerun to update the chat
        st.rerun()

def generate_response(prompt):
    """Generate a response based on the user's prompt."""

    # Get data from database
    profiles = db.get_all_profiles()
    templates = db.get_all_templates()

    # Basic keyword matching for responses
    if any(word in prompt for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! How can I help you with your emails today?"

    elif any(word in prompt for word in ["compose", "write", "create", "draft"]):
        if "email" in prompt:
            return compose_email_help(templates)

    elif any(word in prompt for word in ["template", "templates"]):
        return template_help(templates)

    elif any(word in prompt for word in ["recipient", "recipients", "contact", "contacts"]):
        return recipient_help(profiles)

    elif any(word in prompt for word in ["send", "schedule", "reminder"]):
        return "To send emails, schedule them, or set reminders, please visit the '📧 Send Emails' page from the sidebar. I can help you prepare your content here first!"

    elif any(word in prompt for word in ["help", "what can you do", "commands"]):
        return get_help_text()

    elif any(word in prompt for word in ["thank", "thanks"]):
        return "You're welcome! Is there anything else I can help you with?"

    elif any(word in prompt for word in ["bye", "goodbye", "see you"]):
        return "Goodbye! Feel free to come back anytime you need help with your emails."

    else:
        # Try to understand context or provide general help
        return get_general_response(prompt, profiles, templates)

def compose_email_help(templates):
    """Help with composing emails."""
    if not templates:
        return "You don't have any email templates yet. Visit the '📄 Email Templates' page to create some templates first!"

    template_names = [t["name"] for t in templates]
    response = "I can help you compose an email! Here are your available templates:\n\n"
    for i, name in enumerate(template_names, 1):
        response += f"{i}. {name}\n"
    response += "\nTell me which template you'd like to use, or describe what kind of email you want to write (e.g., 'business introduction', 'follow-up', 'thank you note')."

    return response

def template_help(templates):
    """Provide information about templates."""
    if not templates:
        return "You don't have any email templates yet. Go to the '📄 Email Templates' page to create your first template!"

    count = len(templates)
    template_names = [t["name"] for t in templates]

    response = f"You have {count} email template{'s' if count != 1 else ''}:\n\n"
    for name in template_names:
        response += f"• {name}\n"

    response += "\nYou can create new templates or edit existing ones on the '📄 Email Templates' page."

    return response

def recipient_help(profiles):
    """Provide information about recipients."""
    if not profiles:
        return "You don't have any recipients yet. Visit the '👥 Profiles' page to add contacts!"

    count = len(profiles)
    response = f"You have {count} contact{'s' if count != 1 else ''} in your address book:\n\n"

    for profile in profiles[:5]:  # Show first 5
        response += f"• {profile['name']} - {profile['title']} ({profile['profession']})\n"

    if count > 5:
        response += f"... and {count - 5} more\n"

    response += "\nYou can manage your contacts on the '👥 Profiles' page."

    return response

def get_help_text():
    """Return help text."""
    return """Here's what I can help you with:

**Email Composition:**
• Help you choose and customize email templates
• Suggest appropriate content based on recipient profiles
• Provide writing tips for different types of emails

**Templates & Recipients:**
• Show you available email templates
• List your contacts and their details
• Help you match templates to recipients

**System Navigation:**
• Guide you to the right pages for specific tasks
• Explain how different features work

**General Tips:**
• Best practices for email communication
• Professional writing suggestions

Just ask me anything related to email management!"""

def get_general_response(prompt, profiles, templates):
    """Try to provide a helpful general response."""
    # Check if user is asking about specific features
    if "dashboard" in prompt:
        return "The dashboard shows your email statistics and quick actions. Visit the home page to see your metrics and recent activity."

    elif "schedule" in prompt or "reminder" in prompt:
        return "You can schedule emails and set reminders on the '📧 Send Emails' page. Choose 'Schedule' or 'Add Reminder' after composing your email."

    elif "search" in prompt:
        return "Use the '🔍 Search' page to find specific emails, contacts, or templates in your system."

    elif "profile" in prompt or "user" in prompt:
        return "You can manage your user profile and system settings on the '🙋‍♀️ User Profile' page."

    else:
        return "I'm not sure I understand. Try asking about:\n• Composing emails\n• Your templates or contacts\n• How to use specific features\n• Or just say 'help' to see all my capabilities!"

if __name__ == "__main__":
    main()
