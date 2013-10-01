
from string import ascii_lowercase
import sys
global finished
global queue
global my_words

queue = []

class Node:
    def __init__(self, word, parent=None):
        self.word = word
        self.children = []
        self.parent = parent

    def get_children(self):
        global my_words

        #change the word to a list to change its letters
        word = list(self.word)
        for position in range(len(word)):
            temp = word[:]
            for letter in list(ascii_lowercase):
                temp[position] = letter
                new_word = ''.join(temp)
                if my_words.has_key(new_word) and my_words[new_word] == 0:
                    new_node = Node(new_word,parent=self)
                    self.children.append(new_node)
                    my_words[new_word] = 1

def load_words(location):
    f = file(location).read()
    return f


def get_words(all_words,word_length):
    global my_words
    my_words = {}
    for word in all_words.split():
        if len(word) is word_length:
            my_words[word.lower()] = 0
    return my_words




def process(my_words, start_node, end):
    global finished
    global queue

    #words reached by changing 1 letter
    similar_words ={}

    #starting temporary word
    top_temp = list(start_node.word)

    #hold parent of current node
    parent = start_node.parent

    #delete start word from list
    if my_words[start_node.word] == 0:
        my_words[start_node.word] = 1

    #get the children of the current(start) node

    start_node.get_children()
    curr_children = start_node.children

    #for everyone of the new children, build queue
    for child in curr_children:

        #if we reach the end word we are finished
        if child.word == end:
            finished = True
            print 'reached end word'
            path = []
            #print the path from the end to the start word
            while child.parent is not None:
                path.append(child.word)
                child =  child.parent
            path.append(child.word)
            path.reverse()
            print path
            break

        #if current_node word is in the english dictionary then add
        # to similar and remove from my_words
        if child not in similar_words:
            parent = child.parent
            similar_words[child] = 1

        #add every node from similar words into queue if it is not there
        for node in similar_words:
            if node not in queue:
                queue.append(node)

if __name__ == '__main__':
    global finished
    args = sys.argv
    start_word = args[1]
    end_word = args[2]
    start_node = Node(start_word)
    finished = False
    w = load_words('/usr/share/dict/words')
    if len(start_word) == len(end_word):
        word_length = len(start_word)
    else:
        print """ Word length does not match! Make sure you are using two words of the same length """
        sys.exit(0)

    #start the process with the start_node
    process(get_words(w,len(start_word)),start_node,end_word)

    while queue:
        #first node from queue
        first_node = queue.pop(0)

        #if it is in my_words delete it
        if first_node.word in my_words:
            my_words[first_node.word] = 1

        #if no valid path is found, inform the user
        if finished == False and len(queue) == 0:
            print ("There is no way to reach %s from %s "
                    "through the English dictionary") % (start_word,end_word)

        #if we are still looking, continue with the first node from queue
        if finished == False:
            process(my_words, first_node, end_word)

