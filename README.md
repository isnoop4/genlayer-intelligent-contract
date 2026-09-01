# AI-Driven Decentralized Freelance Escrow

An Intelligent Contract-powered freelance escrow system built on GenLayer. It uses non-deterministic LLM consensus (`gl.nondet.exec_prompt` with `ComparativeEq`) to automatically evaluate submitted work against task requirements and reach structured JSON consensus before releasing funds.

---

## Contract Details

* **Network**: GenLayer Studionet / Testnet Bradbury
* **Contract Address** : `0x72B04b56465548638d06d7A903a101E0895275BE
* **Explorer**: [View on GenLayer Explorer](https://explorer-studio.genlayer.com/address/0x72B04b56465548638d06d7A903a101E0895275BE)

---

## Key Features

* **Smart Escrow Locking**: Clients deposit funds into the contract specifying task requirements.
* **AI Output Validation**: GenLayer validators execute LLM prompts in parallel to evaluate submitted proof-of-work.
* **Structured Consensus**: Evaluates work returning structured JSON (`APPROVED` vs `REJECTED`, confidence level, and rationale).
* **Automated Settlement & Dispute**: Auto-settles payments upon approval or flags disputed contracts for refund.

---

##How It Works
Deploy — Client deploys the contract with the freelancer's
address and a plain-language job description.
Fund — Client calls fund_escrow and deposits GEN into the
escrow (CREATED → FUNDED).
Submit — Freelancer calls submit_work_and_claim with their
submitted work. This triggers the leader/validator consensus
flow: an LLM evaluates the work against the task description and
returns a structured verdict (APPROVED / REJECTED), which
validators independently re-check before it's accepted.
Settle
If APPROVED → status becomes COMPLETED, and payment is
transferred to the freelancer automatically.
If REJECTED → status becomes DISPUTED, and the client can
call resolve_dispute_refund to reclaim the deposited funds
(DISPUTED → REFUNDED).
Cancel — If the client wants to back out before funding, they
can call cancel_escrow (CREATED → CANCELLED).

---

## Project Structure

```text
├── contracts/
│   └── FreelanceEscrow.py    # GenLayer Intelligent Contract (Python)
├── frontend/
│   ├── index.html            # Web DApp UI
│   └── app.js                # GenLayer Web3 integration logic
└── README.md                 # Project documentation
