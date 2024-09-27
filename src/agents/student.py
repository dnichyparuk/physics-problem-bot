from langchain.memory import ConversationBufferMemory
class StudentAgent:
    def __init__(self, name: str, llm, problem: str):
        self.name = name
        self.llm = llm
        self.problem = problem
        self.memory = ConversationBufferMemory()
        self.solution = ""

    async def solve_problem(self, callback)-> str:
        """Student solves or revises the physics problem using memory."""
        previous_conversation = self.memory.load_memory_variables({})["history"]
        if previous_conversation:
            prompt = (
                f"{self.name}, based on your previous solution and feedback:\n\n"
                f"{previous_conversation}\n\n"
                f"Please revise or improve your solution to the physics problem: {self.problem}.\n\n"
                f"Use LATEX markup for mathematical formulas."
            )
        else:
            prompt = f"{self.name}, please solve the following physics problem: {self.problem}"

        # Generate the student's response and update the memory
        response = self.llm(prompt)
        self.memory.save_context({"input": prompt},{"output":response})
        self.solution = response
        await callback(f"{self.name}'s Solution:\n{response}")