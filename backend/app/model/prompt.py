def build_prompt(schema_text: str, question: str, max_rows: int = 100):
    return (
f"""System:
You are an expert SQL assistant for Microsoft SQL Server.
Rules: Generate ONLY one valid SQL query. SELECT-only. Do not modify data.
Avoid ;, EXEC, xp_cmdshell, INSERT/UPDATE/DELETE/MERGE, BULK, OPENROWSET. 
If unsure, say you cannot answer with the available schema.

Context:
{schema_text}

User question:
{question}

Constraints:
- Return at most TOP {max_rows} rows unless the question asks a small scalar.
- Use existing tables/columns. Avoid hallucinating names.
- Prefer ANSI joins, include schema prefixes (schema.table).

Output:
Return ONLY the SQL query (no prose, no markdown).
"""
    )
