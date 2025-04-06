```mermaid
graph TD
    MainAgent[Main Agent<br/>Orchestrator] --> SubAgent1[Research Agent<br/>Information Gathering]
    MainAgent --> SubAgent2[Analysis Agent<br/>Data Processing]
    MainAgent --> SubAgent3[Execution Agent<br/>Task Implementation]

    %% Main Agent Responsibilities
    MainAgent --> |1. Request Analysis| Analyze[Analyze Request]
    MainAgent --> |2. Task Delegation| Delegate[Delegate Tasks]
    MainAgent --> |3. Result Synthesis| Synthesize[Synthesize Results]
    MainAgent --> |4. Quality Control| QC[Quality Control]

    %% SubAgent1 Responsibilities
    SubAgent1 --> |1. Information Search| Search[Search Information]
    SubAgent1 --> |2. Data Collection| Collect[Collect Data]
    SubAgent1 --> |3. Source Verification| Verify[Verify Sources]

    %% SubAgent2 Responsibilities
    SubAgent2 --> |1. Data Processing| Process[Process Data]
    SubAgent2 --> |2. Pattern Recognition| Patterns[Find Patterns]
    SubAgent2 --> |3. Analysis| Analyze2[Analyze Information]

    %% SubAgent3 Responsibilities
    SubAgent3 --> |1. Task Execution| Execute[Execute Tasks]
    SubAgent3 --> |2. Implementation| Implement[Implement Solutions]
    SubAgent3 --> |3. Code Generation| Code[Generate Code]

    style MainAgent fill:#f9f,stroke:#333,stroke-width:2px
    style SubAgent1 fill:#bbf,stroke:#333,stroke-width:2px
    style SubAgent2 fill:#bfb,stroke:#333,stroke-width:2px
    style SubAgent3 fill:#fbb,stroke:#333,stroke-width:2px
```

This diagram shows:

1. Main Agent (Orchestrator):
   - Analyzes incoming requests
   - Delegates tasks to appropriate sub-agents
   - Synthesizes results from sub-agents
   - Ensures quality control

2. Research Agent:
   - Searches for relevant information
   - Collects necessary data
   - Verifies sources and credibility

3. Analysis Agent:
   - Processes collected data
   - Identifies patterns and relationships
   - Performs in-depth analysis

4. Execution Agent:
   - Executes specific tasks
   - Implements solutions
   - Generates code when needed

The color coding helps distinguish between different agent types and their specific roles in the system. 