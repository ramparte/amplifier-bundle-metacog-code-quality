"""
Pytest fixtures for code-quality collection tests.

Provides common fixtures for testing agent files, YAML parsing, and context references.
"""

import pytest
from pathlib import Path


@pytest.fixture
def collection_dir():
    """Return path to collection root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def agents_dir(collection_dir):
    """Return path to agents directory."""
    return collection_dir / "agents"


@pytest.fixture
def context_dir(collection_dir):
    """Return path to context directory."""
    return collection_dir / "context"


@pytest.fixture
def all_agent_files(agents_dir):
    """Return list of all agent markdown files."""
    return sorted(agents_dir.glob("*.md"))


@pytest.fixture(params=[
    "static-analyzer.md",
    "security-scanner.md",
    "performance-analyzer.md",
    "documentation-checker.md",
    "quality-aggregator.md"
])
def agent_file(request, agents_dir):
    """Parametrized fixture for each agent file."""
    return agents_dir / request.param


@pytest.fixture
def expected_agents():
    """Return list of expected agent names."""
    return [
        "static-analyzer",
        "security-scanner",
        "performance-analyzer",
        "documentation-checker",
        "quality-aggregator"
    ]


@pytest.fixture
def expected_context_files():
    """Return list of expected context files."""
    return [
        "code-smells-patterns.md",
        "security-patterns.md",
        "performance-patterns.md",
        "documentation-standards.md"
    ]
