# Tool Usage Notes

## exec — Safety Limits

- Commands have a 60s timeout
- Dangerous commands are blocked (rm -rf, format, dd, shutdown)
- Output truncated at 10,000 characters

## File Tools

- Use `read_file` to check existing content before writing
- Use `write_file` for full rewrites
- Use `edit_file` for targeted edits

## Model

- Provider: Groq
- Model: llama-3.1-8b-instant
- Keep prompts directive — role + exact behavior + hard stops
- No subagent spawning from this agent
