# YAML support and features

In this example, we'll be using the following script:

- `examples/yaml/main.py`

and the following config files:

- `examples/yaml/conf/base.yml`
- `examples/yaml/conf/exp1.yml`
- `examples/yaml/conf/exp2.yml`

## Including other YAML files

ArgBind supports saving and loading arguments from `.yml` files. It also supports
including other `.yml` files within `.yml` files, in a limited way. 
This is enabled via the `$include` directive:

```yaml
$include:
    - examples/yaml/conf/base.yml

# Rest of experiment configuration
```

Multiple files can be included by putting more items in the list. 

**IMPORTANT**

If the files in 
the list also have `$include` directives in their contents, those `$include` 
directives will not be parsed. **That is to say, this is NOT recursive.**

This allows one to share a base configuration between multiple files. You can
override something inside the base without any issues as well. For example,
if `base.yml` looks like:

```yaml
func.arg1: a
func.arg2: b
```

And `exp.yml` includes `base.yml`:

```yaml
$include:
    - base.yml

func.arg1: c
```

Then, `func` will be called with `arg1='c', arg2='b'`. Let's look at the example
in `main.py`. The usage is:

```
❯ python examples/yaml/main.py -h
usage: main.py [-h] [--args.save ARGS.SAVE] [--args.load ARGS.LOAD] [--args.debug ARGS.DEBUG] [--func.arg1 FUNC.ARG1] [--func.arg2 FUNC.ARG2] [--func.arg3 FUNC.ARG3] [--func.arg4 FUNC.ARG4]

optional arguments:
  -h, --help            show this help message and exit
  --args.save ARGS.SAVE
                        Path to save all arguments used to run script to.
  --args.load ARGS.LOAD
                        Path to load arguments from, stored as a .yml file.
  --args.debug ARGS.DEBUG
                        Print arguments as they are passed to each function.

Generated arguments for function func:
  Dummy function for binding.

  --func.arg1 FUNC.ARG1
                        Argument 1, by default 'default'
  --func.arg2 FUNC.ARG2
                        Argument 2, by default 'default'
  --func.arg3 FUNC.ARG3
                        Argument 3, by default 'default'
  --func.arg4 FUNC.ARG4
                        Argument 4, by default 'default'
```

Let's run it using the default arguments:

```
❯ python examples/yaml/main.py
Argument 1: default
Argument 2: default
Argument 3: default
Argument 4: default
```

Let's run it using `conf/base.yml`:

```
❯ python examples/yaml/main.py --args.load examples/yaml/conf/base.yml
Argument 1: from base
Argument 2: from base
Argument 3: from base
Argument 4: from base
```

Now, let's try `conf/exp1.yml` which has the following contents:

```
$include:
  - examples/yaml/conf/base.yml
func.arg4: from exp1
```

The settings from `base.yml` are included in `exp1.yml` when we run this:

```
❯ python examples/yaml/main.py --args.load examples/yaml/conf/exp1.yml
Argument 1: from base
Argument 2: from base
Argument 3: from base
Argument 4: from exp1
```

You can see that Argument 4 is changed according to what is in `exp1.yml`, 
overriding what is in the `base.yml`.

## Using variables

Settings that are shared between different arguments can be defined once using the
`$vars` directive. If `$vars` is in a `.yml` file, then items within it 
can be accessed inside the `.yml` file by prefacing them with `$`. For example:

```yaml
$vars:
    reuse_arg: reuse
func.arg1: $reuse_arg
func.arg2: $reuse_arg
```

This is functionally equivalent to:

```yaml
func.arg1: reuse
func.arg2: reuse
```
**IMPORTANT**
Only the latest `$vars` will be used, if multiple files are included.

Let's take a look at `exp2.yml`:

```
$include:
  - examples/yaml/conf/base.yml
  - examples/yaml/conf/exp1.yml

$vars:
  reuse_arg: from exp2

func.arg1: $reuse_arg
func.arg2: $reuse_arg
```

Here, we are including two files. `exp1.yml` binds `func.arg4` to `from exp1`, and
`exp2.yml` binds `func.arg1` and `func.arg2` to `$reuse_arg`, which is resolved in
`$vars` to `from exp2`. This results in the following output:

```
❯ python examples/yaml/main.py --args.load examples/yaml/conf/exp2.yml
Argument 1: from exp2
Argument 2: from exp2
Argument 3: from base
Argument 4: from exp1
```
