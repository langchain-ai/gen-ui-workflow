from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import json
from sse_starlette.sse import EventSourceResponse
from graph.workflow import genui_graph
from graph.state import GraphState, ComponentNode

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateUIRequest(BaseModel):
    prompt: str


class GenerateUIResponse(BaseModel):
    component_tree: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


@app.post("/api/generate-ui", response_model=GenerateUIResponse)
async def generate_ui(request: GenerateUIRequest):
    """
    Generate UI components from a natural language prompt using recursive idea expansion.

    This endpoint:
    1. Takes a user prompt
    2. Generates a high-level component tree (may contain "ideas")
    3. Recursively expands ideas into concrete components
    4. Returns a fully expanded hierarchical component tree
    """
    try:
        # Create initial state
        initial_state: GraphState = {
            "user_prompt": request.prompt,
            "component_tree": None,
            "error": None,
        }

        # Run the graph (will recursively expand all ideas)
        result = await asyncio.to_thread(genui_graph.invoke, initial_state)

        return GenerateUIResponse(
            component_tree=result.get("component_tree"), error=result.get("error")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-ui/stream")
async def generate_ui_stream(request: GenerateUIRequest):
    """
    Stream complete state updates as the graph executes.

    This endpoint streams the full GraphState object after each node execution,
    allowing the frontend to observe the complete graph state evolution.
    """

    async def event_generator():
        try:
            initial_state: GraphState = {
                "user_prompt": request.prompt,
                "component_tree": None,
                "error": None,
            }

            # Stream graph execution - sends full state after each node
            async for event in genui_graph.astream(initial_state):
                # Each event is a dict of {node_name: complete_state}
                for node_name, state in event.items():
                    yield {
                        "event": "state_update",
                        "data": json.dumps(
                            {
                                "node": node_name,
                                "state": {
                                    "user_prompt": state.get("user_prompt"),
                                    "component_tree": state.get("component_tree"),
                                    "error": state.get("error"),
                                },
                            }
                        ),
                    }

            # Final completion event
            yield {
                "event": "done",
                "data": json.dumps({"status": "complete"}),
            }

        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)}),
            }

    return EventSourceResponse(event_generator())
