# Safe upstream sync

Run on Windows in the HomeVision checkout, before starting a new feature:

```powershell
git status --short
git fetch upstream
git log --oneline HEAD..upstream/main
git diff --stat HEAD..upstream/main
```

Do not blindly merge a new DataVision revision into the release branch. Use a separate integration branch (`git switch -c upstream-review-YYYYMMDD`) and merge only after inspecting `MainActivity.kt`, build flavors, resource names, and the licensing files. Rerun `node`/Python patch checks, Gradle tests, Fire TV remote tests, and staging installation. Source conflicts should fail CI instead of being automatically resolved.

Do not re-run `apply_homevision.py` over an already patched tree; the patcher refuses to do so. Review upstream differences and port individual commits manually.
