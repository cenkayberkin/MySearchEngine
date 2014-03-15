#!/usr/local/bin/python
"""Author Mehmet Cenk Ayberkin"""

import string
import os, sys
from collections import deque
import pickle
from collections import OrderedDict
import Compress

if len(sys.argv) != 3:
  print >> sys.stderr, 'usage: python index.py data_dir output_dir'
  os._exit(-1)

total_file_count = 0
root = sys.argv[1]
out_dir = sys.argv[2]

#root = "/Users/cenkayberkin/Desktop/PA12/toy_example/data"
#out_dir = "/Users/cenkayberkin/Desktop/PA12/toy_example/outDir"
if not os.path.exists(out_dir):
  os.makedirs(out_dir)

#root = "./Corpus"
#out_dir = "./OutDir"

# this is the actual posting lists dictionary
# word id -> {position_in_file, doc freq}
file_pos_dict = {}
# this is a dict holding document name -> doc_id
doc_id_dict = {}
# this is a dict holding word -> word_id
word_dict = {}
# this is a queue holding block names, later used for merging blocks
block_q = deque([])

doc_id = -1
word_id = 0

def count_file():
  global total_file_count
  total_file_count += 1

def CompressIndex(index_f,indexC_f):
    linetoEncode = index_f.readline()
    while linetoEncode != '':
        line=  linetoEncode.split("|")
        posts = line[2].rstrip("\n").split(",")
        gappedResult = Compress.toGaps(posts)
        encodedResult = Compress.vb_encode(gappedResult)
        encodedString = "".join(map(chr,encodedResult))
        resultLine = "{termId}|{df}|{posts}".format(termId=line[0],df=line[1],posts=encodedString)
        file_pos_dict[line[0]] = (int(indexC_f.tell()),len(resultLine))
        indexC_f.write(resultLine)
        linetoEncode = index_f.readline()

def merge_posting (b1_f, b2_f,comb_f):
    result = []
    b1_next = b1_f.readline()
    b2_next= b2_f.readline()
    while not (b1_next == '' and b2_next == ''):
        line1=  b1_next.split("|") 
        line2 = b2_next.split("|")

        if line1[0] == '':
            #result.append(b2_next)
            comb_f.write(b2_next)
            termId = b2_next.split("|")[0]
            file_pos_dict[termId] = int(comb_f.tell()) - int(len(b2_next)) 
            b2_next= b2_f.readline()
        elif line2[0] == '':
            #result.append(b1_next)
            comb_f.write(b1_next)
            termId = b1_next.split("|")[0]
            file_pos_dict[termId] = int(comb_f.tell()) - int(len(b1_next)) 
            b1_next = b1_f.readline()    
        elif int(line1[0]) < int(line2[0]):
            #result.append(b1_next)
            comb_f.write(b1_next)
            termId = b1_next.split("|")[0]
            file_pos_dict[termId] = int(comb_f.tell()) - int(len(b1_next)) 
            b1_next = b1_f.readline()    
        elif int(line1[0]) > int(line2[0]):
            #result.append(b2_next)
            comb_f.write(b2_next)
            termId = b2_next.split("|")[0]
            file_pos_dict[termId] = int(comb_f.tell()) - int(len(b2_next)) 
            b2_next= b2_f.readline()
        else:
           postings1 = line1[2].rstrip('\n').split(",")
           postings2 = line2[2].rstrip('\n').split(",")
           unionOfPosts = set(postings1).union(set(postings2))
           postings = ",".join(sorted(unionOfPosts,key=lambda i:int(i)))
           resultLine = "{termId}|{df}|{posts}\n".format(termId=line1[0],df=str(len(unionOfPosts)),posts=postings)
           comb_f.write(resultLine)
           file_pos_dict[line1[0]] = int(comb_f.tell()) - int(len(resultLine)) 
           #result.append(resultLine)
           b1_next = b1_f.readline()
           b2_next= b2_f.readline()
    #comb_f.write("".join(result))
    
def WriteTermsToDisk(sortedPostingsList, block_pl):
    tempDic = {}
    for posting in sortedPostingsList:
        if posting[0] not in tempDic:
            tempDic[posting[0]] = [1, set([posting[1]])]
        else:
            tempDic[posting[0]][1].add(posting[1])
    
    for item in sorted(tempDic.keys()):
        block_pl.write("{item}|{df}|{docIds}\n".format(item=item,df=str(len(tempDic[item][1])),docIds=",".join(str(i) for i in sorted(tempDic[item][1]))))
        
for dir in sorted(os.listdir(root)):
  print >> sys.stderr, 'processing dir: ' + dir
  dir_name = os.path.join(root, dir)
  block_pl_name = out_dir+'/'+dir 
  # append block names to a queue, later used in merging
  block_q.append(dir)
  block_pl = open(block_pl_name, 'w')
  term_doc_list = []
  for f in sorted(os.listdir(dir_name)):
    count_file()
    file_id = os.path.join(dir, f)
    doc_id += 1
    doc_id_dict[doc_id] = file_id
    fullpath = os.path.join(dir_name, f)
    file = open(fullpath, 'r')
    for line in file.readlines():
      tokens = line.strip().split()
      for token in tokens:
        if token not in word_dict:
          word_dict[token] = word_id
          word_id += 1
        term_doc_list.append((word_dict[token], doc_id))
  print >> sys.stderr, 'sorting term doc list for dir:' + dir
  sortedTermDocList = sorted(term_doc_list,key=lambda post: (post[0],post[1]))
  print >> sys.stderr, 'print posting list to disc for dir:' + dir
  WriteTermsToDisk(sortedTermDocList, block_pl)
  block_pl.close()

print >> sys.stderr, '######\nposting list construction finished!\n##########'

print >> sys.stderr, '\nMerging postings...'
while True:
  if len(block_q) <= 1:
    break
  b1 = block_q.popleft()
  b2 = block_q.popleft()
  print >> sys.stderr, 'merging %s and %s' % (b1, b2)
  b1_f = open(out_dir+'/'+b1, 'r')
  b2_f = open(out_dir+'/'+b2, 'r')
  comb = b1+'+'+b2
  comb_f = open(out_dir + '/'+comb, 'w')
  merge_posting(b1_f,b2_f,comb_f)
  b1_f.close()
  b2_f.close()
  comb_f.close()
  os.remove(out_dir+'/'+b1)
  os.remove(out_dir+'/'+b2)
  block_q.append(comb)

print >> sys.stderr, '\nPosting Lists Merging DONE!'

# rename the final merged block to corpus.index
final_name = block_q.popleft()
os.rename(out_dir+'/'+final_name, out_dir+'/corpus.indexU')

index_f = open(out_dir+'/corpus.indexU')
indexC_f = open(out_dir+'/corpus.index',"w")

print >> sys.stderr, '\nCompressing Index!'
CompressIndex(index_f, indexC_f)

# print all the dictionary files
doc_dict_f = open(out_dir + '/doc.dict', 'w')
word_dict_f = open(out_dir + '/word.dict', 'w')
file_pos_dict_f = open(out_dir + '/Pos.dict','w')
pickle.dump(doc_id_dict,doc_dict_f)
pickle.dump(word_dict,word_dict_f)
pickle.dump(file_pos_dict,file_pos_dict_f)
doc_dict_f.close()
word_dict_f.close()
file_pos_dict_f.close()
print total_file_count