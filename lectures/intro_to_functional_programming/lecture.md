## (Intro to) Functional Programming in Python



## What is FP?
* A programming paradigm that treats computation as the evaluation of functions, and avoids changing state and mutable data <!-- .element: class="fragment" -->
* Contrast with: <!-- .element: class="fragment" -->
  * object-oriented programming, which is based on objects, which are collections of data (internal state) and code (methods) <!-- .element: class="fragment" -->
  * imperative programming, which performs computations through a sequence of steps, using variables and state <!-- .element: class="fragment" -->



## Functions
![function](images/function.png)

* A mapping of input -> output, with each input associated with exactly one output


## Functions
```py
def add(a, b):
  return a + b
```

```
>> add(1, 2)
3
>> add([1, 2], [3, 4])
[1, 2, 3, 4]
```


## First-class functions
* Functions can be treated as values and can be: <!-- .element: class="fragment" -->
  * created at runtime <!-- .element: class="fragment" -->
  * passed as arguments to other functions <!-- .element: class="fragment" -->
  * returned from other functions <!-- .element: class="fragment" -->
  * stored in data structures <!-- .element: class="fragment" -->


## First-class functions
```py
def exponentiator(n):
  def f(x):
    return x ** n
  return f

def g(f, x):
  return x * f(x)

```
<!-- .element: class="fragment" -->

```py
>>> square = exponentiator(2)
>>> square(2)
4
>>> cube = exponentiator(3)
>>> cube(2)
8
>>> g(square, 2)
8
>>> g(cube, 2)
16
```
<!-- .element: class="fragment" -->



## FP and problem decomposition
* This flexibility allows composition and combining of smaller functions <!-- .element: class="fragment" -->
* In FP, problems are decomposed into a set of functions, and input flows through them <!-- .element: class="fragment" -->
* Think about data, its flow and transformations <!-- .element: class="fragment" -->
* Contrast with OOP which decomposes instead into related objects <!-- .element: class="fragment" -->



## FP and purity
FP discourages side effects, or changes not visible in a function's return value, such as I/O, or changes to external state. <!-- .element: class="fragment" -->

```py
run_count = 0

def add(a, b):
  global run_count
  run_count += 1
  return a + b
```
<!-- .element: class="fragment" -->

Side-effect-free functions are called purely functional. <!-- .element: class="fragment" -->

```py
def add(a, b, prev_run_count):
  return (a + b, prev_run_count + 1)
```
<!-- .element: class="fragment" -->


## FP and purity
* Pure functions only depend on the provided input and return the same output for the same input every time <!-- .element: class="fragment" -->
* Functions with no side effects are easier to reason about, since you don't have to worry about unexpected behavior affecting other parts of the program or system <!-- .element: class="fragment" -->
* Pure functions typically operate on immutable data -- instead of altering existing values, altered copies are created and the original is preserved <!-- .element: class="fragment" -->


## FP and referential transparency
* Purity + immutability of data leads to referential transparency <!-- .element: class="fragment" -->
* This just means that a given expression always evaluates to the same result in any context <!-- .element: class="fragment" -->
* Removing side-effects from a unit means it'll work in any environment, and makes it easier to test, integrate, and compose units <!-- .element: class="fragment" -->


## Real-world purity
* Of course, in real-world applications, we need to do input/output and depend on external state. <!-- .element: class="fragment" -->
* The usual approach is to isolate these impure operations from a pure core. <!-- .element: class="fragment" -->



## Recursion
* Another characteristic of functional-style programming is the use of recursion instead of loops <!-- .element: class="fragment" -->
* The usual loop constructs (for/while) rely on loop counters, i.e., assignment and mutable variables <!-- .element: class="fragment" -->


## Recursion vs. iteration

```py
def factorial(n):
  res = 1
  for i in range(1, n + 1):
    res *= i
  return res
```

```py
def factorial(n):
  if n == 0:
    return 1
  return n * factorial(n - 1)
```
<!-- .element: class="fragment" -->


## Recursion vs. iteration
* Note that unlike functional languages, Python is not optimized for recursions.



## FP in Python
* Python provides features and built-in functions to support programming in a functional style <!-- .element: class="fragment" -->
  * `lambda` <!-- .element: class="fragment" -->
  * `map` <!-- .element: class="fragment" -->
  * `filter` <!-- .element: class="fragment" -->
  * `reduce` <!-- .element: class="fragment" -->
  * `functools` <!-- .element: class="fragment" -->



## `lambda`
* Alternative, more concise way to create functions <!-- .element: class="fragment" -->
* Any number of arguments, but must be a single expression (which is the return value), and fit on one line <!-- .element: class="fragment" -->


