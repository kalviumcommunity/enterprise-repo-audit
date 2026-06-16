# Instructor Setup Guide: Creating the Enterprise Repository Audit Lab

This guide provides step-by-step instructions for instructors to recreate the enterprise-repo-audit repository with all hidden issues embedded in Git history.

---

## Overview

The goal is to create a repository that:
- Looks professional and complete at first glance
- Contains multiple hidden governance and operational failures
- Requires students to use Git forensics to discover issues
- Takes 45-60 minutes for students to fully audit

This guide uses Git commands to embed problems into history that students will discover through investigation.

---

## Part 1: Initial Repository Setup

### Step 1: Create and Initialize Repository

```bash
# Create the repository directory
mkdir enterprise-repo-audit
cd enterprise-repo-audit

# Initialize git
git init

# Create initial README
echo "# enterprise-repo-audit" > README.md

# Initial commit
git add README.md
git commit -m "Initial commit"
```

### Step 2: Create Directory Structure

```bash
# Create all necessary directories
mkdir -p src config scripts docs .github/workflows

# Create initial placeholder files
touch src/__init__.py
touch config/.gitkeep
touch scripts/.gitkeep

git add .
git commit -m "Add project structure"
```

---

## Part 2: Build Complete File Structure

After setting up the directory structure, add all the files created earlier:
- src/app.py, auth.py, utils.py
- config/settings.env.example
- scripts/backup.sh, migrate.sh, cleanup.sh
- deploy.sh
- docs/architecture.md, release-process.md
- .github/workflows/ci.yml
- SECURITY.md, CONTRIBUTING.md, .gitignore
- requirements.txt
- INVESTIGATION-REPORT.md

```bash
# Commit all application files
git add src/ config/ scripts/ docs/
git commit -m "Add application source code"

git add .github/
git commit -m "Add CI pipeline configuration"

git add .gitignore requirements.txt
git commit -m "Add project configuration"

git add SECURITY.md CONTRIBUTING.md
git commit -m "Add governance documentation"
```

---

## Part 3: Embed Hidden Issue #1 - Secret in Git History

**Problem:** Exposed API key in config file, later removed but still in history.

### Implementation

```bash
# Modify settings.env.example to include a secret
cat > config/settings.env.example << 'EOF'
SERVICE_HOST=127.0.0.1
SERVICE_PORT=5000
ENVIRONMENT=production
DEBUG=false

# CRITICAL: AWS credentials exposed in history
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
STRIPE_API_KEY=sk_prod_51234567890abcdefghijklmnop

# Database
DB_HOST=prod-db.example.com
DB_USER=admin
DB_PASSWORD=Production123!SecurePass
EOF

# Commit with secret
git add config/settings.env.example
git commit -m "Update production environment configuration"

# Later, "fix" the issue by removing secrets but they remain in history
cat > config/settings.env.example << 'EOF'
SERVICE_HOST=127.0.0.1
SERVICE_PORT=5000
ENVIRONMENT=production
DEBUG=false
DB_HOST=localhost
DB_PORT=5432
EOF

# Add .env to .gitignore (should have been done earlier)
echo ".env" >> .gitignore
echo "config/settings.env" >> .gitignore

git add config/settings.env.example .gitignore
git commit -m "Remove sensitive data from repository"

# This leaves the secret accessible via:
# git log -S "AWS_SECRET_ACCESS_KEY"
# git log -p --all -- config/settings.env.example
```

---

## Part 4: Embed Hidden Issue #2 - Inconsistent Commit Messages

**Problem:** Poor commit message standards mixed with good ones.

### Implementation

