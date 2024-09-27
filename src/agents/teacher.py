from langchain.memory import ConversationBufferMemory
class TeacherAgent:
    def __init__(self, llm):
        self.llm = llm
        self.memory = ConversationBufferMemory()

    async def review_solution(self, student_name: str, student_solution: str, callback)-> str:
        """Teacher reviews the student's solution using memory."""
        previous_conversation = self.memory.load_memory_variables({})["history"]
        prompt = (
            f"As a physics teacher, review the following student's solution:\n\n"
            f"{student_solution}\n\n"
            f"Previous feedback:\n\n"
            f"{previous_conversation}\n\n"
            f"Provide specific feedback on any errors or areas for improvement."
        )

        # Generate the teacher's feedback and update the memory
        feedback = self.llm(prompt)
        self.memory.save_context({"input": student_solution}, {"output": feedback})
        await callback(f"Teacher's feedback for {student_name}:\n{feedback}")
        return feedback