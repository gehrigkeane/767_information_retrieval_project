ECS 767 Information Retrieval Project
===================

Brought to you by Qiaozhi Wang, Yound Liu, and Gehrig Keane. This is the home of the python implementation for a rudimentary information retrieval system.

Project Structure
-------------

The project directory contains several files with the following structure

#### Memory Assets

Contains pickle files for the inverted index, pre-processed document vectors, and the **IDF** figures for the dictionary. (inverted_index.pickle, document_vectors.pickle, document_index.pickle, and idf.pickle)

* **inverted_index.pickle:** contains the inverted index data structure
* **document_index.pickle:** contains a dictionary of document names and their corresponding document number
* **document_vectors.pickle:** contains a list of lists which contain the normalized document vectors 
* **idf.pickle:** contains a dictionary of terms and their associated **IDF** values

#### Tokenization

This file contains all of the pre-processed documents in their token form, they are stored in pickle files as a list of plaintext tokens.

#### Tour

This file contains all of the raw documents and their psuedo-processed pickle companions, these files require further pre-processing

#### Test

This file contains simple python scripts that serve a number of utilities
