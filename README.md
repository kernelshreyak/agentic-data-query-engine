# Agentic Data Query Engine (ADQE)

Fast data source agnostic query engine for wide range of local and remote data sources using agents supporting agentic RAG and agentic code/tool execution for efficient querying across large databases and datasets.

The best querying mechanism is automatically determined by the agents and they do any required formatting as well.

Currently tesed with Open AI GPT-4o

Supported data sources:
- Any locally readable file format (type needs to be specified when adding the data source)
- Any locally accessible database or a remote database which does not have specific security requirements as this is a simpler implementation for now