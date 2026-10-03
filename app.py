import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from ask_ollama import ask_llama


st.header("PDF to Vector Store")
with st.sidebar:
    st.subheader("Upload your PDF")
    file = st.file_uploader("Upload your PDF", type=["pdf"])
text = ""
if file is not None:
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    # st.write(text)

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

chunks = get_text_chunks(text)
st.write("Number of chunks: " + str(len(chunks)))
# st.write(chunks)

embeddigs = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)
st.write("Embeddings created")

if len(chunks) > 0:
    vector_store = FAISS.from_texts(chunks, embeddigs)
    st.write("Vector store created")
else:
    st.write("No chunks to create vector store from.")


input = st.text_input("Ask a question about your PDF:")
if input:
    with st.spinner("Searching for similar content in the PDF...", show_time=True):
        match = vector_store.similarity_search(input, k=3)

        st.write("Top 3 matches from the PDF:")
        st.table([m.page_content[:100] + "..." for m in match])

    with st.spinner("Generating answer from LLaMA...", show_time=True):
        prompt = f"""
        You are a helpful assistant. Use the following context to answer the question. 
        if the answer is not contained within the context below, say "I don't know." Do not make up an answer.
        Context: {match} Question: {input}
        """

        answer = ask_llama(prompt)
    
    st.success("Done!")
    st.write("Answer from LLaMA:")
    st.write(answer)




