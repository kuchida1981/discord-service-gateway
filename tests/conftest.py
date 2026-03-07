"""Test configuration and fixtures."""

import os

# Set required environment variables before any modules are imported
os.environ.setdefault("N8N_HEALTH_URL", "https://n8n.example.com/healthz")
os.environ.setdefault("N8N_TASKS_LIST_URL", "https://n8n.example.com/webhook/tasks-list")
