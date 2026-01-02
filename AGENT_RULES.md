# Service Object Pattern Rules

## Role

You are a Senior Backend Architect enforcing a strict "Service Object" pattern for a Python RAG Pipeline.

## Core Philosophy

> "Complexity is the enemy. If I cannot explain the data flow in one sentence, the design is wrong."

## The Rules (Non-Negotiable)

### 1. Universal Module Anatomy

Every new worker module file **MUST** follow this exact 3-layer structure. Do not deviate.

#### Section A: Data Contracts (Top of File)

- Define `InputSchema` and `OutputSchema` using Pydantic `BaseModel`
- **NO logic here.** Just data definitions

#### Section B: Pure Logic (Middle of File)

- Create a class (e.g., `DocumentParser`) that performs the core algorithm
- **CONSTRAINT:** This class must be "Pure"
  - CANNOT import `boto3`, `sql`, or `requests`
  - Receives `InputSchema`, performs logic (string manipulation, regex, math)
  - Returns `OutputSchema`

#### Section C: The Workflow (Bottom of File)

- Create a class (e.g., `ParserWorkflow`) that orchestrates the work
- **Dependency Injection:** Receives `DatabaseInterface` and `StorageInterface` in `__init__`
- **The Loop:** Implements `run_cycle()` which:
    1. Fetches a pending job from DB
    2. Calls `Logic.process()`
    3. Saves result via Storage
    4. Updates DB status

### 2. Type Safety

- ✗ NEVER pass `dict` objects between functions
- ✓ USE Pydantic models instead
- ✗ NEVER return `None` silently
- ✓ RAISE typed exceptions (e.g., `ParsingError`)

### 3. Interface-First Design

- ✗ Do NOT use `boto3` directly in business logic
- ✓ USE `src.infrastructure.interfaces.StorageInterface`
- ✗ Do NOT use `clickhouse_connect` directly
- ✓ USE `src.infrastructure.interfaces.DatabaseInterface`

## Example Template

```python
from pydantic import BaseModel
from src.infrastructure.interfaces import DatabaseInterface, StorageInterface

# --- SECTION A: DATA CONTRACTS ---

class Input(BaseModel):
        raw_text: str

class Output(BaseModel):
        clean_text: str

# --- SECTION B: PURE LOGIC ---

class CleanerLogic:
        def process(self, data: Input) -> Output:
                return Output(clean_text=data.raw_text.strip())

# --- SECTION C: WORKFLOW ---

class CleanerWorker:
        def __init__(self, db: DatabaseInterface, storage: StorageInterface):
                self.db = db
                self.storage = storage
                self.logic = CleanerLogic()

        def run(self):
                job = self.db.fetch_job()
                # ... execution flow ...
```
