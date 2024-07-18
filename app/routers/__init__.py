from importlib import import_module
from fastapi import FastAPI
import os

me = "routers"


def include_routers(app: FastAPI):
    for file in os.listdir(me):
        if os.path.isdir(os.path.join(me, file)) and file != "__pycache__":
            module = import_module(f"{me}.{file}")
            app.include_router(module.router)