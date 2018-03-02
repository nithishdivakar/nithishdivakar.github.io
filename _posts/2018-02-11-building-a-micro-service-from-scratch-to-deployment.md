---
layout: post
title: Building a micro service from scratch to deployment
date: 2018-02-11 12:08 +0530
comments: true
share: true
---


So you have implemented your super complicated algorithm. BUT, it is still only code. It cannot take more than one input at a time. Showing it to others involves running a program in command line. And you have no idea how to fit it as a small block in a larger system. 
Wh you need is to build a micro services around it.

## What do I have to Do?

Its simple.  You put a queue in front of your algorithm and you are done. Thigns which needs computing goes into this queue and they wait till results come. Your algorithm simply goes over the queue, computing and removing each requests. This is the folder structure.
<pre>
.
|-- algorithm
|   |-- __init__.py
|   `-- my_implementation.py
|-- requirements.txt
`-- run_as_service.py

</pre>
The `my_implementation.py` file contains your algorithm. implemented as if it take one argument and simply returns the result. The only constraint is, the input argument and the outut argument need to be a python dictionary. To say in simple terms.

```python
def foo(a):
  return a+10
```
becomes
```python
def foo(D):
  a = D['a']
  return {'output':a+10}
```
Ofcourse you can modify everything, but the patterns remains same. Dictionary in, dictionary out. Evrything else in this post is fire and forget. This is all you have to care about.

## Producer, Consumer and a Queue

The `run_as_service.py` is where all the magic happens. We will use redis for our queue and flask for building a api. Lets begin with installing all dependencies. 

### installing redis
The following sequence of commands will install redis on your system

```
curl -OL -C - http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo make install
```

### python packages
The following commands will install all python dependencies.

```
pip install flask gevent requests redis
```

In this post
