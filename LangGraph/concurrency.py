from langchain_core.messages import HumanMessage
# node
def call_model():
  # do cool stuff
  # thread_id = <here I'm lost ... configurable["thread_id"]>
  print(thread_id)

# Define graph
workflow = MessageGraph()
...

# Define nodes and edges ...
workflow.add_node("agent", call_model)
...
app = workflow.compile(...)


# now call it
thread = {"configurable": {"thread_id": "2"}}
inputs = [HumanMessage(content="hi! I'm bob")]
for event in app.stream(inputs, thread):
    for v in event.values():
        print(v)
