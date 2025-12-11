# Documentation Standards

Reference guide for documentation quality assessment.

## Docstring Standards

### Python Docstrings

**Required Elements:**
- Brief description (one line)
- Detailed description (if needed)
- Parameters (Args)
- Return value (Returns)
- Exceptions (Raises)
- Examples (optional but recommended)

**Google Style (Recommended):**
```python
def process_payment(amount: float, currency: str, user_id: int) -> dict:
    """Process a payment transaction.
    
    Validates the payment amount and currency, then charges the user's
    default payment method.
    
    Args:
        amount: Payment amount (must be positive)
        currency: Three-letter currency code (e.g., 'USD', 'EUR')
        user_id: ID of the user making the payment
        
    Returns:
        dict: Transaction details with keys:
            - transaction_id (str): Unique transaction identifier
            - status (str): 'success' or 'failed'
            - timestamp (datetime): When transaction occurred
            
    Raises:
        ValueError: If amount is negative or currency invalid
        UserNotFoundError: If user_id doesn't exist
        PaymentError: If payment processing fails
        
    Example:
        >>> result = process_payment(29.99, 'USD', user_id=123)
        >>> print(result['status'])
        'success'
    """
    pass
```

**NumPy Style:**
```python
def calculate_metrics(data, normalize=True):
    """Calculate statistical metrics from data.
    
    Parameters
    ----------
    data : array_like
        Input data array
    normalize : bool, optional
        Whether to normalize results (default is True)
        
    Returns
    -------
    dict
        Dictionary containing:
        - mean : float
        - std : float
        - median : float
    """
    pass
```

### JavaScript/TypeScript Docstrings (JSDoc)

```javascript
/**
 * Process a payment transaction.
 * 
 * @param {number} amount - Payment amount (must be positive)
 * @param {string} currency - Three-letter currency code
 * @param {number} userId - ID of the user making payment
 * @returns {Promise<Object>} Transaction details
 * @throws {ValueError} If amount is negative
 * 
 * @example
 * const result = await processPayment(29.99, 'USD', 123);
 * console.log(result.status); // 'success'
 */
async function processPayment(amount, currency, userId) {
    // implementation
}
```

## Documentation Coverage Requirements

### Public APIs: 100%
All public functions, classes, and methods must be documented:
- Module-level docstrings
- Class docstrings
- Public method docstrings
- Public function docstrings

### Internal Functions: 50%+
Complex internal functions should be documented:
- Document if logic is non-obvious
- Document if reused in multiple places
- Simple helpers may skip docstrings

### Examples: Recommended
Provide examples for:
- Complex functions
- Public APIs
- Non-obvious usage patterns

## Comment Standards

### Good Comments (Explain WHY)

```python
# Use binary search because dataset is pre-sorted and large
result = binary_search(sorted_data, target)

# Retry up to 3 times to handle transient network issues
for attempt in range(3):
    try:
        response = api_call()
        break
    except NetworkError:
        time.sleep(2 ** attempt)

# Cache for 5 minutes to reduce database load during traffic spikes
@cache(timeout=300)
def get_user_data(user_id):
    pass
```

### Bad Comments (State the Obvious)

```python
# ❌ Obvious comment
# Increment counter
counter += 1

# ❌ Redundant comment
# Loop through items
for item in items:

# ❌ Commented-out code
# old_function()  # Not needed anymore
```

### TODO Comments

Format: `# TODO: description (author, date)`

```python
# TODO: Add input validation (Alice, 2025-12-01)
# FIXME: Memory leak when processing large files (Bob, 2025-11-15)
# HACK: Temporary workaround for bug in library v1.2 (Charlie, 2025-10-20)
```

## README Requirements

### Essential Sections

1. **Title and Description**
   - Project name
   - One-line description
   - Badges (build status, coverage, version)

2. **Installation**
   ```bash
   pip install package-name
   # or
   npm install package-name
   ```

3. **Quick Start**
   - Minimal working example
   - Common use case

4. **Usage Examples**
   - Code examples with output
   - Common scenarios

5. **API Reference** (or link to docs)
   - Key functions/classes
   - Parameters and return values

6. **Contributing**
   - How to contribute
   - Development setup
   - Testing instructions

7. **License**
   - License type
   - Copyright information

### Optional but Recommended

- **Features**: Key capabilities
- **Requirements**: System/language requirements
- **Configuration**: Environment variables, config files
- **FAQ**: Common questions
- **Changelog**: Version history
- **Credits**: Acknowledgments

## API Documentation

### REST API Documentation

