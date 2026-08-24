# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class AIFreelanceEscrow(gl.Contract):
    client: Address
    freelancer: Address
    job_description: str
    amount: u256
    status: str  # "CREATED", "FUNDED", "COMPLETED", "DISPUTED", "REFUNDED"

    def __init__(self, freelancer: str, job_description: str):
        self.client = gl.message.sender_address
        self.freelancer = Address(freelancer)
        self.job_description = job_description
        self.amount = u256(0)
        self.status = "CREATED"

    @gl.public.write.payable
    def fund_escrow(self):
        """Client mendepositkan dana ke dalam escrow."""
        assert gl.message.sender_address == self.client, "Only client can fund"
        assert self.status == "CREATED", "Escrow already funded or finalized"
        assert gl.message.value > u256(0), "Must deposit funds"

        self.amount = gl.message.value
        self.status = "FUNDED"

    @gl.public.write
    def submit_work_and_claim(self, submitted_work: str) -> str:
        """Freelancer mengirim hasil kerja dan memicu konsensus AI."""
        assert gl.message.sender_address == self.freelancer, "Only freelancer can submit"
        assert self.status == "FUNDED", "Escrow is not funded"

        task_desc = self.job_description

        # AI Consensus Call (Callable lambda + principle)
        result = gl.eq_principle.prompt_comparative(
            lambda: f"Task Description: {task_desc}\nSubmitted Work: {submitted_work}\nAnalyze if the submitted work satisfies the task requirements. Respond ONLY with 'APPROVED' or 'REJECTED'.",
            "The output must evaluate if the submission matches the task description."
        )

        if "APPROVED" in str(result).upper():
            self.status = "COMPLETED"
            # Update settlement state
            self.amount = u256(0)
            return "APPROVED: Work accepted and escrow settled."
        else:
            self.status = "DISPUTED"
            return "REJECTED: Work did not meet requirements."

    @gl.public.write
    def resolve_dispute_refund(self):
        """Client melakukan refund jika status pekerjaan ditolak/disputed."""
        assert gl.message.sender_address == self.client, "Only client can trigger refund"
        assert self.status == "DISPUTED", "No dispute to refund"

        self.amount = u256(0)
        self.status = "REFUNDED"
