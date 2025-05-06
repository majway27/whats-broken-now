# Tests

- Run tests from the whats-broken-now directory.
  - `run_tests.sh`

## Tickets

- Using Python's unittest discovery (recommended)
  - `PYTHONPATH=. python -m unittest discover tests/tickets -v`
- Running specific test files
  - `PYTHONPATH=. python -m unittest tests/tickets/test_tickets.py -v`