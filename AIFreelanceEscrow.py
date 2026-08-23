# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class AIFreelanceEscrow(gl.Contract):
    client: Address
    freelancer: Address
    job_description: str
    is_completed: bool

    def __init__(self, freelancer: Address, job_description: str):
        self.client = gl.message.sender_address
        self.freelancer = freelancer
        self.job_description = job_description
        self.is_completed = False

    @gl.public.write
    def submit_work_and_claim(self, submitted_work: str) -> str:
        if gl.message.sender_address != self.freelancer:
            return "Error: Only freelancer can submit"
        if self.is_completed:
            return "Error: Contract already completed"

        prompt = f"Task requirement: {self.job_description}. Submitted work: {submitted_work}. Does it fulfill the task? Answer APPROVED or REJECTED."
        
        # Eksekusi prompt langsung di scope fungsi write
        evaluation = gl.nondet.exec_prompt(prompt)

        if "APPROVED" in str(evaluation).upper():
            self.is_completed = True
            return "APPROVED: Work accepted."
        else:
            return f"REJECTED: {evaluation}"

