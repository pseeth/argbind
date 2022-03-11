# Binding a module

ArgBind allows you bind an entire module, giving back an object that
behaves similarly to the original module, but has all of the
sub-modules and functions bound to the parser. This is useful if
you're working with a big package, but don't want to sprinkle the package
code with decorators for all the functions you care about. Instead, one can
do it all at once and get a package with everything bound as needed.

Let's start by using ArgBind to bind all the methods in `torch.optim`:

```python
import torch
import argbind

optim = argbind.bind_module(
    torch.optim, 
    filter_fn=lambda fn: hasattr(fn, "step")
)
args = {
    "lr": 2e-4,
    "args.debug": True,
}

net = torch.nn.Linear(1, 1)
for fn_name in dir(optim):
    if fn_name.startswith("_") or fn_name == "Optimizer":
        continue
    fn = getattr(optim, fn_name)
    args[f"{fn_name}.lr"] = args["lr"]
    with argbind.scope(args):
        fn(net.parameters())
```

A few things to note, `bind_module` takes (optionally) a `filter_fn`, 
which takes in the object, and returns a bool which indicates whether
or not it should be bound. You can use this to filter out any functions
or classes that you don't want bound. Here we use it to bind only
classes which have a `step` attribute (these are the optimizers).

Then we just write our script normally like any other ArgBind script.

**N.B.: `bind_module` only goes ONE level deep. It does not recursively apply
itself to bind submodules. This could happen in the future, but the 
logic must be done carefully to avoid loops cause by circular imports.**

For comparison, here is how the code would look without binding
the entire module, to achieve the same output:

```python
import torch
import argbind

# Binding all the optimizers
ASGD = argbind.bind(torch.optim.ASGD)
Adadelta = argbind.bind(torch.optim.Adadelta)
Adagrad = argbind.bind(torch.optim.Adagrad)
AdamW = argbind.bind(torch.optim.AdamW)
Adamax = argbind.bind(torch.optim.Adamax)
LBFGS = argbind.bind(torch.optim.LBFGS)
NAdam = argbind.bind(torch.optim.NAdam)
RAdam = argbind.bind(torch.optim.RAdam)
RMSprop = argbind.bind(torch.optim.RMSprop)
Rprop = argbind.bind(torch.optim.Rprop)
SGD = argbind.bind(torch.optim.SGD)
SparseAdam = argbind.bind(torch.optim.SparseAdam)

optimizers = [
    ASGD, Adadelta, Adagrad, AdamW, Adamax, LBFGS,
    NAdam, RAdam, RMSprop, Rprop, SGD, SparseAdam
]

class holder:
    def __init__(self):
        for o in optimizers:
            setattr(self, o.__name__, o)
optim = holder()

args = {
    "lr": 2e-4,
    "args.debug": True,
}

net = torch.nn.Linear(1, 1)

for fn_name in dir(optim):
    if fn_name == "Optimizer":
        continue
    fn = getattr(optim, fn_name)
    if hasattr(fn, "step"):
        args[f"{fn_name}.lr"] = args["lr"]
        with argbind.scope(args):
            fn(net.parameters())
```

In this script, every single function must be bound one by one, which
is rather tedious. `bind_module` is more succinct.