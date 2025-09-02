# LSM Trees

B and B+ trees are great for reads, but often slow for writes. LSM trees are used by databases that need fast writes (analytics, social media etc.). These are basically a structure that makes it nice for buffering writes. We pre-reserve a chunk on disk, and write a log to it as we fill up a buffer, then when it's full we flush the buffer to an SSTable on disk. This is also combined with other fancier data structures like [bloom filters](https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/) to make this whole process more efficient.

## References

- LSM Trees & SSTables
  - Microsoft
    - [An efficient design and implementation of LSM-tree based key-value store on open-channel SSD](https://www.microsoft.com/en-us/research/publication/an-efficient-design-and-implementation-of-lsm-tree-based-key-value-store-on-open-channel-ssd/)
    - [Scaling Write-Intensive Key-Value Stores](https://www.microsoft.com/en-us/research/video/scaling-write-intensive-key-value-stores/)
  - [LSM Trees | Writing to databases at scale (youtube.com)](https://www.youtube.com/watch?v=MbwmMCu9ltg)
  - [LSM Tree + SSTable Database Indexes | Systems Design Interview: 0 to 1 with Google Software Engineer (youtube.com)](https://www.youtube.com/watch?v=ciGAVER_erw)
  - [p2085-alkowaileet.pdf (vldb.org)](https://www.vldb.org/pvldb/vol15/p2085-alkowaileet.pdf)
  - [Log Structured Merge Trees - ben stopford](http://www.benstopford.com/2015/02/14/log-structured-merge-trees/)
  - [Elasticsearch from the Bottom Up, Part 1 | Elastic Blog](https://www.elastic.co/blog/found-elasticsearch-from-the-bottom-up)
  - [Storage engine | Apache Cassandra 3.x (datastax.com)](https://docs.datastax.com/en/cassandra-oss/3.x/cassandra/dml/dmlManageOndisk.html)
  - [How Cassandra Stores Data: An Exploration of Log Structured Merge Trees | HackerNoon](https://hackernoon.com/how-cassandra-stores-data-an-exploration-of-log-structured-merge-trees)
  - [B-TREE v/s LSM TREE (youtube.com)](https://www.youtube.com/watch?v=nMVJIk_MDu4)
  - [The Secret Sauce Behind NoSQL: LSM Tree (youtube.com)](https://www.youtube.com/watch?v=I6jB0nM9SKU)
  - [System Design: LSM Trees | Data Structure Behind Google and Facebook Storage Engine (youtube.com)](https://www.youtube.com/watch?v=P2xtlLymqqI)
