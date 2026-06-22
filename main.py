from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import (
    inserate_ultra as inserate,
    inserat,
    inserate_detailed_ultra as inserate_detailed,
    inserate_batch,
    convert_url,
    inserate_by_url,
    inserat_with_ai


)
from utils.browser import OptimizedPlaywrightManager
from utils.asyncio_optimizations import EventLoopOptimizer


from langchain.agents import create_agent

from ai.tools.ai_query import build_search_tool
from ai.config.settings import settings
from ai.config.prompts import load_prompt

from redis.asyncio import Redis
from langgraph.checkpoint.redis import AsyncRedisSaver

from ai.config.settings import settings
# Global browser manager instance for sharing across all endpoints
browser_manager = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown events"""
    global browser_manager

    # Setup uvloop for maximum performance (2-4x improvement)
    uvloop_enabled = EventLoopOptimizer.setup_uvloop()

    # Optimize event loop settings
    EventLoopOptimizer.optimize_event_loop()

    # Startup: Initialize shared browser manager with optimized settings
    browser_manager = OptimizedPlaywrightManager(max_contexts=20, max_concurrent=10)
    await browser_manager.start()

    client = Redis(
        host=settings.redis_config.host,
        port=settings.redis_config.port, 
    )

    saver = AsyncRedisSaver(redis_client=client)
    await saver.asetup()
    
    tool = build_search_tool(browser_manager)
    agent = create_agent(
        model=settings.agent_config.model, 
        tools=[tool], 
        system_prompt=load_prompt("system"),
        checkpointer=saver
        )

    # Store browser manager in app state for access by routers
    app.state.browser_manager = browser_manager
    app.state.uvloop_enabled = uvloop_enabled
    app.state.agent = agent
    yield

    # Shutdown: Clean up browser resources
    if browser_manager:
        await browser_manager.close()


app = FastAPI(version="1.0.0", lifespan=lifespan)


@app.get("/")
async def root(): 
    return {
        "message": "Welcome to the Kleinanzeigen API",
        "endpoints": ["/inserate", "/inserat/{id}", "/inserate-detailed"],
        "status": "operational",
    }


app.include_router(inserate.router)
app.include_router(inserat.router)
app.include_router(inserate_detailed.router)
app.include_router(inserate_batch.router)
app.include_router(convert_url.router)
app.include_router(inserate_by_url.router)
app.include_router(inserat_with_ai.router)
