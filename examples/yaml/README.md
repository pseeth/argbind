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
directives will also be parsed, allowing you to maintain a hierarchy
of configuration files as needed, without excessively long `$include`
sections.

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
Argument 5: ['default']
```

Let's run it using `conf/base.yml`:

```yaml
func.arg1: from base
func.arg2: from base
func.arg3: from base
func.arg4: from base
func.arg5: 
  - from base
```

```
❯ python examples/yaml/main.py --args.load examples/yaml/conf/base.yml
Argument 1: from base
Argument 2: from base
Argument 3: from base
Argument 4: from base
Argument 5: ['from base']
```

Now, let's try `conf/exp1.yml` which has the following contents:

```yaml
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
Argument 5: ['from base']
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

```yaml
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
Argument 5: ['from base']
```

As usual, we can override arguments from the command line:

```
❯ python examples/yaml/main.py --args.load examples/yaml/conf/exp2.yml --func.arg2 "from command line"
Argument 1: from exp2
Argument 2: from command line
Argument 3: from base
Argument 4: from exp1
Argument 5: ['from base']
```

Variables can also be replaced within a list. For example, `exp3.yml` has the
following contents:

```yaml
$include:
  - examples/yaml/conf/base.yml
  - examples/yaml/conf/exp1.yml

$vars:
  reuse_arg: from exp3
  reuse_arg2: from exp3 again 

func.arg1: $reuse_arg
func.arg2: $ARGBIND_ENV_VAR
func.arg5:
  - $reuse_arg
  - $reuse_arg2
```

`func.arg5` is a list containing values with `$` at the beginning. Each value
in the list that beings with `$` is replaced with the corresponding
entry in `$vars`:

```
❯ python examples/yaml/main.py --args.load examples/yaml/conf/exp3.yml
Argument 1: from exp3
Argument 2: from environment variable
Argument 3: from base
Argument 4: from exp1
Argument 5: ['from exp3', 'from exp3 again']
```

## Using environment variables

By default, if a value includes a `$`, it is looked up in the set of current 
environment variables. For example, in `exp4.yml`, we have:

```yaml
$include:
  - examples/yaml/conf/base.yml
  - examples/yaml/conf/exp1.yml

$vars:
  reuse_arg: from exp4

func.arg1: $reuse_arg
func.arg2: $ARGBIND_ENV_VAR
func.arg5:
  - $reuse_arg
  - $ARGBIND_ENV_VAR
```

`func.arg2` resolves to `$ARGBIND_ENV_VAR`, which is not in `$vars`. So it 
is instead looked up in the environment variables. Running it without 
setting the environment variable results in:

```
❯ python examples/yaml/main.py --args.load examples/yaml/conf/exp4.yml
$reuse_arg
$ARGBIND_ENV_VAR
examples/yaml/conf/base.yml
Argument 1: from exp4
Argument 2: $ARGBIND_ENV_VAR
Argument 3: from base
Argument 4: from exp1
Argument 5: ['from exp4', '$ARGBIND_ENV_VAR']
```

If we export the environment variable first, we see that Argument 2 resolves
to the value in the environment variable:

```
❯ export ARGBIND_ENV_VAR="from environment variable"
❯ python examples/yaml/main.py --args.load examples/yaml/conf/exp4.yml
Argument 1: from exp4
Argument 2: from environment variable
Argument 3: from base
Argument 4: from exp1
Argument 5: ['from exp4', 'from environment variable']
```

Argument 5 uses a mix of variables sourced from `$vars` and from 
environment variables.
