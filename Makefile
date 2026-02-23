.PHONY: lint lint-sh

lint: lint-sh

lint-sh:
	@tools/shell_lint_quick.sh tools
