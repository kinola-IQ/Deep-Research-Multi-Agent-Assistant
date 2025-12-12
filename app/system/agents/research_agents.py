from llama_index.core.agent.workflow import FunctionAgent, ReActAgent
from ..tools import search_web, record_notes
from ..model.model_loader import model


# instantiating model
llm = model

# instantiating the agents
question_agent = FunctionAgent(
    tools=[],
    llm=llm,
    verbose=False,
    system_prompt="""You are part of a deep research system.
      Given a research topic, you should come up with a bunch of questions
      that a separate agent will answer in order to write a comprehensive
      report on that topic. To make it easy to answer the questions separately,
      you should provide the questions one per line. Don't include markdown
      or any preamble in your response, just a list of questions."""
)

research_agent = FunctionAgent(
    system_prompt=(
        "You are the ResearchAgent that can search the web for\
        information on a given topic and record notes on the topic. "
        "Once notes are recorded, you should hand off \
        control to a seperate Agent to write a report on the topic."
        "if search results turn up empty, signify without fail."
    ),
    llm=llm,
    tools=[search_web, record_notes],
    verbose= False
)
