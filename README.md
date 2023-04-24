# py-finae

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