One of the central concepts of LangGraph is state. Each graph execution creates a state that is passed between nodes in the graph as they execute, 
and each node updates this internal state with its return value after it executes. The way that the graph updates its internal state is 
defined by either the type of graph chosen or a custom function.
State in LangGraph can be pretty general, but to keep things simpler to start, we'll show off an example where the graph's state is limited to a list of chat messages 
using the built-in MessageGraph class. This is convenient when using LangGraph with LangChain chat models because we can return chat model output directly.
