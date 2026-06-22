from fastapi import APIRouter, HTTPException, Request, Query


router = APIRouter()

@router.post("/inserat_with_ai")
async def inserat_with_ai(request: Request, query: str):
    agent = request.app.state.agent
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": query}
                ]
            },
            config={"configurable": {"thread_id": "1"}}
    )
    try:    
        return {"answer": result["messages"][-1].content}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
