# py-finae

FIANE is a new programming paradigm powred by LLMs.

It's a framework thats make you write simple guidances (in python class) and extract massive structured and validated knowledge from LLMs.

The extracted knowledge are expressed in native python objects so can be used in any python programs.

You can also easily re-use, combine or share your extractions with others to create new ones.


## Dev

```
> pip install -e .
```


## Publish to pip instructions

```
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine

python3 -m build
twine check dist/*
twine upload dist/*
```