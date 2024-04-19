import streamlit as st
from PIL import Image
import time
import os
import pandas as pd
from pdf2pdf import extract_text, generate_embeddings, query_pinecone

def main():
    st.set_page_config(page_title="Research Assistant", layout="wide")

    css = """
    <style>
    h1 {
        color: #1f77b4;
        font-weight: bold;
        font-size: 36px;
    }
    p {
        font-size: 18px;
        line-height: 1.5;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


    # Search functionality
    with st.form(key='search_form'):
        search_query = st.text_input("Enter search terms or a prompt to find research papers:")
        search_button = st.form_submit_button(label='Search')
        if search_button:
            with st.spinner('Searching for relevant research papers...'):
                embeddings = generate_embeddings(search_query)
                query_results = query_pinecone(embeddings)
                query_matches = query_results[0]["matches"]
                
                similar_papers = {"DOI":[], "Title":[], "Date":[]}
                for match in query_matches:
                    similar_papers["DOI"].append(match["metadata"]["doi"])
                    similar_papers["Title"].append(match["metadata"]["title"])
                    similar_papers["Date"].append(match["metadata"]["latest_creation_date"])
                similar_papers = pd.DataFrame(similar_papers)
                similar_papers_sorted = similar_papers.sort_values(by="Date", ascending=False)
                st.write(similar_papers_sorted)

    # PDF Upload
    with st.form(key='upload_form'):
        uploaded_file = st.file_uploader("Upload a PDF file of a Research Paper, to find a Similar Research Paper", type=['pdf'])
        upload_button = st.form_submit_button(label='Upload')
        if upload_button and uploaded_file:
            with st.spinner('Processing your PDF...'):
                file_path = os.path.join("PDFs", uploaded_file.name)
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getvalue())
                data = extract_text("PDFs/" + uploaded_file.name)
                if len(data) > 5:
                    embeddings = generate_embeddings(data)
                    query_results = query_pinecone(embeddings)
                    query_matches = query_results[0]["matches"]
                    
                    similar_papers = {"DOI":[], "Title":[], "Date":[]}
                    for match in query_matches:
                        similar_papers["DOI"].append(match["metadata"]["doi"])
                        similar_papers["Title"].append(match["metadata"]["title"])
                        similar_papers["Date"].append(match["metadata"]["latest_creation_date"])
                    similar_papers = pd.DataFrame(similar_papers)
                    similar_papers_sorted = similar_papers.sort_values(by="Date", ascending=False)
                    st.write(similar_papers_sorted)

    
    st.write("## Chat with the Model")
    user_input = st.text_input("Enter your research topic here:")
    if user_input:
        # Logic to handle chat interaction or provide summaries
        st.write("Generating overview for your topic...")
        # Display research summaries, timeline or domain overviews here.

    with st.form(key='upload_pdf_form'):
        st.write("Chat Pdf")
        uploaded_file = st.file_uploader("Upload your research PDF:", type=['pdf'])
        submit_button = st.form_submit_button("Submit PDF")

    if submit_button and uploaded_file:
        with st.spinner('Processing your PDF...'):
            # PDF processing logic goes here
            time.sleep(2)  # Simulate the processing delay
            st.success('Finished processing! Chat with the model below to get a summary or explore more.')


    

    # Tutorial page
     
    st.sidebar.header("Tutorial")
    st.sidebar.write("This is a tutorial on how to use the Research Assistant application.")
    st.sidebar.write("1.  ")
    st.sidebar.write("2.  ")
    st.sidebar.write("3.  ")

 
if __name__ == "__main__":
    main()