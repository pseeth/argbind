# Changelog
## v0.3.3
- Allow `argbind.load_args` to take in an already open filestream.

## v0.3.2
- Better way of binding classes.
- Using `__qualname__` instead of `__name__` to identify functions more reliably.
- Classes are bound by replacing their `__init__` function with an argbound version.
- Binding `__init__` functions uses as the prefix the name of the class, rather than `__init__`.

## v0.2.0
- Fixed a bug in resolving variables in lists, introduced in v0.1.8. 

## v0.1.9
- Positional arguments can now be bound with `positional=True`. ArgBind should now be able to build programs
  with identical APIs to ArgParse, with less code and added support for .yaml files!

## v0.1.8
- Environment variables can now be referenced within YAML files. All variables that are in `os.environ` are used to resolve any values that start with `$` in a YAML file.
- Variables now resolve not only for strings but also within lists of strings.

## v0.1.7
- Updated the behavior of `args.debug` to create a prettier and more readable 
  output.

## v0.1.6
- Added `without_prefix` option to `bind`, which exposes the keyword arguments
  without the function name as the prefix, if `without_prefix=True`. There was 
  an unused version of this in its place called `no_global` which has now been
  removed.

## v0.1.5
- Using `functools.wraps` in the `bind` decorator. This decorates the 
  function without changing its name.

## v0.1.4
- `bind_to_parser` renamed to `bind`. `bind_to_parser` still exists
  to maintain backwards compatibility.

## v0.1.3
- Stable release.

## v0.1.2
- Removing unused functionality.

## v0.1.1
- Fixing some minor bugs.

## v0.1.0
- Initial release.

