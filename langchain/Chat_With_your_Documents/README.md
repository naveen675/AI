# Chat With Your Documents


## Summary

Chat With Your Documents is a Python application that enables users to interact with multiple PDF documents using natural language queries. This application uses advanced text processing and language understanding techniques to extract information from uploaded PDFs and provide relevant answers to user questions.

## Table of Contents

- [Tools and Python Modules/Frameworks/Packages Used](#tools-and-python-modulesframeworkspackages-used)
- [How the Application Works](#how-the-application-works)
- [Usage of Embeddings](#usage-of-embeddings)
- [Example Usage](#example-usage)
- [Important Notes](#important-notes)
- [How to Run the Application](#how-to-run-the-application)
- [GitHub Repository](#github-repository)
- [Contact](#contact)

## Tools and Python Modules/Frameworks/Packages Used

- **Streamlit**: Streamlit is used for creating the user interface of the application.
- **PyPDF2**: PyPDF2 is used for reading text from PDF documents.
- **langchain**: langchain is a custom library that provides text processing and language understanding capabilities.
- **HuggingFace Transformers**: HuggingFace's Transformers library is used for working with pre-trained language models.
- **FAISS**: FAISS is used for creating a vector store for text chunks.
- **Google Cloud**: For deploying this application. I have used cloud run here. Vertex AI for accessing PALM LLM

## How the Application Works

1. Users upload one or more PDF documents using the left sidebar.
2. After uploading the documents, users click the "Process" button to extract text content from the PDFs and create a vector store for text chunks.
3. Once the processing is complete, users can enter questions related to the content of the PDFs in the text input field.
4. The application uses a language model and embeddings to understand the user's question and retrieve relevant information from the PDFs.
5. The answers are displayed in the main content area of the application.

## Usage of Embeddings

The application uses embeddings to represent text chunks from the uploaded PDF documents. These embeddings help in efficiently searching for relevant information when users ask questions. The embeddings are generated using HuggingFace Transformers, allowing for semantic understanding of the text.

## Example Usage

- Upload your PDF documents and click on the "Process" button.
- Enter a question related to the content of the uploaded PDFs in the text input field.
- The application will provide an answer based on the information in the PDF documents.

## Important Notes

- The language model and embeddings can only provide answers based on the information present in the uploaded PDFs. If the information is not in the documents, it will respond with "I am sorry, This Information is not available in the provided Documents."

## How to Run the Application

1. Make sure you have the required Python modules installed.
2. Set up the necessary environment variables as mentioned in the code (e.g., `EMBEDDING_MODEL_NAME`, `GOOGLE_APPLICATION_CREDENTIALS`, and `HUGGINGFACEHUB_API_TOKEN`).
3. Run the Python script.
4. Access the application through your web browser.

## GitHub Repository

The code for this application can be found on GitHub: [GitHub Repository](https://github.com/naveen675/AI/blob/main/langchain/Chat_With_your_Documents)

## Contact

- GitHub: [GitHub Profile](https://github.com/naveen675)
- LinkedIn: [LinkedIn Profile](www.linkedin.com/in/naveen675)

Feel free to reach out if you have any questions or feedback about the application.

Credits: ChatGpt for Writing ReadMe file with the given prompt.
