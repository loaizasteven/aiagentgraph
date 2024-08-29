if __name__ == "__main__":
    import os.path as osp
    import json 

    from langchain.agents import AgentExecutor, create_react_agent
    from langchain_openai import OpenAI
    from langchain_core.prompts import PromptTemplate

    from tools.agenttools import average_dog_weight, calculate
    file_dir = osp.dirname(__file__)

    # Load and Config
    prompt_dict = json.load(open(osp.join(file_dir, 'config/prompts.json'), 'r'))
    prompt = PromptTemplate.from_template(prompt_dict.get('system_prompt_template'))
    tools = [average_dog_weight, calculate]

    # Create Agent
    client = OpenAI()
    agent = create_react_agent(client, tools, prompt)

    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    agent_executor.invoke(
        {"input": "How much does a toy poodle weigh?"
         })
    agent_executor.invoke(
        {"input": "I have 2 dogs, a border collie and a scottish terrier. What is their combined weight"
         })