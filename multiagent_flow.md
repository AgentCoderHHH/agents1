```mermaid
sequenceDiagram
    participant User
    participant MainAgent
    participant SubAgent1
    participant SubAgent2
    participant SubAgent3

    User->>MainAgent: Makes a request
    MainAgent->>MainAgent: Analyzes request complexity
    alt Complex Request
        MainAgent->>SubAgent1: Delegate subtask 1
        MainAgent->>SubAgent2: Delegate subtask 2
        MainAgent->>SubAgent3: Delegate subtask 3
        
        SubAgent1-->>MainAgent: Returns result 1
        SubAgent2-->>MainAgent: Returns result 2
        SubAgent3-->>MainAgent: Returns result 3
        
        MainAgent->>MainAgent: Synthesizes results
    else Simple Request
        MainAgent->>MainAgent: Process directly
    end
    
    MainAgent-->>User: Returns final response
```

This diagram shows:
1. User initiates a request
2. MainAgent evaluates if the request needs multiple agents
3. If complex:
   - MainAgent splits tasks among specialized SubAgents
   - Each SubAgent processes its assigned task
   - MainAgent combines the results
4. If simple:
   - MainAgent handles the request directly
5. Final response is returned to the user 