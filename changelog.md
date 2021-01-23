# Changelog
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

