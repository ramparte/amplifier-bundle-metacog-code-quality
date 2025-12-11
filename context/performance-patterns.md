# Performance Anti-Patterns

Reference guide for performance analysis.

## Algorithm Complexity Anti-Patterns

### Nested Loops (O(n²))
**Problem:** Quadratic time complexity
**Detection:** Two loops, one nested in another, iterating over same/related data
**Impact:** 1000 items = 1M operations

```python
# ❌ O(n²)
for user in users:
    for post in posts:
        if post.user_id == user.id:
            user.posts.append(post)

# ✅ O(n)
posts_by_user = {}
for post in posts:
    posts_by_user.setdefault(post.user_id, []).append(post)
for user in users:
    user.posts = posts_by_user.get(user.id, [])
```

### Linear Search in Loop
**Problem:** O(n×m) when O(n) possible
**Detection:** `in` operator or linear search inside loop

```python
# ❌ O(n×m)
for item in list1:
    if item in list2:  # list2 searched linearly each time

# ✅ O(n+m)
set2 = set(list2)
for item in list1:
    if item in set2:  # O(1) lookup
```

### Repeated Expensive Calculations
**Problem:** Computing same value multiple times
```python
# ❌ Recalculating
for item in items:
    if item.value > calculate_threshold():  # Called N times

# ✅ Calculate once
threshold = calculate_threshold()
for item in items:
    if item.value > threshold:
```

## Database Anti-Patterns

### N+1 Query Problem
**Problem:** Query in loop generates 1+N database calls
**Impact:** 100 items = 101 queries instead of 1-2

```python
# ❌ N+1 queries
users = User.query.all()  # 1 query
for user in users:
    posts = Post.query.filter_by(user_id=user.id).all()  # N queries

# ✅ 2 queries (or 1 with JOIN)
users = User.query.options(joinedload(User.posts)).all()
# OR
users = User.query.all()
posts = Post.query.filter(Post.user_id.in_([u.id for u in users])).all()
```

### SELECT * Anti-Pattern
**Problem:** Fetching unnecessary columns
```python
# ❌ Fetching all columns
users = User.query.all()  # Gets all 50 columns

# ✅ Select only needed
users = User.query.with_entities(User.id, User.name).all()
```

### Missing Pagination
**Problem:** Loading entire table into memory
```python
# ❌ Load everything
all_users = User.query.all()  # 1M records in memory

# ✅ Paginate
users = User.query.paginate(page=1, per_page=100)
```

### Missing Indexes
**Detection:** Queries on columns without indexes
**Impact:** Full table scan vs indexed lookup

## Memory Anti-Patterns

### Loading Large Files Entirely
```python
# ❌ Load entire file
with open('large_file.txt') as f:
    data = f.read()  # 1GB file = 1GB RAM

# ✅ Stream/iterate
with open('large_file.txt') as f:
    for line in f:  # ~4KB at a time
        process(line)
```

### String Concatenation in Loop
**Problem:** O(n²) due to string immutability
```python
# ❌ O(n²)
result = ""
for item in items:
    result += str(item)  # Creates new string each time

# ✅ O(n)
result = "".join(str(item) for item in items)
```

### Unnecessary Deep Copies
```python
# ❌ Copying when not needed
import copy
data_copy = copy.deepcopy(large_data)  # Expensive

# ✅ Reference if not modifying
data_ref = large_data  # Or shallow copy if needed
```

## I/O Anti-Patterns

### Synchronous I/O in Hot Path
```python
# ❌ Blocking I/O
for url in urls:
    response = requests.get(url)  # Waits for each

# ✅ Async I/O
async with aiohttp.ClientSession() as session:
    tasks = [fetch(session, url) for url in urls]
    responses = await asyncio.gather(*tasks)
```

### No Buffering
```python
# ❌ Unbuffered I/O
for byte in file.read(1):  # Read 1 byte at a time
    process(byte)

# ✅ Buffered
for chunk in iter(lambda: file.read(8192), b''):
    process(chunk)
```

### Excessive Logging
```python
# ❌ Logging in tight loop
for item in millions_of_items:
    logger.debug(f"Processing {item}")  # I/O on each iteration

# ✅ Batch or conditional logging
if len(items) % 1000 == 0:
    logger.debug(f"Processed {len(items)} items")
```

## Caching Anti-Patterns

### No Caching of Expensive Operations
```python
# ❌ No caching
def get_user_permissions(user_id):
    # Expensive: queries multiple tables
    return calculate_permissions(user_id)

# ✅ With caching
@cache.memoize(timeout=300)
def get_user_permissions(user_id):
    return calculate_permissions(user_id)
```

### Caching Volatile Data
**Problem:** Caching data that changes frequently
**Solution:** Only cache stable, expensive-to-compute data

## Data Structure Anti-Patterns

### Wrong Structure for Access Pattern
```python
# ❌ Using list for lookups
users_list = [user1, user2, ...]
if target_id in [u.id for u in users_list]:  # O(n)

# ✅ Using dict for lookups
users_dict = {u.id: u for u in users}
if target_id in users_dict:  # O(1)
```

### List Instead of Set for Membership
```python
# ❌ List membership check
tags_list = ['python', 'javascript', 'go']
if 'rust' in tags_list:  # O(n)

# ✅ Set membership check
tags_set = {'python', 'javascript', 'go'}
if 'rust' in tags_set:  # O(1)
```

## Severity Guidelines

**Critical (>100x impact):**
- N+1 queries with large datasets (100+ records)
- O(n²) or worse in hot code paths
- Memory leaks in long-running services

**High (10-100x impact):**
- Nested loops over moderate datasets (100-1000 items)
- Missing database indexes on frequent queries
- Loading large files into memory
- Synchronous I/O in request handlers

**Medium (2-10x impact):**
- Repeated calculations in loops
- Inefficient string operations
- Suboptimal data structure choice
- Missing simple caching opportunities

**Low (<2x impact):**
- Minor inefficiencies in cold paths
- Premature optimization candidates

## Detection Metrics

**Cyclomatic Complexity as Proxy:**
- High complexity often correlates with nested loops
- Threshold: >10 warrants performance review

**Database Query Patterns:**
- Queries inside loops = likely N+1 problem
- COUNT queries in loops = definitely N+1

**Memory Patterns:**
- `.read()` without size parameter = risk
- Growing lists in loops = potential memory issue

## Impact Estimation

Provide estimated speedup:
- **N+1 fix:** N queries → 1 query = Nx faster
- **O(n²) → O(n):** For n=1000, 1M → 1K ops = 1000x faster
- **Indexing:** Table scan → Index lookup = 100-10000x faster
- **Caching:** Recomputation → cached = query_time/lookup_time

## References

- Big O Cheat Sheet: https://www.bigocheatsheet.com/
- Database Performance: https://use-the-index-luke.com/
