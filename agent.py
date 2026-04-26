# 导入依赖
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

# https://smith.langchain.com/

# load env variables
load_dotenv()

# 数据库配置
DB_PATH = "chinook.db"

# 自动创建测试数据库
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}", sample_rows_in_table_info=3)

# Initialize large model - Using Cloud model
# model = ChatOpenAI(
#     model="openrouter/free",
#     temperature=0,
#     openai_api_base=os.getenv("OPENAI_API_BASE"),
# )

# Initialize large model - Using Ollama model
model = ChatOllama(
    # model="qwen3.5:9b",
    model="gemma4:e4b",
    validate_model=False,
    streaming=False,
    temperature=0,
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),  # Default Ollama URL
)

base_dir = "./"


def create_sql_deep_agent():
    """
    create SQL Deep Agent
    Returns:instance of DeepAgent
    """
    # create SQL toolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=model)
    sql_tools = toolkit.get_tools()
    
    # display available tools
    print("\n Available tools:")
    for i, tool in enumerate(sql_tools, 1):
        print(f"  {i}. {tool.name} - {tool.description[:50]}...")
    
    # create Deep Agent
    agent = create_deep_agent(
        model=model,
        memory=["./AGENTS.md"],
        skills=[
            "./skills/query-writing",
            "./skills/schema-exploration"
        ],
        tools=sql_tools,
        subagents=[],
        backend=FilesystemBackend(root_dir=base_dir, virtual_mode=False)
    )
    return agent


def execute_query(agent, query: str) -> str:
    """
    execute natural language query
    
    Args:
        agent: agent instance
        query: user natural language query
        
    Returns:
        result of query
    """
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })
    # process AIMessage instance
    if hasattr(result["messages"][-1], 'content'):
        return result["messages"][-1].content
    else:
        return result["messages"][-1]["content"]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Text-to-SQL Agent")
    parser.add_argument("--draw-graph", action="store_true", help="generate LangGraph")
    parser.add_argument("--output", type=str, default="agent_graph.png", help="png name for graph")
    args = parser.parse_args()
    
    print("Text-to-SQL Agent starting...")
    
    try:
        agent = create_sql_deep_agent()
        
        if args.draw_graph:
            print(f"\ngenerating LangGraph ...")
            try:
                # 尝试使用 mermaid 绘制
                graph_image = agent.get_graph().draw_mermaid_png()
                with open(args.output, "wb") as f:
                    f.write(graph_image)
                print(f"save to：{args.output}") # https://mermaid.live/
            except Exception as e:
                print(f"PNG generate failed，try ouput Mermaid text ...")
                mermaid_code = agent.get_graph().draw_mermaid()
                print("\nMermaid code:")
                print(mermaid_code)
                print("\npaste the code to https://mermaid.live/ and view")
            exit(0)
        
        print("\nSQL Deep Agent started successfully！")
        
        # 显示数据库信息
        print(f"\nSQL path: {DB_PATH}")
        print(f"NO. of available tables：{len(db.get_usable_table_names())}")
        print(f"List of tables：{', '.join(db.get_usable_table_names())}")
        
        # 测试查询示例
        test_queries = [
            # "加拿大有多少客户？",
            # "数据最多的是哪个表？",
            "哪张表的数据最多？",
            # "哪张表的数据最少？"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n 测试 {i}: {query}")
            result = execute_query(agent, query)
            print(f"\n 结果:\n{result}")
            print("-" * 60)
        
    except Exception as e:
        print(f"\n 启动失败：{str(e)}")
        print("\n 请检查:")
        print("  1. 是否安装了必要的依赖包")
        print("  2. OpenAI API 密钥是否正确配置")
        print("  3. 数据库文件是否存在")
        print("\n 如需生成 LangGraph 可视化图: python3 agent.py --draw-graph [--output graph.png]")
        
    finally:
        # 显式清理
        if agent and hasattr(agent, 'cleanup'):
            agent.cleanup()
        # 关闭数据库连接
        if 'db' in globals() and hasattr(db, 'engine'):
            db.engine.dispose()
        # 强制垃圾回收
        import gc
        collected = gc.collect()