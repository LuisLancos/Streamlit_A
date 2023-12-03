import streamlit as st
import openai

# Set the OpenAI Assistant ID (replace with your actual assistant ID)
ASSISTANT_ID = "asst_axrsu71yTNAXbzyf1Nv1EJ59"

# Initialize OpenAI client with API key from Streamlit secrets
def init_openai_client():
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    return openai.Client(api_key=openai_api_key)

# Additional functions (upload_file, update_assistant_with_files, create_thread, etc.) here...

# Streamlit app main function
def main():
    st.title("Gliding Technical Advisor")

    # Initialize OpenAI client
    client = init_openai_client()

    # Initialize session state for thread ID and response area
    if 'thread_id' not in st.session_state or st.session_state['thread_id'] is None:
        st.session_state['thread_id'] = create_thread(client)
    if 'response_area' not in st.session_state:
        st.session_state['response_area'] = []

    # File uploader positioned at the bottom
    uploaded_file = st.file_uploader("Upload a file", type=['pdf', 'txt', 'docx'])
    if uploaded_file is not None:
        file_id = upload_file(client, uploaded_file)
        if file_id:
            st.success("File uploaded successfully.")
            update_assistant_with_files(client, [file_id])

    # Text input for user query
    user_query = st.text_input("Enter your query:")

    # Send Query
    if st.button('Send Query'):
        if user_query:
            add_message_to_thread(client, st.session_state['thread_id'], user_query)
            response = run_assistant_and_get_response(client, st.session_state['thread_id'])
            if response:
                st.session_state['response_area'].append(f"You: {user_query}\nAssistant: {response}")
            else:
                st.session_state['response_area'].append(f"You: {user_query}\nAssistant: No response received.")

    # Display the response area
    for message in st.session_state['response_area']:
        st.text_area("", message, height=100, key=message[:30])  # Unique key for each message

    # Start New Thread
    if st.button('Start New Thread'):
        st.session_state['thread_id'] = create_thread(client)
        st.session_state['response_area'] = []

# Run the Streamlit app
if __name__ == "__main__":
    main()


