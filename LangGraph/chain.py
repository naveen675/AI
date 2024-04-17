async def generate(
        state: GraphState
    ) -> Dict[
        str,
        Union[
            str, 
            List[int],
            List[str]
        ]
    ]:

    """
    Generates a response after context has been retrieved.

    Args:
        state (messages): The current state of the agent.
    Returns:
        dict: The output key is filled.
    """

    agent_output = state["agent_outcome"]    
    inputs = agent_output.tool_input
    docs = state["docs"]

    output = await chain.ainvoke(
        {
            INPUT_KEY: inputs["standalone_query"],
            "conversation_summary": inputs["conversation_summary"],
            "context": _combine_documents(docs),
        }
    )

    return {"output": output}
