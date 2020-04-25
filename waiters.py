from database import Users
from pyromod.helpers import ikb

funcs = {}

def create_waiter(waiting_for, filters=None):
    def decorator(func):
        funcs[waiting_for] = {"func": func, filters: filters}
        return func
    return decorator

 
