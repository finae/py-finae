# py-finae

FIANE is a new way to use/interactive with LLMs.

It's a framework thats make you write simple guidances/hints and extract massive structured and verified knowledge from LLMs.

The extracted data are native Python objects and can be used in any Python programs. You can also easily re-use, combine or share your extractions with others to create new ones.


### More about Finae

It's not people loving chatbots with long prompts, it's so far the best way for general public to enjoy the computing powers (so called AI).

Finae's vision is to create a new language (human-computer interface) in between natural language and Python (more concised than natural language, less rigorous than Python), and experiemnt a new programming paradigm, I call it **keyword-oriented** or **hint-oriented** programming.


### Design Ideas

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

## Dev

```
> pip install -e .
```


## For project owner/maintainer

### Publish to pip hub

```
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine

python3 -m build
twine check dist/*
twine upload dist/*
```