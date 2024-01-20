---
cssclasses:
  - my_style_width_100
---


## Data Structure Interfaces

> When discussing data structures, it is important to understand the difference between a data structure's interface and its implementation.

- A data strcuture is a way to store data, with algorithms that support operation on the data
- Collection of supported operation is called an interface
- Interface is a specification: what operations are supported(the problem)
- Data structuere is a representation: how operations are supported
- In this class, two main interfaces: Sequence and Set

> Data Structure is a way to store data, with algorithms that support operation on the data,
> COllection, interface, specification, representation 




## 🤔 What is Collection in datastructure
In computer programming, a collection is a grouping of some variable number of data items (possible zero) that have some shared significance to the problem being solved and need to be operated upon togehter in some controlled fashion

# Sequence Interface

- Maintain a sequence of items (order is extrinsic) 
- Ex:  $$x_0, x_1, x_2, \ldots, x_{n-1} $$
- (use n to denote the number of items stored in the data structure) 
- supports sequence oprations:

|  |  |  |
| ---- | ---- | ---- |
| Container | build(x) <br>len() | given an iterable X, build sequence from items in X <br>return the number of stored items |
| static | iter_seq()<br>get_at(i)<br>set_at(i,x) | return the sorted items one-by-one in sequence order<br>$$return \ the \  i^{th} $$$$replace \ the \ i^{th} \ item \ with \ x $$<br> |
| **Dynamic** | **insert_at(i, x)<br>delete_at(i)<br>insert_first(x)<br>delete_first()<br>insert_last(x)<br>delete_last** | **$$ \begin{align} add \ x \ the \ i^{th} \ item  \\ remove \ and \ return \ the \ i^{th} \ item \\ add \ x \ as \ the \ first \ item \\ remove \ and \ return \ the \ first \ item \\ add \ x \ as \ the \ last \ item \\ remove \ and \ return \ the \ last \ item  \end{align} $$** |
|  |  |  |

> Note that insert_ / delete_ operations change the rank of all items after the modified them.


> An Interface says what you want to do.
> A data structure says how you do it


## 🤔 What is Sequence Interface

The Sequence interface is interface that provide method that define or computation on sequential item


# Set Interface 
- Sequence about extrinsic order, set is abount intrinsic order
- Maintain a set of items having unique keys (.e.g , item x has key x. key) 
- Set or multi-set ? We restrict to unique keys for now.  
- Often we let key of an item be the item itself, but may wnat to store more info than just key

> By constract, Set maintain a collection of items based on an intrinsic property involving what the items are, usually based on a unique key, x.key, aassociated with each item x.
> Sets are generalizations of dictionaries and other insrinsic query databases.

![[Pasted image 20240119163650.png]]


# Sequence Implementations

Exists three data structures to implement the sequence interface.

## Problem Set1
You will extend both Linked Lists and Dynamic arrays to make both first and last dynamic operations O(1) time for each.  
Notice that none of these data structures support dynamic operations at arbitrary index in sub-linear time. 
-> Lecture 7에서 성능을 향상 시킬 수 있는지에 대해 배울 예정임

> 첫 번째와 마지막 요소에 대한 O(1) 시간 동적 작업은 연결 리스트와 동적 배열에서 이미 가능한 부분입니다. 그러나 임의의 인덱스에서의 서브-리니어 시간 동적 작업은 이러한 데이터 구조들에서 지원되지 않습니다. 

![[Pasted image 20240119164748.png]]

### What is sub-linear time
"서브-리니어(Sub-linear)"는 컴퓨터 과학과 수학에서 사용되는 용어로, 어떤 알고리즘 또는 연산이 데이터의 크기에 따라 선형적으로 증가하는 것보다 덜 빠르게 증가할 때 이를 묘사하는 데 사용됩니다. 예를 들어, 데이터 크기가 n일 때, 선형 시간은 O(n)으로 표현되며, 이는 작업 수행 시간이 데이터 크기에 비례하여 증가함을 의미합니다.

반면에, 서브-리니어 시간 알고리즘이란 O(n)보다 더 효율적인, 즉 데이터 크기에 선형적으로 비례하지 않고 더 적게 증가하는 시간 복잡도를 갖는 알고리즘을 의미합니다. 예를 들어 O(log n) 또는 O(sqrt(n))과 같은 시간 복잡도는 서브-리니어입니다. 이러한 알고리즘들은 데이터가 커질수록 선형 알고리즘에 비해 상대적으로 덜 시간이 걸립니다.

간단히 말해, 서브-리니어 시간은 데이터 양이 증가할수록 필요한 처리 시간이 데이터 양의 증가율보다 덜 증가하는 경우를 말합니다.

# Array Sequence

Computer memory is a finite resource. On modern computers many processes may share the same main memory store, so an operating system will assign a fixed chunk of memory addresses to each active process.

The amount of memory assigned depends on the needs of the process and the avialability of free memory. 

For example, when a computer program makes a request to store a variable, the program must tell the operating system how much momory will be required to store it.  To fullfill the request, the operating system will find the avaialbe memory in the process's assigned memory address space and reserve it for that purpose until it is no longer needed. 

Memory management and allocation 


# Reference

[data structure interface ](https://opendatastructures.org/ods-java/1_2_Interfaces.html)