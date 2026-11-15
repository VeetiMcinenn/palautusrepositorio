# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Dependencies are managed with `uv`; run everything through `uv run`.

**Start the app** (from `src/`, on port 5000, which is what the tests expect):

```
cd src && uv run flask --app app run --port 5000 --debug
```

Note: `src/index.py` starts the app on port **5001**, but `src/AppLibrary.py` and
`src/tests/resource.robot` are hardcoded to port **5000**. Running `python src/index.py`
therefore does not work with the test suite as-is. Use the `flask run` command above,
or check that nothing stale is already listening on 5000 (`netstat -ano | findstr :5000`).
Tests silently run against whatever is on that port.

**Run the Robot Framework tests** (the app must be running first):

```
uv run robot --variable HEADLESS:true src/tests          # whole suite, headless
uv run robot src/tests                                    # visible browser, 500ms slowMo
uv run robot --variable HEADLESS:true src/tests/register.robot   # one suite
uv run robot --variable HEADLESS:true -t "Register With Too Short*" src/tests  # one test
```

Robot writes `output.xml`, `log.html` and `report.html` into the cwd; pass
`--outputdir <dir>` to keep them out of the repo.

A pre-commit hook runs pylint on committed Python files.

## Architecture

Flask app with a three-layer structure under `src/`, all state in memory:

- `app.py` — routes. Each POST handler calls a service method, catches `Exception`,
  `flash`es the message and redirects back to the form. Templates render flashed
  messages, which is what the tests assert on. Success redirects to `/welcome`
  (register) or `/ohtu` (login).
- `services/user_service.py` — `UserService.validate()` is the single place where
  registration rules live (username length, uniqueness, password length, content,
  confirmation). It raises `UserInputError` with the exact string the Robot tests
  look for, so error messages are effectively part of the test contract.
- `repositories/user_repository.py` — in-memory list of `User` entities; module-level
  singleton `user_repository`. `delete_all()` backs the `/tests/reset` endpoint.

**Test setup:** Robot tests in `src/tests/` are end-to-end through a real browser
(`robotframework-browser`). `resource.robot` holds shared keywords and URLs.
`AppLibrary.py` is a Python keyword library that talks to the running app over HTTP:
`Reset Application` hits `/tests/reset`, `Create User` POSTs to `/register`. Every
test that needs a known user calls both in its `Test Setup`, so tests are independent
and order does not matter. The suite does not start the app itself.

Adding a registration rule means: add a test to `register.robot` asserting on the
message, then add the check and message to `validate()`.
