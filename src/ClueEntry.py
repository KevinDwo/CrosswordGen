class ClueEntry:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer.upper()
        self.status = False

    def get_question(self) -> str:
        return self.question
    
    def get_answer(self) -> str:
        return self.answer
    
    def get_status(self) -> bool:
        return self.status
    
    def set_status(self, status: bool):
        self.status = status
