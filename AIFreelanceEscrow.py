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

    @gl.public.write
    def fund_escrow(self):
        """Client mendepositkan dana ke dalam escrow."""
        assert gl.message.sender_address == self.client, "Only client can fund"
        assert self.status == "CREATED", "Escrow already funded or finalized"
        assert gl.message.value > u256(0), "Must deposit funds"

        self.amount = gl.message.value
        self.status = "FUNDED"

    @gl.public.view
    def _evaluate_work_nondet(self, submitted_work: str) -> bool:
        """Helper non-deterministic call untuk evaluasi AI."""
        prompt = (
            f"Task Description: {self.job_description}\n"
            f"Submitted Work: {submitted_work}\n"
            "Analyze if the submitted work fully satisfies the task requirements. "
            "Respond ONLY with 'APPROVED' or 'REJECTED'."
        )
        response = gl.nondet.exec_prompt(prompt)
        return "APPROVED" in response.upper()

    @gl.public.write
    def submit_work_and_claim(self, submitted_work: str) -> str:
        """Freelancer mengirim hasil kerja dan memicu verifikasi konsensus AI."""
        assert gl.message.sender_address == self.freelancer, "Only freelancer can submit"
        assert self.status == "FUNDED", "Escrow is not funded"

        # Pemanggilan Equivalence Principle yang valid untuk GenVM
        is_acceptable = gl.eq_principle.eq_or_reject(
            lambda: self._evaluate_work_nondet(submitted_work)
        )

        if is_acceptable:
            self.status = "COMPLETED"
            payout_amount = self.amount
            self.amount = u256(0)
            
            # Transfer dana escrow ke freelancer
            gl.transfer(self.freelancer, payout_amount)
            return "APPROVED: Work accepted and payment transferred."
        else:
            self.status = "DISPUTED"
            return "REJECTED: Work did not meet requirements."

    @gl.public.write
    def resolve_dispute_refund(self):
        """Client dapat melakukan refund jika status pekerjaan ditolak/disputed."""
        assert gl.message.sender_address == self.client, "Only client can trigger refund"
        assert self.status == "DISPUTED", "No dispute to refund"

        refund_amount = self.amount
        self.amount = u256(0)
        self.status = "REFUNDED"

        # Kembalikan dana ke client
        gl.transfer(self.client, refund_amount)