## `lambda`
```py
def add(a, b):
  return a + b

# Equivalently:
add = lambda a, b: a + b

def exponentiator(n):
  def f(x):
    return x ** n
  return f

# Equivalently:
exponentiator = lambda n: lambda x: x ** n
```


## `lambda`
Useful for creating one-off functions <!-- .element: class="fragment" -->

```py
>>> l = [dict(a=1, b=2), dict(a=3, b=6), dict(a=2, b=1)]
>>> sorted(l)
[{'a': 1, 'b': 2}, {'a': 2, 'b': 1}, {'a': 3, 'b': 6}]
>>> sorted(l, key=lambda d: d['b'])
>>> l
[{'a': 2, 'b': 1}, {'a': 1, 'b': 2}, {'a': 3, 'b': 6}]
```
<!-- .element: class="fragment" -->


## `lambda`
But for more complicated functions, just define a named function in the usual way.



## `map`
* Built-in function with two arguments: `map(function, sequence)` <!-- .element: class="fragment" -->
* Returns a new list containing the results of applying the given function to the elements of the sequence <!-- .element: class="fragment" -->


## `map`
Let's say we want to transform words in a list:

```py
>>> words = ['insync', 'really', 'rocks']
>>> upper_words = []
```

 ```py
>>> for word in words:
...   upper_words.append(word.upper() + '!')
>>> upper_words
['INSYNC!', 'REALLY!', 'ROCKS!']
```
 <!-- .element: class="fragment" -->

 ```py
>>> [word.upper() + '!' for word in words]
['INSYNC!', 'REALLY!', 'ROCKS!']
```
<!-- .element: class="fragment" -->

```py
>>> map(lambda w: w.upper() + '!', words)
['INSYNC!', 'REALLY!', 'ROCKS!']
```
<!-- .element: class="fragment" -->



## `filter`
* Similar built-in function with two arguments: `filter(function, sequence)` <!-- .element: class="fragment" -->
* Applies function to each element, and returns a list of elements that evaluate to True  <!-- .element: class="fragment" -->


## `filter`
```py
>>> nums = [1, 2, 3, 4, 5]
>>> even_nums = []
```

```py
>>> for num in nums:
...   if num % 2 == 0:
...     even_nums.append(num)
>>> even_nums
[2, 4]
```
 <!-- .element: class="fragment" -->

```py
>>> [num for num in nums if num % 2 == 0]
[2, 4]
```
 <!-- .element: class="fragment" -->

```py
>>> filter(lambda n: n % 2 == 0, nums)
[2, 4]
```
 <!-- .element: class="fragment" -->



## `reduce`
* Again, built-in function with two arguments: `reduce(function, sequence, [initial_value])`  <!-- .element: class="fragment" -->
* Cumulatively performs the function on elements of the sequence  <!-- .element: class="fragment" -->


## `reduce`
```py
>>> reduce(lambda a, x: a + x, [0, 1, 2, 3, 4])
10
```

`(0 + 1)`
<!-- .element: class="fragment" -->

`(0 + 1) + 2`
<!-- .element: class="fragment" -->

`((0 + 1) + 2) + 3 ...`
<!-- .element: class="fragment" -->


## `reduce`
```py
>>> reduce(lambda a, x: a + x, [0, 1, 2, 3, 4], 5)
15
```

`(5 + 0)`
<!-- .element: class="fragment" -->

`(5 + 0) + 1`
<!-- .element: class="fragment" -->

`((5 + 0) + 1) + 2 ...`
<!-- .element: class="fragment" -->



## `functools`
* Contain higher-order-functions that act on or return other functions


## `functools.partial`
* `functools.partial(function[, *args][, **kwargs])`
* Returns a new object which when called behaves like the given function with the supplied args and kwargs <!-- .element: class="fragment" -->
* Used for partial function application, which "freezes" some portion of a function's arguments, returning a simpler function <!-- .element: class="fragment" -->


## `functools.partial`

```py
>>> from functools import partial
>>> basetwo = partial(int, base=2)
>>> basetwo('10010')
18
>>> basethree = partial(int, base=3)
>>> basethree('10010')
84
```


## `functools.partial`
* Partial function application is useful for creating specialized functions from general functions



## Why do FP?
* A different paradigm with different ways to break down and solve problems <!-- .element: class="fragment" -->
* Encourages modularity <!-- .element: class="fragment" -->
* Ease of debugging and testing <!-- .element: class="fragment" -->
* Composability <!-- .element: class="fragment" -->
* Easier memoization and caching <!-- .element: class="fragment" -->
* Easier concurrency and usage of multiple cores/machines <!-- .element: class="fragment" -->