```bash
# Add commits with poor messages
# Create a temporary test file
echo "test data" > /tmp/feature1.txt
cp /tmp/feature1.txt src/feature1.py
git add src/feature1.py
git commit -m "fix"

# Another poor message
echo "more data" > /tmp/feature2.txt
cp /tmp/feature2.txt src/feature2.py
git add src/feature2.py
git commit -m "asdf"

# Another one
echo "test" > /tmp/feature3.txt
cp /tmp/feature3.txt src/feature3.py
git add src/feature3.py
git commit -m "temp"

# Poor message with typos
echo "data" > /tmp/feature4.txt
cp /tmp/feature4.txt src/feature4.py
git add src/feature4.py
git commit -m "final"

# Really final (shows lack of standards)
echo "done" > /tmp/feature5.txt
cp /tmp/feature5.txt src/feature5.py
git add src/feature5.py
git commit -m "really final this time"

# Oops message
echo "oops" > /tmp/feature6.txt
cp /tmp/feature6.txt src/feature6.py
git add src/feature6.py
git commit -m "oops forgot something"

# Generic changes
echo "changes" > /tmp/feature7.txt
cp /tmp/feature7.txt src/feature7.py
git add src/feature7.py
git commit -m "changes"

# Cleanup these poor commits
git reset --hard HEAD~7
```

---

## Part 5: Create Stale Feature Branches

**Problem:** Multiple feature branches never merged or abandoned.

### Implementation

```bash
# Create feature branches that will never be merged
git checkout -b feature/payment-v1
echo "# Payment Processing v1" > src/payment_v1.py
git add src/payment_v1.py
git commit -m "Add payment processing module"
git commit --allow-empty -m "Update payment logic"
git commit --allow-empty -m "Add payment tests"

# Switch back to main and continue
git checkout main
git branch feature/payment-v1

# Create another abandoned feature branch
git checkout -b feature/new-dashboard
echo "# New Dashboard UI" > src/dashboard.py
git add src/dashboard.py
git commit -m "Initial dashboard implementation"
git commit --allow-empty -m "Add dashboard charts"
git commit --allow-empty -m "Dashboard styling"

git checkout main

# Create a stale branch that's way behind
git checkout -b feature/test-ui
echo "# UI Tests" > src/ui_tests.py
git add src/ui_tests.py
git commit -m "Add UI testing framework"

git checkout main

# Create a legacy-hotfix branch
git checkout -b legacy-hotfix
echo "# Legacy fix" > src/legacy_fix.py
git add src/legacy_fix.py
git commit -m "Apply critical hotfix to legacy code"

git checkout main

# These branches now exist and are unmerged
# Students can discover with: git branch -no-merged
```

---

## Part 6: Embed Hidden Issue #3 - Poor Merge Commits

**Problem:** Inefficient merge history and poor merge commit messages.

### Implementation

```bash
# Create a temporary feature on a branch
git checkout -b temp-feature
echo "temp feature" > /tmp/temp.py
cp /tmp/temp.py src/temp_feature.py
git add src/temp_feature.py
git commit -m "Add temporary feature"
git commit --allow-empty -m "Update temp feature"

# Merge without squashing, creating poor merge commit
git checkout main
git merge temp-feature --no-ff -m "Merge branch 'temp-feature'"

# This creates: "Merge branch 'temp-feature'" - uninformative

# Repeat with another poor merge
git checkout -b feature-x
echo "feature x" > src/feature_x.py
git add src/feature_x.py
git commit -m "Add feature X"

git checkout main
git merge feature-x --no-ff -m "Merge temp"

# This creates unnecessary merge commits in history
# Students should recognize that squashing would be better

# Cleanup branches
git branch -D temp-feature feature-x
```

---

## Part 7: Embed Hidden Issue #4 - Undocumented Hotfix

**Problem:** Production fix directly on main without documentation or issue reference.

### Implementation

