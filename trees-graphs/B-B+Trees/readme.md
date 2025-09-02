# B & B+ Trees

B & B+ Trees are special types of trees optimized for retrieving chunks of data at a time. This makes them effective for retrieving data from a disk, or cache. Because **random access** is slow on harddrives you want to retrieve chunks as much as you can. With a binary search tree the leaves of a node could be stored in separate blocks anywhere on the disk, which means you might have to physically wait for the drive head to spin in order to reach the leaf.

Both B and B+ tree's are balanced trees, this basically means they will try to balance themselves out in terms of numbers of leaves before increasing depth. This is complicated to do often, and the B-tree method is especially complex. I would look at [avl trees](https://en.wikipedia.org/wiki/AVL_tree) to understand how this works. 

## B Trees

B trees are similar to binary trees however they are able to have more than 2 leaves per node. Very important is that it's search time is `log(n)`, meaning with 1 million elements in the tree you're looking at `log(1,000,000) = 6` checks to search.

### Properties of B-Tree

- All leaves are at the same level.
- B-Tree is defined by the term minimum degree `t`. The value of `t` depends upon disk block size.
- Every node except the root must contain at least t-1 keys. The root may contain a minimum of $1$ key.
- All nodes (including root) may contain at most ($2*t - 1$) keys.
- Number of children of a node is equal to the number of keys in it plus $1$.
- All keys of a node are sorted in increasing order. The child between two keys $k1$ and $k2$ contains all keys in the range from $k1$ and $k2$.
- B-Tree grows and shrinks from the root which is unlike Binary Search Tree. Binary Search Trees grow downward and also shrink from downward.
- Like other balanced Binary Search Trees, the time complexity to search, insert, and delete is `O(log n)`.
- Insertion of a Node in B-Tree happens only at Leaf Node.

### Example

Running `b-tree.py`:

```
tree constructed with
        t: 16
        Max Value: 100000
        Minimum Height: 3
        Maximum Height: 4
        Minimum keys per level: 15
        Maximum Keys per level: 31
        Approximate Average Searches: 13.0
        Approximate Maximum Searches: 47.0

Keys in result row:
        [(2128, 44528), (2129, 14737), (2130, 96332), (2131, 46746), (2132, 8890), (2133, 8479), (2134, 12021), (2135, 88073), (2136, 97567), (2137, 23655), (2138, 86609), (2139, 28736), (2140, 91477), (2141, 63495), (2142, 45463)]
Took 4 checks to find 2131

==============================================

tree constructed with
        t: 16
        Max Value: 100000
        Minimum Height: 3
        Maximum Height: 4
        Minimum keys per level: 15
        Maximum Keys per level: 31
        Approximate Average Searches: 13.0
        Approximate Maximum Searches: 47.0

Keys in result row:
        [(9808, 26544), (9809, 74331), (9810, 75853), (9811, 38723), (9812, 64392), (9813, 19916), (9814, 25693), (9815, 9620), (9816, 30289), (9817, 36897), (9818, 10790), (9819, 153), (9820, 15516), (9821, 44313), (9822, 7092)]
Took 12 checks to find 9819


==============================================

tree constructed with
        t: 16
        Max Value: 100000
        Minimum Height: 3
        Maximum Height: 4
        Minimum keys per level: 15
        Maximum Keys per level: 31
        Approximate Average Searches: 13.0
        Approximate Maximum Searches: 47.0

Keys in result row:
        [(30528, 35624), (30529, 17248), (30530, 95250), (30531, 60293), (30532, 87962), (30533, 40520), (30534, 86764), (30535, 80835), (30536, 12482), (30537, 21289), (30538, 71669), (30539, 88331), (30540, 1596), (30541, 13741), (30542, 50675)]
Took 4 checks to find 30531

==========================
tree constructed with
        t: 16
        Max Value: 100000
        Minimum Height: 3
        Maximum Height: 4
        Minimum keys per level: 15
        Maximum Keys per level: 31
        Approximate Average Searches: 13.0
        Approximate Maximum Searches: 47.0

Keys in result row:
        [(31296, 85408), (31297, 95173), (31298, 25326), (31299, 86865), (31300, 73503), (31301, 56158), (31302, 54721), (31303, 93578), (31304, 18064), (31305, 70367), (31306, 11877), (31307, 85053), (31308, 24404), (31309, 26056), (31310, 8672)]
Took 12 checks to find 31307
```

## B+ trees

B+ trees make 1 small adjustment to B trees. The values in the parent nodes can also be found in the leaf nodes. This is only a slight difference, but it does help optimize since people rarely fill a B-tree to begin with.

![](./drawings.excalidraw.svg)



## References

