# belief-engine


### How to run the client
The client will allow the user to:
1) Add beliefs to the belief base (using the revision procedure of contraction + expansion)
2) Check if a given belief follows from the belief base
3) Check the resulting contraction of the belief base with a belief
4) Print the blief base
5) Resetting the belief base


**With confidence**

```{bash}
python src/cli.py --confidence   
```

**Without confidence**

```{bash}
python src/cli.py
```

### How to run tests

**Postulates**
```{bash}
python src/postulates.py  
```

**Pretyped belief base tests**
```{bash}
python src/belief_base.py  
```

```