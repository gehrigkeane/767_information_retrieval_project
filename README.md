# 767 Information Retrieval Project
Gehrig Keane, Young Liu, and Qiaozhi Wang

----------

### Contact Information
##### Gehrig Keane:
* gehrigkeane@gmail.com or gmk@ku.edu
* 316-210-8049

##### Young Liu:
* youngliu323@gmail.com
* 913-575-0715

##### Qiaozhi Wang:
* qzwang@ku.edu
* 785-551-8323

----------

### /token/test.py 
Currently builds a python dictionary in the style of an inverted index. After iterating through every file in the current working directory with the .tk extension a dictionary exists with words as keys and an array as the value. The array is always three elements long, the first element is always the document frequency, the second elements is always the total frequency, and the third element is always a linked list of postings. 

Dictionary 

| Key     | Value | [file_name, line_number, word_number, term_frequency]  |
| ------- | ------- | ------- |
| example word | [doc_freq, tot_freq, ll_object] | [node] -> [node] -> None |
| a       | [1,1,linkedlist] | [doc1.tk, [0], [2], 1] -> None |
| b       | [2,3,linkedlist] | [doc1.tk, [0], [2], 1] -> [doc2.tk, [0, 1], [1, 1], 2] -> None |
| etc... | | |

----------

### /token/token_rename.py 
This file can be imported for use with:

```python
import token_rename as tn

tn.htm_to_token()
tn.token_to_htm()
```
