# tester

Fixture repository for the `issue-follower` pipeline.

Issues labelled `agent-ok` are picked up by the local poller, implemented by a
sandboxed Codex session, verified against the test suite, and published as a
draft pull request.

```bash
uv run pytest -q
```
