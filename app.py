import streamlit as st
import openai

# Set the OpenAI Assistant ID (replace with your actual assistant ID)
ASSISTANT_ID = "your_assistant_id_here"

# Initialize OpenAI client with API key from Streamlit secrets
def init_openai_client():
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    return openai.Client(api_key=openai_api_key)

# Upload a file to OpenAI and return its ID
def upload_file(client, file):
    try:
        uploaded_file = client.files.create(file=file, purpose='assistants')
        return uploaded_file.id
    except Exception as e:
        st.error(f"Failed to upload file: {e}")
        return None

# Update assistant with file IDs
def update_assistant_with_files(client, file_ids):
    try:
        client.beta.assistants.update(ASSISTANT_ID, file_ids=file_ids)
    except Exception as e:
        st.error(f"Failed to update assistant with file: {e}")

# Create a new thread
def create_thread(client):
    try:
        thread = client.beta.threads.create()
        return thread.id
    except Exception as e:
        st.error(f"Failed to create thread: {e}")
        return None

# Add a message to a thread
def add_message_to_thread(client, thread_id, message_content):
    client.beta.threads.messages.create(thread_id=thread_id, role="user", content=message_content)

# Get responses from a thread
def get_thread_responses(client, thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id, order="asc")
    return [msg.content[0].text.value for msg in messages.data if msg.role == 'assistant']

# Run the assistant and get a response
def run_assistant_and_get_response(client, thread_id):
    run = client.beta.threads.runs.create(assistant_id=ASSISTANT_ID, thread_id=thread_id)
    while run.status not in ['completed', 'failed']:
        run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread_id)
    if run.status == 'completed':
        return get_thread_responses(client, thread_id)
    else:
        return ["No response or run failed"]

# Streamlit app main function
def main():
    st.title("OpenAI Chatbot with File Upload")

    # Initialize OpenAI client
    client = init_openai_client()

    # Session state for thread, file IDs, and conversation log management
    if 'thread_id' not in st.session_state or 'file_ids' not in st.session_state or 'conversation_log' not in st.session_state:
        st.session_state['thread_id'] = create_thread(client)
        st.session_state['file_ids'] = []
        st.session_state['conversation_log'] = []

    # File uploader
    uploaded_file = st.file_uploader("Upload a file", type=['pdf', 'txt', 'docx'])
    if uploaded_file is not None:
        file_id = upload_file(client, uploaded_file)
        if file_id:
            st.session_state['file_ids'].append(file_id)
            st.success("File uploaded successfully.")
            # Update the assistant with the new file ID
            update_assistant_with_files(client, st.session_state['file_ids'])

    # Text input for user query
    user_query = st.text_input("Enter your query:")

    # Send Query
    if st.button('Send Query'):
        if user_query:
            # Append user query to conversation log
            st.session_state['conversation_log'].append(f"You: {user_query}")
            add_message_to_thread(client, st.session_state['thread_id'], user_query)
            response = run_assistant_and_get_response(client, st.session_state['thread_id'])
            if response and response[0]:
                # Append assistant response to conversation log
                st.session_state['conversation_log'].append(f"Assistant: {response[0]}")
                st.write("Assistant's Response:", response[0])
            else:
                st.write("Assistant's Response: No response received.")

    # Display conversation log
    st.write("Conversation Log:")
    for message in st.session_state['conversation_log']:
        st.text(message)

    # Start New Thread
    if st.button('Start New Thread'):
        st.session_state['thread_id'] = create_thread(client)
        st.session_state['file_ids'] = []
        st.session_state['conversation_log'] = []

# Run the Streamlit app
if __name__ == "__main__":
    main()
