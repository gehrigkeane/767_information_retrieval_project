class node:
    def __init__(self):
        self.file_name = None # String value
        self.line_num = None # Int value
        self.word_num = None # Int value
        self.term_f = None # Int value
        self.next = None # contains the reference to the next node


class linked_list:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def add(self, fn, ln, wn):
        self.length += 1
        nn = node() # create a new node
        nn.file_name = fn
        nn.line_num = [ln]
        nn.word_num = [wn]
        nn.term_f = 1

        # Append new nodes to the back of the list
        if self.tail:
            self.tail.next = nn
            self.tail = nn
        else:
            self.head = nn
            self.tail = nn

    def check(self, fn, ln, wn):
        n = self.find(fn) 
        if n:
            # have the correct node
            n.term_f += 1
            n.line_num.append(ln)
            n.word_num.append(wn)
        else:
            # No node exists with filename
            self.add(fn, ln, wn)

    def find(self, fn):
        n = self.head
        while n:
            if n.file_name == fn:
                return n
            n = n.next
        return None

    def list_print(self):
        n = self.head # cant point to ll!
        while n:
            print "[fn:" + str(n.file_name) + ", ln:" + str(n.line_num) + ", wn:" + str(n.word_num) + ", tf:" + str(n.term_f) + "] -> ", 
            n = n.next
        print "None",