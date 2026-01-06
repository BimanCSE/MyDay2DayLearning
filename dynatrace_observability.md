## Dynatrace AI and LLM Observability:
Dynatrace supports GenAI observability by troubleshooting conversation issue, performance, costs and correlating data throughout the product for effectively resolving the issue in LLM or traditional Machine Learning. Dynatrace supports following LLM paradigm 
- Retrieve Augmented Generation (RAG)
- Agents
- Agentic Application

#### Instrument : 
Instrument is the process of adding observability code to an application. Dynatrace **OpenLLMMetry** as instrument library . **OpenLLMMetry** automatically registers an OpenTelemetry SDK and list of instrument for popular GenAI frameworks, models and vector database. 

#### Trace : 
A trace describes a user request and all the operations performed to satisfy it. We can analyze the steps relevant to observing AI/ML workloads.

Traces help bring visibility into complex workflows, providing information about costs, performance, and insights into the quality of the generated output in the context of AI/ML workloads.

It's common to have LLM applications with complex and autonomous logic in which a model makes the decision. We can leverage traces to understand how requests propagate across RAG or agentic pipelines and see the details of each step that was executed.

Each action performed in a trace is stored as a span. The span attributes contain information relevant to AI/ML workloads (such as token costs for the operation, and input and output prompts). OpenLLMetry follows the OpenTelemetry Semantic Conventions for GenAI﻿, so it's easy to find the relevant attribute keys.

#### Traceloop span kind: 
Traceloop marks spans that belong to an LLM framework with a particular attribute, traceloop.span.kind. This attribute helps to organize and understand the structure of your application's traces, making it easier to analyze and debug complex LLM-based systems.

The traceloop.span.kind attribute can have one of four possible values:

- workflows: Represents a high-level process or chain of operations.
- task: Denotes a specific operation or step within a workflow.
- agent: Indicates an autonomous component that can make decisions or perform actions.
- tool: Represents a utility or function used within the application.
![OpenTeleMetry](https://dt-cdn.net/images/arch-886-aece62e05b.png?_gl=1*mkoxqn*_ga*NzAyNzAyMzgyLjE3NTE1MjM5NzU.*_ga_1MEMV02JXV*czE3Njc2NzI5OTkkbzQkZzEkdDE3Njc2NzQxNDMkajU2JGwwJGgw)
### OpenLLMetry:

OpenLLMetry supports AI model observability by capturing and normalizing key performance indicators (KPIs) from diverse AI frameworks. Utilizing an additional OpenTelemetry SDK layer, this data seamlessly flows into the Dynatrace environment, offering advanced analytics and a holistic view of the AI deployment stack.

Given the prevalence of Python in AI model development, OpenTelemetry serves as a robust standard for collecting observability data, including traces, metrics, and logs. While OpenTelemetry's auto-instrumentation provides valuable insights into spans and basic resource attributes, it falls short in capturing specific KPIs crucial for AI models, such as model name, version, prompt and completion tokens, and temperature parameter.

OpenLLMetry bridges this gap by supporting popular AI frameworks like OpenAI, HuggingFace, Pinecone, and LangChain. By standardizing the collection of essential model KPIs through OpenTelemetry, it ensures comprehensive observability. The open-source OpenLLMetry SDK, built on top of OpenTelemetry, enables thorough insights into your LLM application.

Because the collected data seamlessly integrates with the Dynatrace environment, users can analyze LLM metrics, spans, and logs in the context of all traces and code-level information. Maintained under the Apache 2.0 license by Traceloop, OpenLLMetry becomes a valuable asset for product owners, providing a transparent view of AI model performance.

Explore the high-level architecture illustrating how OpenLLMetry captures and transmits AI model KPIs to the Dynatrace environment, empowering businesses with unparalleled insights into their AI deployment landscape.