```bash
# Simulate urgent hotfix committed directly to main (bad practice)
echo "# HOTFIX: Login timeout issue" > /tmp/hotfix.py
cat > src/hotfix_login.py << 'EOF'
# Urgent fix for login timeout
# Applied directly to production
# No issue tracking
# No documentation

SESSION_TIMEOUT = 3600  # Increased from 1800
EOF

git add src/hotfix_login.py
git commit -m "Hotfix login"

# Or even worse:
echo "quick fix" > src/quick_fix.py
git add src/quick_fix.py
git commit -m "fix"

# Students should identify:
# - No reference to issue/ticket
# - No documentation
# - Committed directly to main
# - Poor commit message
# - No code review approval indication
```

---

## Part 8: Embed Hidden Issue #5 - Missing Release Tags

**Problem:** Inconsistent or missing semantic versioning tags.

### Implementation

```bash
# Create inconsistent tags instead of semantic versions
git tag "release-final"
git tag "latest"
git tag "backup"
git tag "v1-final"

# These should be semantic versions like:
# git tag "v1.0.0"
# git tag "v1.0.1"
# git tag "v1.1.0"

# Students should identify that proper semver is missing
# Proper approach would be:
# git tag -d release-final
# git tag -d latest
# git tag -d backup
# git tag -d v1-final
# git tag "v1.0.0"  # Semantic version

# Students can discover this with: git tag -l
```

---

## Part 9: Embed Hidden Issue #6 - No Branch Protection Simulation

**Problem:** Repository documentation shows main branch accepts direct pushes.

### Implementation

This is simulated in documentation rather than actual Git settings since GitHub Actions are needed for real enforcement.

```markdown
# In docs/release-process.md add:

## Current Deployment Process
- Developers push directly to main for emergency fixes
- No branch protection enabled
- No required code review
- No automated tests blocking merge
- No CODEOWNERS policy
```

Students should recognize these are governance failures that need:
- Branch protection rules enabled
- Required status checks
- Required reviews (minimum 2 approvals)
- CODEOWNERS file
- Dismiss stale PR reviews

---

## Part 10: Embed Hidden Issue #7 - Unsafe Deployment Script

This is already embedded in deploy.sh:

```bash
# deploy.sh contains:
rm -rf /opt/enterprise/*  # Dangerous!
# No error handling
# No health checks
# No rollback mechanism
```

---

## Part 11: Complete Git History Sequence

Here's the complete sequence of commands to build the full repository:

```bash
#!/bin/bash
# Complete setup script for enterprise-repo-audit

cd enterprise-repo-audit

# Phase 1: Initial structure
git init
echo "# Enterprise Internal Platform" > README.md
git add README.md
git commit -m "Initial commit"

# Phase 2: Project structure
mkdir -p src config scripts docs .github/workflows
git add src config scripts docs .github/workflows
git commit -m "Add project structure"

# Phase 3: Application code
# [Add all the source files here]
git add src/
git commit -m "Add application source code"

# Phase 4: Infrastructure and configuration
git add config/
git commit -m "Add configuration templates"

# Phase 5: Scripts
git add scripts/
git commit -m "Add utility scripts"

# Phase 6: Documentation
git add docs/
git commit -m "Add documentation"

# Phase 7: CI/CD
git add .github/
git commit -m "Add CI pipeline"

# Phase 8: Exposed secret (then removed)
git add config/settings.env.example
git commit -m "Update production configuration"
# [Later remove the secret]
git add config/settings.env.example
git commit -m "Remove sensitive data"

# Phase 9: Create branches
git checkout -b feature/payment-v1
git add src/payment_v1.py
git commit -m "Add payment module"
git checkout main

git checkout -b feature/new-dashboard
git add src/dashboard.py
git commit -m "Add dashboard"
git checkout main

git checkout -b legacy-hotfix
git add src/legacy.py
git commit -m "Legacy system fix"
git checkout main

# Phase 10: Poor commits
echo "test" > src/test_feature.py
git add src/test_feature.py
git commit -m "fix"

# Phase 11: Merge commits with poor messages
git merge --no-ff feature/payment-v1 -m "Merge temp"

# Phase 12: Tagging (improper)
git tag "release-final"
git tag "latest"
git tag "backup"

echo "Repository setup complete!"
```

