# Security Vulnerability Patterns

Reference guide for security scanning agents.

## Injection Attacks

### SQL Injection
**Pattern:** User input in SQL queries without sanitization
**Risk:** Database compromise, data theft
**Detection:**
- String concatenation in SQL: `"SELECT * FROM " + table`
- F-strings with variables: `f"SELECT * FROM {table}"`
- `.format()` with user input

**Safe Patterns:**
- Parameterized queries: `cursor.execute("SELECT * FROM users WHERE id = ?", (id,))`
- ORM usage: `User.objects.filter(id=user_id)`

### Command Injection
**Pattern:** User input passed to shell commands
**Risk:** System compromise, arbitrary code execution
**Detection:**
- `os.system()` with variables
- `subprocess.call()` with `shell=True` and user input
- `eval()` or `exec()` with user data

### XSS (Cross-Site Scripting)
**Pattern:** Unescaped user content in HTML
**Risk:** Session hijacking, data theft
**Detection:**
- Direct HTML construction with user data
- `.innerHTML` with user content (JavaScript)
- Template rendering without escaping

## Authentication & Authorization

### Weak Password Handling
**Patterns:**
- Plaintext password storage
- Weak hashing (MD5, SHA1 for passwords)
- No salt in password hashing
- Hardcoded passwords

**Regex Patterns:**
```regex
password\s*=\s*['"][^'"]+['"]
pwd\s*=\s*['"][^'"]+['"]
pass\s*=\s*['"][^'"]+['"]
```

### Missing Authorization
**Pattern:** No access control checks before operations
**Detection:**
- Endpoints without auth decorators
- Direct database access without user context
- No role/permission checks

### Insecure Session Management
**Patterns:**
- No session timeout
- Session ID in URL
- Predictable session tokens
- No secure/httponly flags on cookies

## Data Exposure

### Hardcoded Secrets
**High-Risk Patterns:**
```regex
# API Keys
api[_-]?key\s*=\s*['"][a-zA-Z0-9]{20,}['"]
secret[_-]?key\s*=\s*['"][a-zA-Z0-9]{20,}['"]

# AWS Keys
AKIA[0-9A-Z]{16}

# GitHub Tokens
ghp_[a-zA-Z0-9]{36}
github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}

# Private Keys
-----BEGIN.*PRIVATE KEY-----

# Database URLs with passwords
mongodb:\/\/[^:]+:[^@]+@
postgresql:\/\/[^:]+:[^@]+@
mysql:\/\/[^:]+:[^@]+@
```

### Sensitive Data in Logs
**Pattern:** Logging passwords, tokens, PII
**Detection:**
- `log.*password`
- `print.*token`
- `logger.*secret`

### Information Disclosure
**Patterns:**
- Stack traces in production
- Debug mode enabled in production
- Version information exposed
- Directory listings enabled

## Cryptography Issues

### Weak Algorithms
**Deprecated/Weak:**
- MD5, SHA1 for passwords (use bcrypt, Argon2)
- DES, 3DES encryption (use AES-256)
- RSA <2048 bits (use 2048+ bits)

**Detection:**
```python
# Python
hashlib.md5()  # Weak
hashlib.sha1()  # Weak for passwords
```

### Insecure Random
**Pattern:** Predictable randomness for security
**Detection:**
- `random.random()` for tokens/keys (use `secrets` module)
- `Math.random()` in JavaScript for security tokens

### Missing TLS/SSL
**Pattern:** Sensitive data over HTTP
**Detection:**
- `http://` URLs for API calls with credentials
- Disabled SSL verification: `verify=False`

## Common Vulnerability Examples

### Python Examples

```python
# ❌ SQL Injection
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ Safe
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# ❌ Command Injection
os.system(f"ping {user_input}")

# ✅ Safe
subprocess.run(["ping", "-c", "1", user_input])

# ❌ Hardcoded Secret
API_KEY = "sk-1234567890abcdef"

# ✅ Safe
API_KEY = os.getenv("API_KEY")

# ❌ Weak Password Hashing
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ Safe
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# ❌ Insecure Random
token = ''.join(random.choices(string.ascii_letters, k=32))

# ✅ Safe
token = secrets.token_urlsafe(32)
```

### JavaScript Examples

```javascript
// ❌ XSS
element.innerHTML = userInput;

// ✅ Safe
element.textContent = userInput;

// ❌ Command Injection
exec(`ping ${userInput}`);

// ✅ Safe
execFile('ping', ['-c', '1', userInput]);

// ❌ Insecure Random
const token = Math.random().toString(36);

// ✅ Safe
const token = crypto.randomBytes(32).toString('hex');
```

## CWE Mappings

Map findings to Common Weakness Enumeration:
- SQL Injection: CWE-89
- XSS: CWE-79
- Command Injection: CWE-78
- Path Traversal: CWE-22
- Hardcoded Credentials: CWE-798
- Weak Crypto: CWE-327
- Missing Auth: CWE-862
- Insecure Deserialization: CWE-502

## Severity Assessment

**Critical:**
- Remote code execution possible
- Authentication bypass
- SQL injection with admin access
- Hardcoded production credentials

**High:**
- Data exposure (PII, financial)
- XSS on authenticated pages
- CSRF on state-changing operations
- Weak cryptography for sensitive data

**Medium:**
- Information disclosure (non-sensitive)
- Missing security headers
- Outdated dependencies with CVEs
- Insufficient logging

**Low:**
- Minor configuration issues
- Non-exploitable information leakage
- Weak session configuration (with mitigations)

## OWASP Top 10 Coverage

1. **Broken Access Control** - Missing authorization checks
2. **Cryptographic Failures** - Weak algorithms, hardcoded secrets
3. **Injection** - SQL, command, code injection
4. **Insecure Design** - Security flaws in architecture
5. **Security Misconfiguration** - Debug mode, default configs
6. **Vulnerable Components** - Outdated dependencies
7. **Identification and Authentication Failures** - Weak auth
8. **Software and Data Integrity Failures** - Insecure deserialization
9. **Security Logging Failures** - Insufficient logging
10. **Server-Side Request Forgery** - Unvalidated URLs

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE List](https://cwe.mitre.org/)
- [SANS Top 25](https://www.sans.org/top25-software-errors/)
