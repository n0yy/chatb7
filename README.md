# ChatB7 🤖

A virtual assistant powered by Gemini AI that provides information about PT Bintang Toedjoe.

## Overview 📋

ChatB7 is a Streamlit-based conversational AI assistant that uses Google's Gemini and Pinecone vector database to provide accurate information about PT Bintang Toedjoe and its products. The assistant is designed to answer questions in Indonesian language with natural and friendly responses.

## Features ✨

- Interactive chat interface built with Streamlit
- Powered by Google's Gemini 2.0 Pro model
- Retrieval-based answers using Pinecone vector database
- Word-by-word streaming responses for a more natural experience
- References to information sources where available
- Responsive design with clean UI

## Current Knowledge Base 📚

- Company Profile of PT Bintang Toedjoe
- Information about "Kua Lima" product

## Architecture 🏗️

- **Frontend**: Streamlit web application
- **AI Model**: Google Gemini 2.0 Pro
- **Vector Database**: Pinecone
- **Embeddings**: Google's text-embedding-004 model
- **Framework**: LangChain for orchestrating AI components

## Project Structure 📁

```
chatb7/
├── .env.example        # Example environment variables configuration
├── .gitignore          # Git ignore file
├── requirements.txt    # Project dependencies
└── app/
    ├── __init__.py
    ├── main.py         # Main Streamlit application
    ├── models/
    │   ├── __init__.py
    │   └── llms.py     # Language model implementation
    └── utils/
        ├── __init__.py
        └── word_stream.py  # Word streaming utility
```

## Environment Variables 🔑

The application requires the following environment variables:

- `GOOGLE_API_KEY`: Your Google API key for Gemini
- `PINECONE_API_KEY`: Your Pinecone API key

## Limitations 🚧

- Limited knowledge base (currently only Company Profile)
- Basic features only in the current version

## Version History 📝

### Version 0.1.3-beta

- Initial release of ChatB7
- Basic UI implementation
- Knowledge base for Company Profile

## Contributing 🤝

To contribute to ChatB7's knowledge base, you can upload PDF, DOCX, or PPTX files to the Google Drive folder:
[Source Files Access](https://drive.google.com/drive/folders/1WUx_0ztyjDt-e08SDoqqDePJnnxZXpIV?usp=sharing)

## Tech Stack 💻

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **LangChain**: Framework for AI applications
- **Google Gemini**: Large language model
- **Pinecone**: Vector database for efficient similarity search

## Future Developments 🚀

- Expanded knowledge base with more products
- Improved UI and user experience
- Enhanced context understanding
- Multi-language support
- Tabular Agent (SQL, CSV) for handling data as context
