import streamlit as st
import openai

# Set the OpenAI Assistant ID (replace with your actual assistant ID)
ASSISTANT_ID = "asst_axrsu71yTNAXbzyf1Nv1EJ59"

# ... [other functions: init_openai_client, upload_file, update_assistant_with_files, create_thread, add_message_to_thread, get_thread_responses, run_assistant_and_get_response] ...

# Streamlit app main function
def main():
    st.title("OpenAI Chatbot with File Upload")

    # Initialize OpenAI client
    client = init_openai_client()

    # Initialize session state if not already done
    if 'thread_id' not in st.session_state:
        st.session_state['thread_id'] = create_thread(client)
    if 'file_ids' not in st.session_state:
        st.session_state['file_ids'] = []
    if 'conversation_log' not in st.session_state:
        st.session_state['conversation_log'] = []

    # File uploader
    uploaded_file = st.file_uploader("Upload a file", type=['pdf', 'txt', 'docx'])
    if uploaded_file is not None:
        file_id = upload_file(client, uploaded_file)
        if file_id:
            st.session_state['file_ids'].append(file_id)
            st.success("File uploaded successfully.")
            update_assistant_with_files(client, st.session_state['file_ids'])

    # Text input for user query
    user_query = st.text_input("Enter your query:")

    # Send Query
    if st.button('Send Query'):
        if user_query:
            add_message_to_thread(client, st.session_state['thread_id'], user_query)
            response = run_assistant_and_get_response(client, st.session_state['thread_id'])
            if response:
                st.session_state['conversation_log'].append(f"You: {user_query}\nAssistant: {response}\n")
            else:
                st.session_state['conversation_log'].append(f"You: {user_query}\nAssistant: No response received.\n")

    # Display the conversation log in a single, scrollable text area
    full_conversation = "".join(st.session_state['conversation_log'])
    st.text_area("Conversation", full_conversation, height=300, key="conversation_area")

    # Start New Thread
    if st.button('Start New Thread'):
        st.session_state['thread_id'] = create_thread(client)
        st.session_state['file_ids'] = []
        st.session_state['conversation_log'] = []

# Run the Streamlit app
if __name__ == "__main__":
    main()


