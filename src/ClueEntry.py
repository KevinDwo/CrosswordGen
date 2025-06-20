class ClueEntry:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer.upper()

    def getQuestion(self):
        return self.question
    
    def getAnswer(self):
        return self.answer