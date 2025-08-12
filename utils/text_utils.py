def summarize_rows_to_text(column_names, rows, max_rows=10) -> str:
    """
    Convert rows and column names into a readable text summary.
    """
    if not rows:
        return "No rows returned."
    lines = []
    limit = min(len(rows), max_rows)
    for i in range(limit):
        r = rows[i]
        pairs = [f"{col}: {val}" for col, val in zip(column_names, r)]
        lines.append(" | ".join(pairs))
    if len(rows) > max_rows:
        lines.append(f"... (+{len(rows)-max_rows} more rows)")
    return "\n".join(lines)
