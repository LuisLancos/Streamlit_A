import streamlit as st
import openai

# Set the OpenAI Assistant ID (replace with your actual assistant ID)
ASSISTANT_ID = "asst_axrsu71yTNAXbzyf1Nv1EJ59"

# Initialize OpenAI client with API key from Streamlit secrets
def init_openai_client():
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    return openai.Client(api_key=openai_api_key)

# [functions: upload_file, update_assistant_with_files, create_thread, add_message_to_thread, get_thread_responses, run_assistant_and_get_response]

# Streamlit app main function
def main():
    st.title("Gliding Technical Advisor")

    # Initialize OpenAI client
    client = init_openai_client()

    # Initialize session state for thread ID and conversation log
    if 'thread_id' not in st.session_state:
        st.session_state['thread_id'] = create_thread(client)
    if 'conversation_log' not in st.session_state:
        st.session_state['conversation_log'] = []

    # Text input for user query
    user_query = st.text_input("Enter your query:")

    # Send Query
    if st.button('Send Query'):
        if user_query and st.session_state['thread_id']:
            add_message_to_thread(client, st.session_state['thread_id'], user_query)
            response = run_assistant_and_get_response(client, st.session_state['thread_id'])
            conversation_entry = f"You: {user_query}\nAssistant: {response}\n" if response else f"You: {user_query}\nAssistant: No response received.\n"
            st.session_state['conversation_log'].insert(0, conversation_entry)

    # Display the conversation log in a single, scrollable text area
    full_conversation = "".join(st.session_state['conversation_log'])
    st.text_area("Conversation", full_conversation, height=300, key="conversation_area")

    # Start New Conversation Button
    if st.button('Start New Conversation'):
        st.session_state['thread_id'] = create_thread(client)
        st.session_state['conversation_log'] = []

    # File uploader positioned at the bottom
    st.subheader("Upload a File")
    uploaded_file = st.file_uploader("", type=['pdf', 'txt', 'docx'])
    if uploaded_file is not None:
        file_id = upload_file(client, uploaded_file)
        if file_id:
            st.success("File uploaded successfully.")
            update_assistant_with_files(client, [file_id])

# Run the Streamlit app
if __name__ == "__main__":
    main()

    main()
