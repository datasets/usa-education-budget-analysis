## Update Script Maintenance Report

Date: 2026-03-04

- Root cause: brittle DOM selector for ZIP discovery broke as White House page markup changed.
- Fixes made: replaced fixed CSS selector with resilient link scanning for historical budget ZIP, added timeout/status checks, and modernized workflow permissions/triggers.
- Validation: verified script path no longer assumes a single hardcoded page node and fails with a clear error when ZIP link is absent.
- Known blockers: upstream page/link naming changes may still require periodic selector tuning.
