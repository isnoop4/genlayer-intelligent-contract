# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

class AIFreelanceEscrow(gl.Contract):
    client: Address
    freelancer: Address
    job_description: str
    amount: u256
    status: str  # "CREATED", "FUNDED", "COMPLETED", "DISPUTED", "REFUNDED"
    verdict_json: str

    def __init__(self, freelancer: str, job_description: str):
        self.client = gl.message.sender_address
        self.freelancer = Address(freelancer)
        self.job_description = job_description
        self.amount = u256(0)
        self.status = "CREATED"
        self.verdict_json = json.dumps({"verdict": "PENDING"})

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

        # Callback eksplisit memanggil LLM non-deterministik
        def call_nondet() -> str:
            prompt = (
                f"Task Description: '{task_desc}'\n"
                f"Submitted Work: '{submitted_work}'\n\n"
                f"Analyze if the submitted work satisfies the task requirements.\n"
                f"Respond ONLY with valid JSON format:\n"
                f'{{"verdict": "APPROVED" | "REJECTED", "confidence": "HIGH" | "MEDIUM" | "LOW", "reason": "brief explanation"}}'
            )
            return gl.nondet.exec_prompt(prompt)

        # Evaluasi Konsensus Validator
        raw_result = gl.eq_principle.ComparativeEq(call_nondet)
        self.verdict_json = str(raw_result)

        if "APPROVED" in self.verdict_json.upper():
            self.status = "COMPLETED"
            self.amount = u256(0)
            return self.verdict_json
        else:
            self.status = "DISPUTED"
            return self.verdict_json

    @gl.public.write
    def resolve_dispute_refund(self):
        """Client melakukan refund jika status pekerjaan ditolak/disputed."""
        assert gl.message.sender_address == self.client, "Only client can trigger refund"
        assert self.status == "DISPUTED", "No dispute to refund"

        self.amount = u256(0)
        self.status = "REFUNDED"

    @gl.public.view
    def get_verdict(self) -> str:
        return self.verdict_json
