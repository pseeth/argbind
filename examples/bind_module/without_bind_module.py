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

if __name__ == "__main__":
    argbind.parse_args()
    
    net = torch.nn.Linear(1, 1)
    for fn_name in dir(optim):
        if fn_name == "Optimizer":
            continue
        fn = getattr(optim, fn_name)
        if hasattr(fn, "step"):
            args[f"{fn_name}.lr"] = args["lr"]
            with argbind.scope(args):
                fn(net.parameters())

