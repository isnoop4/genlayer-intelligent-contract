# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class AIPredictionMarket(gl.Contract):
    question: str
    is_resolved: bool
    outcome: str

    def __init__(self, question: str):
        self.question = question
        self.is_resolved = False
        self.outcome = "PENDING"

    @gl.public.write
    def resolve_market(self, news_summary: str) -> str:
        if self.is_resolved:
            return f"Market already resolved as: {self.outcome}"

        q = self.question

        def evaluate_result() -> str:
            prompt = f"Based on this news summary: '{news_summary}', answer YES or NO to the question: '{q}'."
            return gl.nondet.exec_prompt(prompt)

        result = gl.eq_principle.ComparativeEq(evaluate_result)

        if "YES" in str(result).upper():
            self.outcome = "YES"
            self.is_resolved = True
            return "RESOLVED: YES"
        elif "NO" in str(result).upper():
            self.outcome = "NO"
            self.is_resolved = True
            return "RESOLVED: NO"
        else:
            return f"UNCLEAR: {result}"
