# belief-engine


### How to run the client
The client will allow the user to:
1) Add beliefs to the belief base (using the revision procedure of contraction + expansion)
2) Check if a given belief follows from the belief base
3) Check the resulting contraction of the belief base with a belief
4) Print the blief base
5) Resetting the belief base


**With confidence (ordering of beliefs is based on the confidence value specified by the user)**

```{bash}
python src/cli.py --confidence   
```

**Without confidence (ordering of beliefs is based on the gamma_o-function explained in the report)**

```{bash}
python src/cli.py
```

### How to run tests

**Postulates**
Tests the success, inclusion, relevance, uniformity, vacuity and consistency postulates.
```{bash}
python src/postulates.py  
```

**Pretyped belief base tests**
Tests the belief revision engine by sequentially adding a series of beliefs to the belief base.
Tests are run using both the gamma_o (rank-based) and gamma_c (confidence-based) selection functions.
```{bash}
python src/belief_base.py  
```

```