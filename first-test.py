# Configure the LLM API in the .env file in the same-level folder. You can refer to the .env.example in the code folder, or reuse the .env file from previous chapter cases.
from tools.calculator_tool import CalculatorTool
from dotenv import load_dotenv
from my_llm import MyLLM
from simple_agent import SimpleAgent

# Load environment variables
load_dotenv()

# Create LLM instance - framework automatically detects provider
llm = MyLLM()

# Or manually specify provider (optional)
# llm = MyLLM()

# Create SimpleAgent
agent = SimpleAgent(
    name="AI Assistant",
    llm=llm,
    system_prompt="You are a helpful AI assistant"
)

# Basic conversation
user_prompt = "Hello! Please introduce yourself."
print (f"User: {user_prompt}")
response = agent.run(user_prompt)
print(f"AI: {response}")

# Create a local arithmetic tool. Tool-calling integration can be added later.
calculator = CalculatorTool()

# Now you can use tools
user_prompt = "Please help me calculate 2 + 3 * 4"
print(f"User: {user_prompt}")
response = agent.run(user_prompt)
print(f"AI: {response}")

# View conversation history
print(f"Number of historical messages: {len(agent.get_history())}")
