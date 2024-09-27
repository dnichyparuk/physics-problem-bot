from solver import solve
import asyncio

async def message_back(message:str):    
    return print (message)

test_message="how can I find speed of a falling object with mass = 10g"
response = asyncio.run(solve(test_message, message_back,2)) #llm
print(response)