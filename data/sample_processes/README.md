# Sample IT Process Descriptions

These are example inputs for the Business Process Optimization app. Each one
describes a real-world IT workflow that is deliberately manual and inefficient,
so the LLM has clear bottlenecks to identify and optimize.

## Files

| File | Scenario | Good for showing |
| ---- | -------- | ---------------- |
| `onboarding.txt` | New-hire IT provisioning | Sequential manual steps, approval delays |
| `offboarding.txt` | Employee de-provisioning | Security gaps, access left active |
| `password_reset.txt` | Account lockout handling | Self-service automation, security fixes |
| `server_provisioning.txt` | New server requests | Infrastructure-as-code, request intake |
| `software_release.txt` | Production releases | CI/CD, change tracking, rollback |
| `ticket_triage.txt` | Helpdesk intake & routing | Auto-classification, knowledge base |
| `patch_management.txt` | OS/app patching | Inventory automation, scaling |

## How to use

**Web UI:** open a file, copy its contents, paste into the text area, and click
**Analyze + Optimize**.

**CLI:**
```powershell
& "$env:USERPROFILE\.local\bin\uv.exe" run python -m src.ui.cli --file data/sample_processes/ticket_triage.txt
```

## Tips for your presentation

- `ticket_triage.txt` and `onboarding.txt` produce the most visually obvious
  "before vs after" improvements — good for a live demo.
- Start with a shorter one (`password_reset.txt`) if you want a faster first run
  while the model warms up.
- You can also write your own: describe any process step by step and include a
  short "Pain points" note at the end to give the model context.
