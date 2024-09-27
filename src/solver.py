API_KEY = '123'

import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from agents.teacher import TeacherAgent
from agents.student import StudentAgent
from agents.judge import JudgeAgent

MODEL = 'phi3-mini'
client = ChatOpenAI(
    api_key = API_KEY, 
    model = MODEL, 
    temperature=0.7)

def llm(message):
    response = client.invoke([message])
    return response.content

# Initialize OpenAI model for the agents
# MultiAgentSystem class

class MultiAgentSystem:
    def __init__(self, llm, physics_problem, callback):
        self.llm = llm
        self.physics_problem = physics_problem
        self.callback = callback  # Callback for sending messages via Chainlit

        # Initialize agents
        self.students = {
            "Student 1": StudentAgent("Student 1", llm, physics_problem),
            "Student 2": StudentAgent("Student 2", llm, physics_problem),
            "Student 3": StudentAgent("Student 3", llm, physics_problem)
        }
        self.teacher = TeacherAgent(llm)
        self.judge = JudgeAgent(llm)

    async def run_iteration(self, iteration) -> str :
        """Run one iteration of student, teacher, and judge interactions."""
        await self.callback(f"**Iteration {iteration} begins**")

        # Step 1: Students provide their initial or revised solutions
        for student_name, student_agent in self.students.items():
            await student_agent.solve_problem(self.callback)

        # Step 2: Teacher reviews and provides feedback
        for student_name, student_agent in self.students.items():
            feedback = await self.teacher.review_solution(
                student_name, student_agent.solution, self.callback
            )
            student_agent.memory.save_context({"input": student_agent.solution}, {"output": feedback})

    async def run_judgment(self) -> str :
        """Judge picks the best solution after iterations."""
        student_solutions = {student: agent.solution for student, agent in self.students.items()}
        await self.judge.evaluate_solutions(student_solutions, self.callback)
    
async def solve(physics_problem, chainlit_callback, iterations)-> str:
    # Initialize the MultiAgentSystem with the LLM, problem, and callback
    agent_system = MultiAgentSystem(llm, physics_problem, chainlit_callback)

    # Run the defined number of iterations
    for i in range(iterations):
        await agent_system.run_iteration(i + 1)

    # Run the judge decision after iterations
    return await agent_system.run_judgment()

# Problem for the students to solve
#physics_problem = "Describe Newton's laws of motion and calculate the force on an object with mass 10 kg accelerated by 2 m/s²."

