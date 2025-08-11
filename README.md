# Tesseract-OCR
As part of my project, I used Tesseract-OCR to extract data from PDF files. The goal was to read and store a large amount of data for implementing Retrieval-Augmented Generation (RAG). I also compared this method with an alternative approach that extracts data from PDFs using AI models.

I tried to compare a random page that is extracted by tesseract-OCR with the main text and found the similarity is approximately 94%.


Similarities:

-Source Document

-Core Content

-Structure 


Differences:

-Formatting

-Typographical/OCR Errors

-Missing or Incorrect Text

For small datasets, such as PDFs with only a few pages, using an AI model is more efficient. However, when dealing with large datasets—such as reading thousands of pages—Tesseract-OCR proves to be the better option in terms of cost.


