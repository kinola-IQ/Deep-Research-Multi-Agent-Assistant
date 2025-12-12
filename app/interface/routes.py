"""module to handle endpoint routing"""
import json
from fastapi import HTTPException, APIRouter
from fastapi.responses import StreamingResponse

# third party / local imports (make sure names match your package)
from ..system.agents.research_agents import question_agent, research_agent
from ..system.agents.write_agents import report_agent
from ..system.agents.review_agents import review_agent   # corrected name
from ..system.agents.workflow import WorkflowClass
from ..system.utils.events import ProgressEvent
from ..system.utils.schema import UserRequest, AgentResponse
from ..system.model.model_loader import model
from ..system.utils.logger import logger


router = APIRouter()


async def _sse_generator(handler):
    """
    Asynchronous Server-Sent Events generator\
    that streams ProgressEvent messages
    and finally emits the final result as a JSON event.\
    Yields properly formatted
    SSE "data: <json>\n\n" blocks.
    """
    try:
        # stream progress events (if handler exposes an async iterator)
        if hasattr(handler, "stream_events"):
            async for event in handler.stream_events():
                if isinstance(event, ProgressEvent):
                    payload = {"type": "progress", "message": event.msg}
                    yield f"data: {json.dumps(payload)}\n\n"

        # await final result
        final_result = await handler
        payload = {"type": "final", "response": final_result}
        yield f"data: {json.dumps(payload)}\n\n"

    except Exception as exc:
        logger.exception("Error while running agent handler")
        payload = {"type": "error", "error": str(exc)}
        yield f"data: {json.dumps(payload)}\n\n"


@router.post("/agent", response_model=AgentResponse)
async def query_agent(query: UserRequest):
    """
    Synchronous-style return (waits for full result, returns AgentResponse).
    Use this if the client expects a single JSON response.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="model not loaded yet")

    workflow = WorkflowClass(timeout=300)
    try:
        handler = workflow.run(
            research_topic=query.text,
            question_agent=question_agent,
            answer_agent=research_agent,
            report_agent=report_agent,
            review_agent=review_agent,
        )

        # handler is expected to be awaitable (await handler -> final_result)
        final_result = await handler
        return AgentResponse(response=final_result)

    except Exception as exc:
        logger.exception("Agent query failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/agent/stream")
async def query_agent_stream(query: UserRequest):
    """
    Streaming endpoint using Server-Sent Events (SSE).
    Clients can connect and receive progress messages\
    and then the final result.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="model not loaded yet")

    workflow = WorkflowClass(timeout=300)
    try:
        handler = workflow.run(
            research_topic=query.text,
            question_agent=question_agent,
            answer_agent=research_agent,
            report_agent=report_agent,
            review_agent=review_agent,
        )

        return StreamingResponse(_sse_generator(handler),
                                 media_type="text/event-stream")

    except Exception as exc:
        logger.exception("Agent stream failed")
        raise HTTPException(status_code=500, detail=str(exc))
