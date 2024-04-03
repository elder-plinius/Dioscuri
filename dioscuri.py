import streamlit as st
from gemini_chat import GeminiChat
from appendages import get_appended_prompt

def main():
    st.title("Chat Interface")

    # Initialize GeminiChat
    gemini_chat = GeminiChat()

    # Chat history
    chat_history_container = st.container()

    # Function to display chat messages
    def display_chat_history(messages):
        with chat_history_container:
            for i, (role, message) in enumerate(messages):
                st.markdown(f"**{role}:**")
                st.write(message)
                st.write("---")

    # Initialize or retrieve chat history from session state
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    messages = st.session_state["chat_history"]

    # State variable for user input
    user_input_state = st.session_state.get("user_input_state", "")

    # User input
    user_input = st.text_input("Enter your message:", key="user_input", value=user_input_state)

    # Temperature slider
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.01)

    # Model dropdown
    model_options = ["gemini-pro"]
    selected_model = st.selectbox("Select Model", model_options, index=3)  # Default to "gemini"

    # Toggle for appending encoded string (jailbreak)
    append_encoded_string = st.checkbox("Toggle Jailbreak", value=False)

    if user_input:
        prompt = user_input
        if append_encoded_string:
            # Append encoded string to the user input
            prompt = user_input + " " + get_appended_prompt()

        max_retries = 5
        retry_count = 0
        response = None

        while retry_count < max_retries:
            # Send the prompt to GeminiChat
            if selected_model == "gemini-pro":
                response = gemini_chat.send_message(prompt, temperature=temperature)
            else:
                response = gemini_chat.send_message(prompt, temperature=temperature, model=selected_model)

            if response is not None:
                break

            retry_count += 1
            print(f"Retrying query ({retry_count}/{max_retries})...")

        if response is None:
            st.error("Failed to generate a response after multiple retries.")

        # Update chat history
        messages.append(("User", user_input))
        messages.append(("Assistant", response))
        st.session_state["chat_history"] = messages

        # Clear user input state
        st.session_state["user_input_state"] = ""

    # Display chat history
    display_chat_history(messages)

if __name__ == "__main__":
    main()
