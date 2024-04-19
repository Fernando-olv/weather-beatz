env:
	@powershell -NoExit -Command "& {.\\Scripts\Activate.ps1}"

run:
	flask --app server.py --debug run

lint:
	pre-commit run --all-files