---

## Part 12: Verification Checklist

After setup, verify all hidden issues are embedded:

```bash
# Issue 1: Secret in history
git log -S "AWS_SECRET_ACCESS_KEY"  # Should find it

# Issue 2: Inconsistent commit messages
git log --oneline | grep -E "^[a-f0-9]+ (fix|asdf|temp|final|oops|changes)"

# Issue 3: Stale branches
git branch --no-merged  # Should show multiple branches

# Issue 4: Poor merge commits
git log --oneline | grep "Merge"

# Issue 5: No semantic versioning
git tag  # Should show non-semantic tags

# Issue 6: Undocumented hotfix
git log --oneline | grep -i hotfix

# Issue 7: Unsafe deploy script
grep "rm -rf" deploy.sh  # Should find dangerous command

# Issue 8: CI skips tests
grep "echo.*skipping" .github/workflows/ci.yml
```

---

## Part 13: Student Investigation Commands

Document which commands students should use to discover each issue:

### Secret Discovery
```bash
git log -S "AWS_SECRET_ACCESS_KEY"
git log -p --all -- config/settings.env.example
git show <commit-hash>
```

### Branch Issues
```bash
git branch -v
git branch --no-merged
git branch --merged
```

### Commit Message Issues
```bash
git log --oneline
git log --format=fuller
```

### Merge Issues
```bash
git log --graph --oneline --all
git log --format="%H %s"
```

### Tagging Issues
```bash
git tag
git tag -l
git show <tag-name>
```

### Deployment Script Issues
```bash
cat deploy.sh
bash -n deploy.sh  # Syntax check
```

---

## Part 14: Expected Student Findings

Students should discover:

1. **Security Issues**
   - Exposed AWS credentials in git history
   - API keys in configuration files

2. **Process Issues**
   - Poor commit message standards
   - Undocumented hotfix
   - Missing code review

3. **Governance Issues**
   - No branch protection
   - Inconsistent tagging
   - No deployment approval

4. **Technical Issues**
   - Unsafe deployment script
   - No error handling
   - No health checks
   - Missing backup strategy

5. **Documentation Issues**
   - Incomplete security policy
   - Incomplete release process
   - Incomplete contribution guidelines

---

## Part 15: Time Estimates

- Initial setup: 30 minutes
- Adding issues: 30 minutes
- Verification: 15 minutes
- **Total setup time: ~75 minutes**

Expected student investigation time: 45-60 minutes

---

## Part 16: Customization Options

Instructors can:

1. **Add more issues:**
   - Multiple commits with secrets
   - More stale branches
   - Database migration failures
   - Configuration inconsistencies

2. **Adjust difficulty:**
   - Remove some issues for beginner level
   - Add more subtle issues for advanced level
   - Create levels: Easy (5 issues), Medium (8 issues), Hard (12+ issues)

3. **Add context-specific issues:**
   - For teams using specific deployment tools
   - For teams with specific compliance requirements
   - For teams with specific monitoring systems

4. **Create variants:**
   - Monorepo variant with multiple services
   - Microservices variant with service mesh
   - Infrastructure-as-Code variant

---

## Part 17: Grading Rubric

Students should be evaluated on:

| Criteria | Points | Description |
|----------|--------|-------------|
| Issue Discovery | 30 | Number and severity of issues found |
| Analysis Quality | 25 | Depth of root cause analysis |
| Evidence Gathering | 20 | Quality of git commands and output provided |
| Recommendations | 15 | Actionable remediation steps |
| Report Quality | 10 | Clarity and professionalism of report |
| **Total** | **100** | |

---

## Notes for Instructors

- Do not share this guide with students
- Repository should appear complete and professional
- Issues should be discoverable but not obvious
- Encourage students to use git forensics
- Provide git command reference if needed
- Consider time limit and adjust difficulty
- Collect reports for assessment

