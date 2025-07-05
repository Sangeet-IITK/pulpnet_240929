This project implements a transformer-based chatbot
that answers questions about IIT Kanpur Aerospace professors using information scraped from official sources.
The chatbot uses a DistilBERT model for question-answering and a sentence transformer for semantic search to find relevant context.

First, scrape the data by running: python scraper.py
then on terminal run: streamlit run app.py to launch chatbot

The app will open in your default browser at http://localhost:8501

The chatbot currently uses data scraped from: IIT Kanpur Aerospace Department faculty pages

A short demonstration video is available here
