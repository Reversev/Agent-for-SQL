# Agent-for-SQL
SQL Intelligent Agent, Supporting Local Deployment and Cloud Deployment

## Basic
```shell
# Clone the repository
git clone https://github.com/Reversev/Agent-for-SQL.git
cd Agent-for-SQL

pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

## Modify .env file:
```
# OpenAI API Configuration
OPENAI_API_KEY=your_api_key_here

# Optional: Custom API Base URL (if using proxy or local deployment)
# OPENAI_API_BASE=https://api.your-proxy.com/v1
OPENAI_API_BASE="https://openrouter.ai/api/v1/chat/completions"

# LangSmith Configuration
LANGCHAIN_TRACING_V2=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=lsv2_pt_xxx
LANGCHAIN_PROJECT=your_project_name
```

## Run Agent
You can modified the contents on ```test_queries``` variable in line 130 of ```agent.py```, and run agent.
```shell
python agent.py
```

##  view langchain process
Monitor platform: view [https://smith.langchain.com/](https://smith.langchain.com/)

## LangGraph
Run the code:
```shell
python3 agent.py --draw-graph --output graph.png
```

![](https://github.com/Reversev/Agent-for-SQL/blob/main/agent_graph.png)



