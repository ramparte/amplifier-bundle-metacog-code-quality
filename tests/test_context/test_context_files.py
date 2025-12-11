"""
Tests for context files.

Validates that all context files exist and contain expected content.
"""

import pytest
from pathlib import Path


class TestContextFileExistence:
    """Test that all context files exist."""
    
    def test_all_expected_context_files_exist(self, context_dir, expected_context_files):
        """Verify all expected context files exist."""
        for filename in expected_context_files:
            context_file = context_dir / filename
            assert context_file.exists(), f"Context file missing: {filename}"
    
    def test_context_files_not_empty(self, context_dir, expected_context_files):
        """Verify context files are not empty."""
        for filename in expected_context_files:
            context_file = context_dir / filename
            content = context_file.read_text()
            assert len(content) > 1000, \
                f"Context file too small: {filename} ({len(content)} bytes)"
    
    def test_no_unexpected_context_files(self, context_dir, expected_context_files):
        """Verify no unexpected context files exist."""
        context_files = list(context_dir.glob("*.md"))
        expected_set = set(expected_context_files)
        actual_set = {f.name for f in context_files}
        
        unexpected = actual_set - expected_set
        assert not unexpected, f"Unexpected context files: {unexpected}"


class TestContextFileContent:
    """Test content quality of context files."""
    
    def test_context_file_has_title(self, context_dir, expected_context_files):
        """Verify each context file has a title."""
        for filename in expected_context_files:
            content = (context_dir / filename).read_text()
            assert content.startswith('#'), \
                f"Context file missing title: {filename}"
    
    def test_context_file_has_sections(self, context_dir, expected_context_files):
        """Verify context files have multiple sections."""
        for filename in expected_context_files:
            content = (context_dir / filename).read_text()
            section_count = content.count('##')
            assert section_count >= 3, \
                f"Too few sections in {filename} ({section_count} sections)"
    
    def test_context_file_has_examples(self, context_dir, expected_context_files):
        """Verify context files include code examples."""
        for filename in expected_context_files:
            content = (context_dir / filename).read_text()
            has_examples = '```' in content
            assert has_examples, \
                f"No code examples in {filename}"


class TestSpecificContextFiles:
    """Test specific context files have expected content."""
    
    def test_code_smells_has_complexity_patterns(self, context_dir):
        """Verify code-smells-patterns.md covers complexity."""
        content = (context_dir / "code-smells-patterns.md").read_text()
        
        expected_terms = [
            'complexity',
            'cyclomatic',
            'nesting',
            'function'
        ]
        
        for term in expected_terms:
            assert term.lower() in content.lower(), \
                f"Missing '{term}' in code-smells-patterns.md"
    
    def test_security_has_injection_patterns(self, context_dir):
        """Verify security-patterns.md covers injection vulnerabilities."""
        content = (context_dir / "security-patterns.md").read_text()
        
        expected_terms = [
            'SQL injection',
            'XSS',
            'command injection',
            'hardcoded secret'
        ]
        
        for term in expected_terms:
            assert term.lower() in content.lower(), \
                f"Missing '{term}' in security-patterns.md"
    
    def test_performance_has_algorithm_patterns(self, context_dir):
        """Verify performance-patterns.md covers algorithm complexity."""
        content = (context_dir / "performance-patterns.md").read_text()
        
        expected_terms = [
            'O(n²)',
            'nested loop',
            'N+1',
            'performance'
        ]
        
        for term in expected_terms:
            assert term.lower() in content.lower(), \
                f"Missing '{term}' in performance-patterns.md"
    
    def test_documentation_has_docstring_standards(self, context_dir):
        """Verify documentation-standards.md covers docstrings."""
        content = (context_dir / "documentation-standards.md").read_text()
        
        expected_terms = [
            'docstring',
            'README',
            'documentation',
            'comment'
        ]
        
        for term in expected_terms:
            assert term.lower() in content.lower(), \
                f"Missing '{term}' in documentation-standards.md"


class TestContextFileSizes:
    """Test context files are appropriately sized."""
    
    def test_context_files_comprehensive(self, context_dir, expected_context_files):
        """Verify context files are comprehensive (>2KB each)."""
        for filename in expected_context_files:
            path = context_dir / filename
            size = path.stat().st_size
            assert size > 2000, \
                f"Context file too small: {filename} ({size} bytes)"
    
    def test_context_files_not_too_large(self, context_dir, expected_context_files):
        """Verify context files aren't excessively large (>50KB)."""
        for filename in expected_context_files:
            path = context_dir / filename
            size = path.stat().st_size
            assert size < 50000, \
                f"Context file too large: {filename} ({size} bytes) - consider splitting"
