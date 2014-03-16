#MySearchEngine
==============

My Search Engine which indexes and searches disk content like spotlight on Mac.

###Search Engine without compression
I have implemented BSBI algorithm for indexing. Because of memory limits we need to use disk, big data wouldn’t fit into memory. One way to do it is read and order postings by blocks. And then merge these blocks 2 at a time (binary merge). Finally i merge all these block inverted indexes at corpus.index file. At corpus.index I keep termId s, document frequencies documentIds as postings. Every line on index is one termId and its information. I keep offset positions of these term IDs at position Dictionary. For querying i find necessary information by using file offsets and then I sort document frequencies of query terms. I start from the smallest possible document frequency terms postings for merging. So increase my chance to have smaller intermediate results for AND operations.
My Compressed index works like this. First I built uncompressed index and then I compress it. I keep offsets and data length of each term information.
File count: 98998
Index memory: memusg: peak=1063656
Uncompress Index size: 84.4 MB
Compressed Index size: 19.5 MB
Index time: 172 seconds
Task 1 query times.
6 seconds
6 seconds

###Search Engine 

A) I have used each sub-directory as a block and built index for one block at a time. If
we have bigger sized blocks than we can process them faster but we will be needing
bigger memory for that. For minimizing indexing time we need to reduce disk
operations which means we should have biggest blocks possible which can fit into our
memory and process it.

B) First of all my indexing program is working on one computer. So its indexing capability
is limited to one computers disk and memory size. Even on one computer I think it’s
faster to directly work with dictionary instead of having list of postings and sort them
then put them into dictionary data structure like SPIMI.

C) Using offsets of termIds and postings is fast way to do it. But faster way would be
reaching this termed postings list information on memory with data structure like
Dictionary. Also for query terms it’s fast to order terms document frequency
information and then merge postings. Using SPIMI instead of BSBI would be faster and if
we use cache mechanism we can increase the speed of query results. At my program
every time new query comes i check index and retrieve results but if we just cache
frequently asked queries we can have better retrieval performance.
