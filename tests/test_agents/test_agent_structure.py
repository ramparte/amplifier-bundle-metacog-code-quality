"""
Tests for agent file structure and configuration.

Validates that all agent files follow Amplifier conventions.
"""

import pytest
import re
from pathlib import Path


def extract_yaml_frontmatter(content):
    """Extract YAML frontmatter from markdown file."""
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        return match.group(1)
    return None


def parse_simple_yaml(yaml_content):
    """Simple YAML parser for basic key-value and list structures."""
    result = {}
    current_key = None
    current_list = []
    indent_level = 0
    
    for line in yaml_content.split('\n'):
        if not line.strip():
            continue
            
        # Count indentation
        indent = len(line) - len(line.lstrip())
        
        # Top-level key
        if indent == 0 and ':' in line:
            if current_key and current_list:
                result[current_key] = current_list
                current_list = []
            
            key, value = line.split(':', 1)
            current_key = key.strip()
            value = value.strip()
            
            if value:
                result[current_key] = value
            else:
                result[current_key] = {}
        
        # Nested key-value
        elif indent > 0 and ':' in line and not line.strip().startswith('-'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            
            if isinstance(result.get(current_key), dict):
                result[current_key][key] = value
        
        # List item
        elif line.strip().startswith('-'):
            item = line.strip()[1:].strip()
            current_list.append(item)
    
    # Add final list
    if current_key and current_list:
        result[current_key] = current_list
    
    return result


class TestAgentFiles:
    """Test that all agent files exist and are properly structured."""
    
    def test_all_expected_agents_exist(self, agents_dir, expected_agents):
        """Verify all expected agent files exist."""
        for agent_name in expected_agents:
            agent_file = agents_dir / f"{agent_name}.md"
            assert agent_file.exists(), f"Agent file missing: {agent_name}.md"
    
    def test_no_unexpected_agent_files(self, agents_dir, expected_agents):
        """Verify no unexpected agent files exist."""
        agent_files = list(agents_dir.glob("*.md"))
        expected_files = {f"{name}.md" for name in expected_agents}
        actual_files = {f.name for f in agent_files}
        
        unexpected = actual_files - expected_files
        assert not unexpected, f"Unexpected agent files: {unexpected}"
    
    def test_agent_file_not_empty(self, agent_file):
        """Verify agent file is not empty."""
        content = agent_file.read_text()
        assert len(content) > 100, f"Agent file too small: {agent_file.name}"


class TestAgentYAMLFrontmatter:
    """Test YAML frontmatter in agent files."""
    
    def test_agent_has_yaml_frontmatter(self, agent_file):
        """Verify agent has YAML frontmatter."""
        content = agent_file.read_text()
        yaml = extract_yaml_frontmatter(content)
        assert yaml is not None, f"Missing YAML frontmatter in {agent_file.name}"
    
    def test_agent_has_meta_section(self, agent_file):
        """Verify agent has meta section in frontmatter."""
        content = agent_file.read_text()
        yaml = extract_yaml_frontmatter(content)
        parsed = parse_simple_yaml(yaml)
        
        assert 'meta' in parsed, f"Missing 'meta' section in {agent_file.name}"
    
    def test_agent_has_name(self, agent_file):
        """Verify agent has name in meta section."""
        content = agent_file.read_text()
        yaml = extract_yaml_frontmatter(content)
        
        assert 'name:' in yaml, f"Missing 'name' field in {agent_file.name}"
    
    def test_agent_has_description(self, agent_file):
        """Verify agent has description in meta section."""
        content = agent_file.read_text()
        yaml = extract_yaml_frontmatter(content)
        
        assert 'description:' in yaml, f"Missing 'description' field in {agent_file.name}"
    
    def test_agent_name_matches_filename(self, agent_file):
        """Verify agent name matches filename."""
        content = agent_file.read_text()
        yaml = extract_yaml_frontmatter(content)
        
        # Extract name value
        name_match = re.search(r'name:\s*(\S+)', yaml)
        if name_match:
            name = name_match.group(1)
            expected_name = agent_file.stem  # filename without .md
            assert name == expected_name, \
                f"Agent name '{name}' doesn't match filename '{expected_name}'"
    
    def test_agent_has_tools_section(self, agent_file):
        """Verify agent has tools section."""
        content = agent_file.read_text()
        yaml = extract_yaml_frontmatter(content)
        
        assert 'tools:' in yaml, f"Missing 'tools' section in {agent_file.name}"
    
    def test_agent_has_providers_section(self, agent_file):
        """Verify agent has providers section."""
        content = agent_file.read_text()
        yaml = extract_yaml_frontmatter(content)
        
        assert 'providers:' in yaml, f"Missing 'providers' section in {agent_file.name}"
    
    def test_agent_provider_has_module(self, agent_file):
        """Verify provider configuration has module."""
        content = agent_file.read_text()
        yaml = extract_yaml_frontmatter(content)
        
        assert 'module:' in yaml, f"Provider missing 'module' in {agent_file.name}"
    
    def test_agent_uses_anthropic_provider(self, agent_file):
        """Verify agent uses provider-anthropic."""
        content = agent_file.read_text()
        yaml = extract_yaml_frontmatter(content)
        
        assert 'provider-anthropic' in yaml, \
            f"Agent should use provider-anthropic in {agent_file.name}"
    
    def test_agent_has_temperature_setting(self, agent_file):
        """Verify agent has temperature configuration."""
        content = agent_file.read_text()
        yaml = extract_yaml_frontmatter(content)
        
        assert 'temperature:' in yaml, \
            f"Missing temperature setting in {agent_file.name}"
    
    def test_agent_temperature_in_valid_range(self, agent_file):
        """Verify temperature is between 0.0 and 1.0."""
        content = agent_file.read_text()
        yaml = extract_yaml_frontmatter(content)
        
        temp_match = re.search(r'temperature:\s*([\d.]+)', yaml)
        if temp_match:
            temp = float(temp_match.group(1))
            assert 0.0 <= temp <= 1.0, \
                f"Temperature {temp} out of range in {agent_file.name}"


class TestAgentContent:
    """Test agent markdown content."""
    
    def test_agent_has_role_description(self, agent_file):
        """Verify agent has 'Your Role' or similar section."""
        content = agent_file.read_text()
        
        has_role = (
            '## Your Role' in content or
            '## Role' in content or
            'You are' in content or
            'You analyze' in content
        )
        
        assert has_role, f"Missing role description in {agent_file.name}"
    
    def test_agent_has_output_format(self, agent_file):
        """Verify agent describes output format."""
        content = agent_file.read_text()
        
        has_output = (
            '## Output Format' in content or
            'Output:' in content or
            'Returns:' in content or
            'json' in content.lower()
        )
        
        assert has_output, f"Missing output format in {agent_file.name}"
    
    def test_agent_has_example_usage(self, agent_file):
        """Verify agent has usage examples."""
        content = agent_file.read_text()
        
        has_example = (
            '## Example' in content or
            '```bash' in content or
            'amplifier task' in content
        )
        
        assert has_example, f"Missing usage examples in {agent_file.name}"
    
    def test_agent_markdown_is_well_formed(self, agent_file):
        """Verify agent markdown is well-formed."""
        content = agent_file.read_text()
        
        # Should have headers
        assert content.count('#') >= 3, \
            f"Too few headers in {agent_file.name}"
        
        # Should have code blocks for examples
        assert '```' in content, \
            f"No code blocks in {agent_file.name}"


class TestAgentContextReferences:
    """Test context file references in agents."""
    
    def test_agent_references_context_files(self, agent_file, context_dir):
        """Verify agents reference context files that exist."""
        content = agent_file.read_text()
        
        # Find context references: @code-quality:context/filename.md
        pattern = r'@code-quality:context/([^\s]+\.md)'
        references = re.findall(pattern, content)
        
        # quality-aggregator might not reference context
        if agent_file.name == 'quality-aggregator.md':
            return  # Optional for aggregator
        
        # Other agents should reference context
        assert len(references) > 0, \
            f"No context references in {agent_file.name}"
        
        # Verify referenced files exist
        for ref in references:
            context_file = context_dir / ref
            assert context_file.exists(), \
                f"Referenced context file missing: {ref} (from {agent_file.name})"
    
    def test_context_reference_format(self, agent_file):
        """Verify context references use correct format."""
        content = agent_file.read_text()
        
        # Should use @code-quality:context/ format
        if '@' in content and 'context' in content:
            pattern = r'@code-quality:context/[\w-]+\.md'
            matches = re.findall(pattern, content)
            
            # If has context references, should be properly formatted
            wrong_pattern = r'@context/|@[^:]+context/'
            wrong_matches = re.findall(wrong_pattern, content)
            
            assert not wrong_matches or matches, \
                f"Malformed context reference in {agent_file.name}"


def test_all_agents_have_unique_names(all_agent_files):
    """Verify all agent names are unique."""
    names = []
    
    for agent_file in all_agent_files:
        content = agent_file.read_text()
        yaml = extract_yaml_frontmatter(content)
        if yaml:
            name_match = re.search(r'name:\s*(\S+)', yaml)
            if name_match:
                names.append(name_match.group(1))
    
    assert len(names) == len(set(names)), \
        f"Duplicate agent names found: {names}"


def test_collection_has_expected_agent_count(all_agent_files, expected_agents):
    """Verify collection has expected number of agents."""
    assert len(all_agent_files) == len(expected_agents), \
        f"Expected {len(expected_agents)} agents, found {len(all_agent_files)}"
