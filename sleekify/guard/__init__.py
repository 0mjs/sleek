from typing import Callable, Awaitable, Any
from asyncio import iscoroutinefunction as is_async


class Guard:
    def __init__(self, router: Callable[..., Awaitable[Any]], *args, **kwargs):
        self.router = router
        self.args = args
        self.kwargs = kwargs

    async def resolve(self):
        if is_async(self.router):
            return await self.router(*self.args, **self.kwargs)
        else:
            return self.router(*self.args, **self.kwargs)
