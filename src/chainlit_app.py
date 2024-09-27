from solver import solve
import os
import uuid
from chainlit import (
    on_chat_start,
    on_message,
    user_session,
    Message,
    Text,
    header_auth_callback,
)

ITERATIONS = os.environ.get('BOT_ITERATIONS')

# The Chainlit callback function that will handle sending messages
async def chainlit_callback(message):
     await Message(content=message).send()

@on_chat_start
async def chat_start() -> None:
    """This method runs when a user opens a new chat session"""

    user_session.set("session_id", str(uuid.uuid4()))
    await Message("Welcome to our chat. How can I help you?").send()

# Chainlit message handler
@on_message
async def on_message(message: str):
    iterations = 3  # Number of iterations for revisions
    msg_content = message.content
    print (msg_content)
    # Initialize the MultiAgentSystem with the LLM, problem, and callback
    response = await solve(msg_content, chainlit_callback, ITERATIONS)
    await chainlit_callback(response)
    
    # # Run the defined number of iterations
    # for i in range(iterations):
    #     await agent_system.run_iteration(i + 1)

    # # Run the judge decision after iterations
    # await agent_system.run_judgment()
