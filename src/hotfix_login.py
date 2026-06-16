"""
HOTFIX: Login timeout issue resolved
Applied directly to production - no documentation
No issue tracking number
No code review - emergency fix
"""

# Increased session timeout from 1800 to 3600
SESSION_TIMEOUT_SECONDS = 3600

# Cached user sessions
_session_cache = {}
