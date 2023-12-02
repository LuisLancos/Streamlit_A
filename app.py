import streamlit as st
import openai

# Function to initialize OpenAI client with API key from Streamlit secrets
def init_openai_client():
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    return openai.Client(api_key=openai_api_key)

# Function to create a new thread
def create_thread(client):
    thread = client.beta.threads.create()
    return thread.id

# Function to add a message to a thread
def add_message_to_thread(client, thread_id, message_content):
    client.beta.threads.messages.create(thread_id=thread_id, role="user", content=message_content)

# Function to get responses from a thread
def get_thread_responses(client, thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id, order="asc")
    return [msg.content[0].text.value for msg in messages.data if msg.role == 'assistant']

# Function to run the assistant and get a response
def run_assistant_and_get_response(client, assistant_id, thread_id):
    run = client.beta.threads.runs.create(assistant_id=assistant_id, thread_id=thread_id)
    while run.status not in ['completed', 'failed']:
        run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread_id)
    if run.status == 'completed':
        return get_thread_responses(client, thread_id)
    else:
        return ["No response or run failed"]

# Streamlit app main function
def main():
    st.title("OpenAI Chatbot")

    # Initialize OpenAI client
    client = init_openai_client()

    # Session state for thread management
    if 'thread_id' not in st.session_state:
        st.session_state['thread_id'] = create_thread(client)
    
    # Text input for user query
    user_query = st.text_input("Enter your query:")

    # Handling the 'Send Query' button
    if st.button('Send Query'):
        if user_query:
            assistant_id = "asst_axrsu71yTNAXbzyf1Nv1EJ59"  # Replace with your actual assistant ID
            add_message_to_thread(client, st.session_state['thread_id'], user_query)
            response = run_assistant_and_get_response(client, assistant_id, st.session_state['thread_id'])
            if response:
                st.write("Assistant's Response:", response[0])
            else:
                st.write("Assistant's Response: No response received.")

    # Handling the 'Start New Thread' button
    if st.button('Start New Thread'):
        st.session_state['thread_id'] = create_thread(client)

# Run the Streamlit app
if __name__ == "__main__":
    main()
