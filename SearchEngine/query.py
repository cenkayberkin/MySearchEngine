#!/usr/local/bin/python
"""Author Mehmet Cenk Ayberkin"""

import pickle
from collections import deque
import os, glob, os.path
import sys


if len(sys.argv) != 2:
  print >> sys.stderr, 'usage: python query.py index_dir' 
  os._exit(-1)

def merge_posting (postings1, postings2):
    new_posting = []
    p1_index = 0
    p2_index = 0
    while len(postings1) > p1_index and len(postings2) > p2_index:
        if int(postings1[p1_index]) < int(postings2[p2_index]):
            p1_index += 1
        elif int(postings1[p1_index]) > int(postings2[p2_index]):
            p2_index += 1
        else: 
            new_posting.append(int(postings1[p1_index]))
            p1_index += 1
            p2_index += 1

    return new_posting

# file locate of all the index related files
#index_dir = "./OutDir"
index_dir = sys.argv[1]

doc_dict_f = open(index_dir + '/doc.dict', 'r')
word_dict_f = open(index_dir + '/word.dict', 'r')
file_pos_dict_f = open(index_dir + '/Pos.dict','r')
index_f = open(index_dir + '/corpus.index','r')

print >> sys.stderr, 'loading word dict'
word_dict = pickle.load(word_dict_f)
print >> sys.stderr, 'loading doc dict'
doc_id_dict = pickle.load(doc_dict_f)
print >> sys.stderr, 'loading index'
file_pos_dic = pickle.load(file_pos_dict_f)

def PrintDocuments(docIdList):
    if len(docIdList) > 0:
        for doc in docIdList:
            print str(doc_id_dict[int(doc)]) + "\n",
    else:
        print "no results found"

def read_posting(termId):
    #termId = word_dict[term]
    termPosition = file_pos_dic[str(termId)]
    index_f.seek(termPosition)
    line = index_f.readline()
    parts =  line.split("|")
    termId = int(parts[0])
    df = int(parts[1])
    postings = parts[2].rstrip('\n').split(",")
    return (termId,df,postings)

# read query from stdin
while True:
    postingList = []

    input = sys.stdin.readline()
    #input = "i\n"
    input = input.rstrip('\n')
    
    if len(input) == 0: # end of file reached
        break
    input_parts = input.split()
    #print "input partss " + str(input_parts)
    for term in input_parts:
        if term in word_dict:
           termId =  word_dict[str(term)]
           postingList.append(read_posting(termId))
        else:
            print "no results found"
    #sorting postingLists by document frequency
    sortedPosts = deque(sorted(postingList,key=lambda post: post[1]))

    if len(sortedPosts) == 1:
        PrintDocuments(sortedPosts[0][2])
    elif len(sortedPosts) > 1:
        while len(sortedPosts) > 1:
            merged = merge_posting(sortedPosts[0][2], sortedPosts[1][2])
            sortedPosts.popleft()
            sortedPosts.popleft()
            sortedPosts.appendleft((1,len(merged),merged))
        PrintDocuments(sortedPosts[0][2])

doc_dict_f.close()
word_dict_f.close()
file_pos_dict_f.close()