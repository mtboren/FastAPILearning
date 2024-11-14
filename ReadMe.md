# FastAPI Learning
Some things relating to FastAPI.

## Quick Start
```powershell
Set-Location <root of cloned repo>
## create a virtualenv
virtualenv .venv
## activate the virtualenv
.venv/Scripts/Activate.ps1
## install the requirements
pip install -r requirements.txt
## run the server in dev mode
fastapi dev app/main.py
```

## Debug
Use the `launch.json` file in the `.vscode` folder to debug the FastAPI app. That is, use the `Python: FastAPI` configuration, start the Debugger in VSCode.

## Test
To test things (requires that `pytest` is installed, of course):
```powershell
pytest tests/
```

[!NOTE]
Most of the tests currently defined are failing -- they are just there to show how to write tests, and are from the FastAPI tutorial (not necessarily written for the current state of the app).

[!NOTE]
The `pytest.ini` file here specifies a config that allows `pytest` to run tests in the `tests/` folder -- tests external to the `app/` folder itself 👍