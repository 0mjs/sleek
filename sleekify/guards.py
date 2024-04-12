from asyncio import iscoroutinefunction
from typing import Awaitable, Callable, Dict, Union

from starlette.responses import JSONResponse

TRouter = Callable[..., Awaitable[Union[JSONResponse, Dict]]]


class Guard:
    def __init__(self, router: TRouter, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.router = router

    async def resolve(self):
        if iscoroutinefunction(self.router):
            return await self.router(*self.args, **self.kwargs)
        else:
            return self.router(*self.args, **self.kwargs)