Each endpoint needs:
```markdown
### POST /api/users

Create a new user account.

**Request:**
```json
{
  "username": "string (required, 3-20 chars)",
  "email": "string (required, valid email)",
  "password": "string (required, min 8 chars)"
}
```

**Response (201 Created):**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "created_at": "ISO8601 datetime"
}
```

**Errors:**
- 400: Invalid input (validation failed)
- 409: Username or email already exists
- 500: Internal server error

**Example:**
```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "secret123"}'
```
```

## Type Hints (Python)

Use type hints for clarity:

```python
from typing import List, Dict, Optional, Union

def process_items(
    items: List[Dict[str, any]],
    config: Optional[Dict[str, str]] = None
) -> Union[List[str], None]:
    """Process items according to configuration."""
    pass
```

## Documentation Anti-Patterns

### Missing Documentation
- Public functions without docstrings
- No README file
- No installation instructions

### Outdated Documentation
- Docstring doesn't match current parameters
- Examples use deprecated API
- README refers to old project structure

### Over-Documentation
- Obvious code documented extensively
- Every variable explained
- Documentation longer than code

### Poor Examples
- Examples that don't run
- Examples without context
- No example output shown

## Documentation Quality Metrics

### Coverage
- Docstring coverage: % of public functions with docstrings
- README completeness: % of required sections present
- Example coverage: % of public APIs with examples

### Quality
- **Good**: Clear, concise, accurate
- **Fair**: Present but minimal
- **Poor**: Outdated, incorrect, or misleading

### Scoring

**Documentation Score = (Coverage × 0.6) + (Quality × 0.4)**

**Thresholds:**
- Excellent: 90-100%
- Good: 75-89%
- Fair: 60-74%
- Poor: <60%

## Language-Specific Standards

### Python
- Follow PEP 257 (Docstring Conventions)
- Use type hints (PEP 484)
- Google, NumPy, or Sphinx style

### JavaScript/TypeScript
- Use JSDoc for documentation
- TypeScript types supplement docs
- ESDoc for generated documentation

### Java
- Use Javadoc for all public APIs
- Include @param, @return, @throws

## Tools and Automation

### Documentation Generators
- Python: Sphinx, pdoc, mkdocs
- JavaScript: JSDoc, TypeDoc
- Java: Javadoc

### Linters
- Python: pydocstyle, darglint
- JavaScript: ESLint (jsdoc plugin)

### Coverage Tools
- interrogate (Python docstring coverage)
- documentation-coverage (Node.js)

## Examples of Good Documentation

### Well-Documented Function
```python
def retry_with_backoff(
    func: Callable,
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
) -> any:
    """Retry a function with exponential backoff.
    
    Executes the given function, retrying on specified exceptions
    with exponentially increasing delays between attempts.
    
    Args:
        func: The function to execute
        max_attempts: Maximum number of retry attempts (default: 3)
        initial_delay: Initial delay in seconds (default: 1.0)
        backoff_factor: Multiplier for delay after each attempt (default: 2.0)
        exceptions: Tuple of exceptions to catch (default: (Exception,))
        
    Returns:
        The return value of func if successful
        
    Raises:
        The last exception raised if all attempts fail
        
    Example:
        >>> def flaky_api_call():
        ...     return requests.get('https://api.example.com/data')
        >>> result = retry_with_backoff(flaky_api_call, max_attempts=5)
        
    Note:
        Delays are: 1s, 2s, 4s, 8s, etc. (exponential backoff)
    """
    pass
```

### Well-Documented Class
```python
class UserRepository:
    """Repository for user data access.
    
    Provides methods to create, read, update, and delete user records
    from the database. Implements caching for frequently accessed users.
    
    Attributes:
        db: Database connection instance
        cache: Cache instance for user data (expires after 5 minutes)
        
    Example:
        >>> repo = UserRepository(db_connection)
        >>> user = repo.get_by_id(123)
        >>> user.email
        'alice@example.com'
    """
    
    def __init__(self, db: Database):
        """Initialize repository with database connection."""
        pass
        
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve user by ID with caching."""
        pass
```

## Severity Guidelines

**High Priority:**
- Missing docstrings on public APIs
- README completely missing or minimal
- No installation/usage instructions

**Medium Priority:**
- Incomplete docstrings (missing parameters/returns)
- Outdated examples
- Missing type hints

**Low Priority:**
- Minor formatting issues
- Could use more examples
- Internal functions without docstrings

## Best Practices

1. **Write docs as you code**: Don't defer documentation
2. **Keep docs DRY**: Reference, don't repeat
3. **Show, don't tell**: Examples > descriptions
4. **Update with code**: Outdated docs worse than no docs
5. **Test examples**: Ensure examples actually work
