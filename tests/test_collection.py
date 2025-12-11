"""
Tests for overall collection structure and metadata.

Validates pyproject.toml, README, and overall collection structure.
"""

import pytest
from pathlib import Path


class TestCollectionStructure:
    """Test collection directory structure."""
    
    def test_required_directories_exist(self, collection_dir):
        """Verify all required directories exist."""
        required_dirs = ['agents', 'context', 'profiles', 'tests', 'examples']
        
        for dirname in required_dirs:
            dir_path = collection_dir / dirname
            assert dir_path.exists(), f"Missing required directory: {dirname}"
            assert dir_path.is_dir(), f"Not a directory: {dirname}"
    
    def test_required_files_exist(self, collection_dir):
        """Verify required project files exist."""
        required_files = [
            'pyproject.toml',
            'README.md',
            'LICENSE'
        ]
        
        for filename in required_files:
            file_path = collection_dir / filename
            assert file_path.exists(), f"Missing required file: {filename}"
            assert file_path.is_file(), f"Not a file: {filename}"


class TestPyprojectToml:
    """Test pyproject.toml configuration."""
    
    def test_pyproject_has_project_section(self, collection_dir):
        """Verify pyproject.toml has [project] section."""
        content = (collection_dir / 'pyproject.toml').read_text()
        assert '[project]' in content
    
    def test_pyproject_has_name(self, collection_dir):
        """Verify pyproject.toml has name field."""
        content = (collection_dir / 'pyproject.toml').read_text()
        assert 'name = "code-quality"' in content
    
    def test_pyproject_has_version(self, collection_dir):
        """Verify pyproject.toml has version."""
        content = (collection_dir / 'pyproject.toml').read_text()
        assert 'version =' in content
    
    def test_pyproject_has_description(self, collection_dir):
        """Verify pyproject.toml has description."""
        content = (collection_dir / 'pyproject.toml').read_text()
        assert 'description =' in content
    
    def test_pyproject_has_amplifier_section(self, collection_dir):
        """Verify pyproject.toml has [tool.amplifier.collection] section."""
        content = (collection_dir / 'pyproject.toml').read_text()
        assert '[tool.amplifier.collection]' in content
    
    def test_pyproject_has_capabilities(self, collection_dir):
        """Verify pyproject.toml lists capabilities."""
        content = (collection_dir / 'pyproject.toml').read_text()
        assert 'capabilities =' in content
        
        expected_capabilities = [
            'static-analysis',
            'security-scanning',
            'performance-analysis',
            'documentation-checking'
        ]
        
        for capability in expected_capabilities:
            assert capability in content, \
                f"Missing capability: {capability}"


class TestReadme:
    """Test README.md documentation."""
    
    def test_readme_not_empty(self, collection_dir):
        """Verify README is not empty."""
        content = (collection_dir / 'README.md').read_text()
        assert len(content) > 1000, "README too short"
    
    def test_readme_has_title(self, collection_dir):
        """Verify README has title."""
        content = (collection_dir / 'README.md').read_text()
        assert content.startswith('#'), "README missing title"
    
    def test_readme_has_installation_section(self, collection_dir):
        """Verify README has installation instructions."""
        content = (collection_dir / 'README.md').read_text()
        has_installation = (
            '## Installation' in content or
            '### Installation' in content or
            'install' in content.lower()
        )
        assert has_installation
    
    def test_readme_has_usage_examples(self, collection_dir):
        """Verify README has usage examples."""
        content = (collection_dir / 'README.md').read_text()
        has_examples = (
            '## Usage' in content or
            '```bash' in content or
            'amplifier task' in content
        )
        assert has_examples
    
    def test_readme_describes_all_agents(self, collection_dir, expected_agents):
        """Verify README mentions all agents."""
        content = (collection_dir / 'README.md').read_text()
        
        for agent_name in expected_agents:
            assert agent_name in content, \
                f"README doesn't mention agent: {agent_name}"


class TestExamples:
    """Test example files."""
    
    def test_examples_directory_has_content(self, collection_dir):
        """Verify examples directory has at least one example."""
        examples_dir = collection_dir / 'examples'
        examples = list(examples_dir.glob('*.md'))
        assert len(examples) >= 1, "No example files found"
    
    def test_example_file_not_empty(self, collection_dir):
        """Verify example files are not empty."""
        examples_dir = collection_dir / 'examples'
        for example_file in examples_dir.glob('*.md'):
            content = example_file.read_text()
            assert len(content) > 500, \
                f"Example too short: {example_file.name}"


class TestLicense:
    """Test LICENSE file."""
    
    def test_license_exists(self, collection_dir):
        """Verify LICENSE file exists."""
        license_file = collection_dir / 'LICENSE'
        assert license_file.exists()
    
    def test_license_not_empty(self, collection_dir):
        """Verify LICENSE is not empty."""
        content = (collection_dir / 'LICENSE').read_text()
        assert len(content) > 100
    
    def test_license_is_mit(self, collection_dir):
        """Verify LICENSE is MIT license."""
        content = (collection_dir / 'LICENSE').read_text()
        assert 'MIT' in content


def test_collection_is_complete(collection_dir, expected_agents, expected_context_files):
    """Integration test: verify collection is complete."""
    # Check agents
    agents_dir = collection_dir / 'agents'
    agent_files = list(agents_dir.glob('*.md'))
    assert len(agent_files) == len(expected_agents)
    
    # Check context
    context_dir = collection_dir / 'context'
    context_files = list(context_dir.glob('*.md'))
    assert len(context_files) == len(expected_context_files)
    
    # Check project files
    assert (collection_dir / 'pyproject.toml').exists()
    assert (collection_dir / 'README.md').exists()
    assert (collection_dir / 'LICENSE').exists()
