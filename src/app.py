import chainlit as cl
from solver import solve

# The Chainlit callback function that will handle sending messages
async def chainlit_callback(message):
    await cl.Message(content=message).send()


# Chainlit message handler
@cl.on_message
async def on_message(message: str):
    iterations = 3  # Number of iterations for revisions
    msg_content = message.content
    print (msg_content)
    # Initialize the MultiAgentSystem with the LLM, problem, and callback
    response = await solve(msg_content, chainlit_callback,2)
    await chainlit_callback(response)
    
    # # Run the defined number of iterations
    # for i in range(iterations):
    #     await agent_system.run_iteration(i + 1)

    # # Run the judge decision after iterations
    # await agent_system.run_judgment()
