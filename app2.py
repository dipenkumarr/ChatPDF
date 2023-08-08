import streamlit as st

# import logging
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template

# # Setup logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# logger = logging.getLogger(__name__)


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        # separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
        separator="\n",
        chunk_size=512,
        chunk_overlap=24,
        length_function=len,
    )

    chunks = text_splitter.split_text(text)

    return chunks


def get_vertorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

    return vectorstore


def get_conversation_chain(vectorstore):
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-xxl",
        model_kwargs={"temperature": 0.5, "max_length": 512},
        huggingfacehub_api_token="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",
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vectorstore.as_retriever(), memory=memory
    )

    return conversation_chain


# def get_conversation_chain(vectorstore):
#     llm = HuggingFaceHub(
#         repo_id="google/t5-small-chat",
#         model_kwargs={"temperature": 0.6, "max_length": 512},
#         huggingfacehub_api_token="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",
#     )
#     memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

#     conversation_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm, retriever=vectorstore.as_retriever(), memory=memory
#     )

#     return conversation_chain


def handle_user_input(user_question):
    response = st.session_state.conversation_chain({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    if "chat_history" in st.session_state:
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(
                    user_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True,
                )
            else:
                st.write(
                    bot_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True,
                )
    else:
        st.write("Sorry, the information you requested was not found in the document.")


# --------------------- Streamlit App ---------------------


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with PDF", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    st.sidebar.subheader("Your Documents")
    pdf_docs = st.sidebar.file_uploader(
        "Upload your PDF here", accept_multiple_files=True
    )

    st.sidebar.write("<br><br>", unsafe_allow_html=True)

    st.sidebar.subheader("Choose a Model")
    model_options = ["hkunlp/instructor-xl"]
    model_name = st.sidebar.selectbox("Select a model", model_options)

    if st.sidebar.button("Process"):
        if pdf_docs:
            with st.spinner("Processing"):
                # Getting pdf
                raw_text = get_pdf_text(pdf_docs)

                # Getting text chunks
                text_chunks = get_text_chunks(raw_text)

                # Creating vector storage
                vectorstore = get_vertorstore(text_chunks)

                # Creating conversation chain
                st.session_state.conversation_chain = get_conversation_chain(
                    vectorstore
                )
        else:
            st.sidebar.warning("Please upload one or more PDF documents.")

    # Display the main app content
    st.header("Chat with PDF")
    user_question = st.text_input("Ask a question about your document:")
    styl = f"""
        <style>
            .stTextInput {{
            position: fixed;
            bottom: 3rem;
            z-index:3;
            }}
        </style>
        """
    st.markdown(styl, unsafe_allow_html=True)

    if user_question:
        if pdf_docs:
            handle_user_input(user_question)
        else:
            st.warning("Please upload one or more PDF documents.")

    st.sidebar.write("<br><br><br>", unsafe_allow_html=True)
    # Implement a user feedback mechanism (for example, with a simple rating)

    st.sidebar.subheader("Feedback")
    user_feedback = st.sidebar.radio(
        "How was your experience?", ["Great!", "Not good."]
    )

    if user_feedback == "Great!":
        st.sidebar.success("Thank you for your feedback!")
    elif user_feedback == "Not good.":
        st.sidebar.warning(
            "We're sorry to hear that. Please let us know how we can improve."
        )


# Run the app
if __name__ == "__main__":
    main()
