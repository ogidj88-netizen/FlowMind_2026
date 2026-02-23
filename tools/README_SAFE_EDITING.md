# FlowMind Safe Editing Rules (tools)

## Problem we saw
Terminal copy/paste can silently corrupt files (random fragments like "&2>&2", "with shebang", etc).
This is fatal for JSON contracts/manifest writers.

## Rule
After any edit under tools/*.sh run:

make lint

If lint fails:
- open the file and delete corrupted lines
- re-run make lint

## Safe file creation pattern
Prefer creating files via heredoc blocks:

cat > path/to/file << 'EOF'
...content...
EOF
