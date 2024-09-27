from langchain.memory import ConversationBufferMemory
class JudgeAgent:
    def __init__(self, llm):
        self.llm = llm
        self.memory = ConversationBufferMemory()

    async def evaluate_solutions(self, student_solutions: dict, callback)-> str:
        """Judge chooses the best solution using memory."""
        previous_conversation = self.memory.load_memory_variables({})["history"]
        solution_text = "\n".join([f"{student}: {solution}" for student, solution in student_solutions.items()])
        prompt = (
            f"As a physics expert, evaluate the following solutions to a physics problem:\n\n"
            f"{solution_text}\n\n"
            f"Previous evaluations:\n\n"
            f"{previous_conversation}\n\n"
            f"Select the best solution and explain why it is the best. Refine it and use LATEX markup for mathematical formulas."
        )

        # Generate the judge's decision and update the memory
        decision = self.llm(prompt)
        self.memory.save_context({"input": solution_text}, {"output": decision})
        await callback(f"Judge's chosen solution:\n{decision}")
        return decision