
## Makefile
-create-environment
  -create venv
  -activate venv
  -export pythonpath

-requirements: create-environment
  -pip install requirements
  
-run-checks
  -pep8
  -pip-audit
  -bandit
  -black

-run-tests

-run-all