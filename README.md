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

## How It Works

1. **Initialization**: Client creates escrow defining `freelancer` address and `job_description`.
2. **Funding**: Client deposits collateral via `fund_escrow()`.
3. **Submission & Consensus**: Freelancer calls `submit_work_and_claim(submitted_work)`.
   * Contract executes non-deterministic callback: `gl.nondet.exec_prompt(...)`.
   * Consensus reached using `gl.eq_principle.ComparativeEq`.
4. **Resolution**: If verdict is `APPROVED`, status shifts to `COMPLETED` and escrow settles. If `REJECTED`, contract flags as `DISPUTED` allowing client refund via `resolve_dispute_refund()`.

---

## Project Structure

```text
├── contracts/
│   └── FreelanceEscrow.py    # GenLayer Intelligent Contract (Python)
├── frontend/
│   ├── index.html            # Web DApp UI
│   └── app.js                # GenLayer Web3 integration logic
└── README.md                 # Project documentation
