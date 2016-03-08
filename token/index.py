#	Author:		Gehrig Keane
#	Purpose:	Testing posting list creation
#	Description:N/A

import os
import llist
import token_rename

def create_inverted_index():
    # List and open every file in current dir
    tk_files = [file for file in os.listdir(".") if file.endswith(".tk")]
    words = {}

    # x = file number 0, 1, ..., n
    # y = file name
    for x,y in enumerate(tk_files):
            # Reset line and word counters
            line_count, word_count = 0, 0

            # Open file y for writing
            with open(y,'r') as f:

                    # Iterate through every line->word in file y
                    for line in f:
                            for word in line.split():
                                    # We are now parsing word by word
                                    # y = filename
                                    # x = filenumber - don't trust this number as it will change with new files in the dir
                                    # f is the file object
                                    # word = current word

                                    # Check if word is in the dictionary
                                    if word in words.keys():
                                            # Capture dict entry for existing word
                                            w = words[word]
                                            w[1] += 1	# increment total frequency

                                            # Check Augments/Modifies the linked list appropriately
                                            ll = w[2]
                                            ll.check(y, line_count, word_count)
                                            w[0] = ll.length
                                    
                                    # Create Dict entry for new word
                                    else:
                                            ll = llist.posting_list()
                                            ll.add(y, line_count, word_count)
                                            words[word] = [1,1,ll]

                                    word_count += 1
                            line_count += 1
    return words

def print_index():
    # x = key - the word
    # y = value - the array of [doc_freq, tot_freq, ll]
    for x,y in words.items():
            print x,
            print "[" + str(y[0]) + ", " + str(y[1]),
            y[2].list_print()
            print "]"