- Red-black trees
  - [Red-black trees in 4 minutes — Intro (youtube.com)](https://www.youtube.com/watch?v=qvZGUFHWChY)
  - [Lec 10 | MIT 6.046J / 18.410J Introduction to Algorithms (SMA 5503), Fall 2005 (youtube.com)](https://www.youtube.com/watch?v=O3hI9FdxFOM)
  - [R2. 2-3 Trees and B-Trees (youtube.com)](https://www.youtube.com/watch?v=TOb1tuEZ2X4)
  - [Algorithms - Red-Black Trees - Lecture 5 (youtube.com)](https://www.youtube.com/watch?v=hm2GHwyKF1o)
  - [Red/Black Tree Visualization (usfca.edu)](https://www.cs.usfca.edu/~galles/visualization/RedBlack.html)
- AVL trees
  - [intro](https://www.geeksforgeeks.org/introduction-to-avl-tree/)
  - [visualization](https://www.cs.usfca.edu/~galles/visualization/AVLtree.html)
  - [AVL Trees Simply Explained (youtube.com)](https://www.youtube.com/watch?v=zP2xbKerIds)
  - [AVL trees in 5 minutes — Intro & Search (youtube.com)](https://www.youtube.com/watch?v=DB1HFCEdLxA)
  - [10.1 AVL Tree - Insertion and Rotations (youtube.com)](https://www.youtube.com/watch?v=jDM6_TnYIqE)
  - [Lecture 6: AVL Trees, AVL Sort (youtube.com)](https://www.youtube.com/watch?v=FNeL18KsWPc)
  - [AVL Trees & Rotations (Self-Balancing Binary Search Trees) (youtube.com)](https://www.youtube.com/watch?v=vRwi_UcZGjU)
- B-trees
  - [Understanding B-Trees: The Data Structure Behind Modern Databases - YouTube](https://www.youtube.com/watch?v=K1a2Bk8NrYQ)
  - [B Tree in Python](https://www.geeksforgeeks.org/b-tree-in-python/)
  - [B-trees in 4 minutes — Intro (youtube.com)](https://www.youtube.com/watch?v=FgWbADOG44s)
  - Benchmarks
    - [Stack overflow](https://stackoverflow.com/questions/6211118/b-trees-vs-binary-trees)
    - [Panthema](https://panthema.net/2007/stx-btree/speedtest/)
  - [Introduction of B Tree](https://www.geeksforgeeks.org/introduction-of-b-tree-2/)
  - [B-Tree Visualization (usfca.edu)](https://www.cs.usfca.edu/~galles/visualization/BTree.html)
  - [B-tree - Gnarley trees | visualization of algorithms and data structures (kubokovac.eu)](https://kubokovac.eu/gnarley-trees/Btree.html)
  - [database - PostgreSQL & SQL Server btree storage fundamentals question - Stack Overflow](https://stackoverflow.com/questions/5294193/postgresql-sql-server-btree-storage-fundamentals-question)
- B+ Trees
  - [Introduction of B+ tree](https://www.geeksforgeeks.org/introduction-of-b-tree/)
  - [B+ Tree Visualization (usfca.edu)](https://www.cs.usfca.edu/~galles/visualization/BPlusTree.html)
  - [JavaScript B+ Tree (goneill.co.nz)](https://goneill.co.nz/btree-demo.php)
  - [B-Tree Tutorial - An Introduction to B-Trees (youtube.com)](https://www.youtube.com/watch?v=C_q5ccN84C8)
  - [10.2 B Trees and B+ Trees. How they are useful in Databases (youtube.com)](https://www.youtube.com/watch?v=aZjYr87r1b8)
  - [B-tree vs B+ tree in Database Systems (youtube.com)](https://www.youtube.com/watch?v=UzHl2VzyZS4)
  - [B-Tree & B*-Tree Explained - Algorithms & Data Structures #23 (youtube.com)](https://www.youtube.com/watch?v=hMGhs63sCO0)
  - [performance - B trees vs binary trees - Stack Overflow](https://stackoverflow.com/questions/6211118/b-trees-vs-binary-trees)
  - [BTree vs Binary Tree - YouTube](https://www.youtube.com/watch?v=NVU3Jlab3T0)
  - [The B-tree implementations used in a lot of databases have tweaks, but they are ... | Hacker News (ycombinator.com)](https://news.ycombinator.com/item?id=6228549)
  - Postgres
    - [postgres/src/backend/access/nbtree/README at master - postgres/postgres (github.com)](https://github.com/postgres/postgres/blob/master/src/backend/access/nbtree/README)
    - [postgres/src/backend/access/nbtree at master - postgres/postgres (github.com)](https://github.com/postgres/postgres/tree/master/src/backend/access/nbtree)
  - Microsoft
    - [SQL Server and Azure SQL index architecture and design guide - SQL Server | Microsoft Learn](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-index-design-guide?view=sql-server-ver16)
    - [How to create B+ tree index Microsoft SQL - Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/620224/how-to-create-b-tree-index-microsoft-sql)
    - [Maintaining indexes optimally to improve performance and reduce resource utilization - SQL Server | Microsoft Learn](https://learn.microsoft.com/en-us/sql/relational-databases/indexes/reorganize-and-rebuild-indexes?view=sql-server-ver16)
- B trees and Drives
  - [How Do Databases Store Tables on Disk? Explained both SSD & HDD (youtube.com)](https://www.youtube.com/watch?v=DbxddGtHl70)
  - [B-Trees on Disk (Database internals) (youtube.com)](https://www.youtube.com/watch?v=dTfR0S_rBGg) (Really good video)
  - [Why do databases store data in B+ trees? (youtube.com)](https://www.youtube.com/watch?v=09E-tVAUqQw)
  - [B-Tree Indexes (youtube.com)](https://www.youtube.com/watch?v=NI9wYuVIYcA)
  - [B-Tree Indexing on databases: The Ultimate Guide [2023] (youtube.com)](https://www.youtube.com/watch?v=bOFlJ0oUjU4)

