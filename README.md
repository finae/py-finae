# py-finae

Finae is a new programming paradigm (like Python + AI) to make coding easy/flexible for everyone.

It's a framework that you write simple guidance to generate scenario UIs and use them to approach to the final a complex app/program iteratively.

It's also a framework where you can write simple guidances/hints and extract massive structured and verified knowledge from LLMs. The extracted data are native Python objects and can be used in any Python programs. You can also easily re-use, combine or share your extractions with others to create new ones.

### More thoughts behind Finae

It's not people loving chatbots, long conversations or sophisticated prmopts. It's just so far the best/easist intereface for people to enjoy rich computing powers (AI).

Finae's vision is to create a new human-computer interaction in-between natural language and Python (rigorous than natural language, concised than Python), so called **keyword-oriented** or **hint-oriented** programming styles.

### Design Ideas

#### Finae class is called concept.


```python
@finae.Concept
class Mountain:
    ...
```
#### Concept Examples
Mountain

```python
m = Mountain('give me any mountain in this world')
print(m.name())

m = Mountain('Highest mountain in the world')
print(m.altitude())

m = Mountain('Mount Everest')
print(m.altitude())

mountains = Mountain.query('Top 50 mountains in the wolrd')
for m in mountains:
    print(m.name())
```

Integer/Float

```python
i = Integer('give me a code generate integer in python')
i = Integer('show me an example of Python integer')
i = Integer('show me an example of Python float')
```

Date
```python
d = Date('independence day of United States')
print(d)

d = Date('1995/03/01')
print(d)

d = Date('03-01-1995')
print(d)

d = Date('year 1995, March, first')
print(d)

d = Date('the day after 1995/03/01')
print(d)

d = Date('the day after ', d)
print(d)
```


Array
```python
a = Array('[1, 2, 3, 4]')
print(a)

a = Array('1, 2, 3, 4')
print(a)

a = Array('1 2 5 6 10')
print(a)

a = Array('1 to 4')
print(a)

a = Array('1 to 4, inclusive')
print(a)

a = Array('give me an array of integer, length less than 20')
print(a)

```


Numpy, pandas
```python
n = Numpy('give me a numpy array, length 10')
print(n)

n = Numpy("""
1 2 3
4 5 6
7 8 9
""")
print(n)

t = PandasTable('Pandas table, columns: name, school, age')
print(t)

t = PandasTable("""
name school age
foo    A    y
bar    B    z
""")
print(t)
```



#### Finae concept memories samples it has processed

E.g. up to 100 for example, and ranked by some scores, keep LRU.

```python
for m in Mountain.samples():
    print(m)
```

#### Finae concept memories/caches the way it parses the input.

The cache is local database file or py that can be checked-in to codebase and version-controlled. (Or delete if want to drop the cache.)


```python
d = Date('independence day of United States')
d = Date('independence day of United States')  # read from cache
d = Date('independence day of United States')  # read from cache
```

## Install

```
> pip install -e .
```


## Owner/maintainer

### Publish to pip hub

```
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine

python3 -m build
twine check dist/*
twine upload dist/*
```