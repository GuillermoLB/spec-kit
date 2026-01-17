# Feature: Database Plugin

**Status**: Draft
**Owner**: spec-kit development team
**Last Updated**: 2026-01-17
**Priority**: Medium

## Purpose

Create a comprehensive database plugin providing SQLAlchemy ORM patterns, Alembic migration workflows, schema design best practices, and DynamoDB patterns for serverless applications. This plugin helps developers build robust data layers efficiently.

## Requirements

- [ ] SKILL.md with database patterns and best practices
- [ ] SQLAlchemy model templates with relationships
- [ ] Alembic migration configuration and templates
- [ ] Database connection management patterns
- [ ] Query optimization examples
- [ ] DynamoDB client templates for serverless
- [ ] PostgreSQL and MySQL specific patterns
- [ ] Schema design best practices
- [ ] Integration with install.sh
- [ ] Validation in verify.sh

## User Stories

**As a** backend developer
**I want** SQLAlchemy patterns and templates
**So that** I can build database models quickly and correctly

**As a** DevOps engineer
**I want** migration management patterns
**So that** I can handle schema changes safely across environments

**As a** serverless developer
**I want** DynamoDB patterns
**So that** I can build serverless applications with best practices

## Acceptance Criteria

1. **Given** I install the database plugin
   **When** I check .claude/skills/database/
   **Then** I see SKILL.md and template files

2. **Given** I use SQLAlchemy model templates
   **When** I create models
   **Then** I have relationships, indexes, and constraints properly defined

3. **Given** I use Alembic templates
   **When** I generate migrations
   **Then** migrations are properly structured and reversible

4. **Given** I use DynamoDB templates
   **When** I build serverless APIs
   **Then** I have efficient query patterns and proper indexing

5. **Given** I follow schema design guidance
   **When** I design database schemas
   **Then** schemas are normalized and performant

## Technical Details

### Plugin Structure

```
plugins/database/
├── skill.md                       # Main plugin file
└── templates/
    ├── sqlalchemy/
    │   ├── models.py              # Model examples
    │   ├── database.py            # Connection management
    │   ├── base.py                # Base model class
    │   └── relationships.py       # Relationship patterns
    ├── alembic/
    │   ├── alembic.ini            # Alembic config
    │   ├── env.py                 # Environment setup
    │   └── migration_template.py  # Migration template
    ├── dynamodb/
    │   ├── client.py              # DynamoDB client
    │   ├── models.py              # DynamoDB patterns
    │   └── queries.py             # Query examples
    └── queries/
        ├── optimization.py        # Query optimization
        └── patterns.py            # Common query patterns
```

### SQLAlchemy Templates

**Template: models.py**

```python
"""
SQLAlchemy model examples with relationships and best practices.
"""
from datetime import datetime
from typing import List
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey,
    Text, Enum, Index, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(Base, TimestampMixin):
    """User model with relationships."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    # Relationships
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")

    # Constraints
    __table_args__ = (
        CheckConstraint('length(username) >= 3', name='username_min_length'),
        Index('idx_user_email_active', 'email', 'is_active'),
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


class Post(Base, TimestampMixin):
    """Blog post model."""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary="post_tags", back_populates="posts")

    __table_args__ = (
        Index('idx_post_author_published', 'author_id', 'published'),
    )


class Comment(Base, TimestampMixin):
    """Comment model."""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")


class Tag(Base):
    """Tag model (many-to-many with posts)."""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)

    # Relationships
    posts: Mapped[List["Post"]] = relationship("Post", secondary="post_tags", back_populates="tags")


# Association table for many-to-many relationship
from sqlalchemy import Table

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
```

**Template: database.py**

```python
"""
Database connection and session management.
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
import logging

logger = logging.getLogger(__name__)

class Database:
    """Database connection manager."""

    def __init__(self, database_url: str, echo: bool = False):
        """
        Initialize database connection.

        Args:
            database_url: SQLAlchemy database URL
            echo: Enable SQL query logging
        """
        self.engine = create_engine(
            database_url,
            echo=echo,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600,   # Recycle connections after 1 hour
        )

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

        # Enable foreign key constraints for SQLite
        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            if 'sqlite' in database_url:
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Provide a transactional scope for database operations.

        Yields:
            SQLAlchemy session

        Example:
            with db.get_session() as session:
                user = session.query(User).first()
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            session.close()

    def create_all(self, base):
        """Create all tables."""
        base.metadata.create_all(bind=self.engine)

    def drop_all(self, base):
        """Drop all tables (use with caution!)."""
        base.metadata.drop_all(bind=self.engine)


# Dependency for FastAPI
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions.

    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = Database(DATABASE_URL)
    with db.get_session() as session:
        yield session
```

### Alembic Templates

**Template: alembic.ini**

```ini
[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url = postgresql://user:password@localhost/dbname

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

**Template: migration_template.py**

```python
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade database schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade database schema."""
    ${downgrades if downgrades else "pass"}
```

### DynamoDB Templates

**Template: dynamodb/client.py**

```python
"""
DynamoDB client wrapper with best practices.
"""
import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import Dict, List, Any, Optional
from decimal import Decimal
import json
import logging

logger = logging.getLogger(__name__)

class DynamoDBClient:
    """DynamoDB client with common operations."""

    def __init__(self, table_name: str, region_name: str = "us-east-1"):
        """
        Initialize DynamoDB client.

        Args:
            table_name: Name of DynamoDB table
            region_name: AWS region
        """
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def get_item(self, key: Dict[str, Any]) -> Optional[Dict]:
        """
        Get single item by key.

        Args:
            key: Primary key (e.g., {"id": "123"})

        Returns:
            Item dict or None if not found
        """
        try:
            response = self.table.get_item(Key=key)
            return response.get('Item')
        except Exception as e:
            logger.error(f"Error getting item: {e}")
            raise

    def put_item(self, item: Dict[str, Any]) -> None:
        """
        Put (create or replace) item.

        Args:
            item: Item to store
        """
        try:
            self.table.put_item(Item=item)
        except Exception as e:
            logger.error(f"Error putting item: {e}")
            raise

    def update_item(
        self,
        key: Dict[str, Any],
        updates: Dict[str, Any]
    ) -> Dict:
        """
        Update item attributes.

        Args:
            key: Primary key
            updates: Attributes to update

        Returns:
            Updated item
        """
        update_expr = "SET " + ", ".join([f"#{k} = :{k}" for k in updates.keys()])
        expr_attr_names = {f"#{k}": k for k in updates.keys()}
        expr_attr_values = {f":{k}": v for k, v in updates.items()}

        try:
            response = self.table.update_item(
                Key=key,
                UpdateExpression=update_expr,
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues="ALL_NEW"
            )
            return response['Attributes']
        except Exception as e:
            logger.error(f"Error updating item: {e}")
            raise

    def delete_item(self, key: Dict[str, Any]) -> None:
        """Delete item by key."""
        try:
            self.table.delete_item(Key=key)
        except Exception as e:
            logger.error(f"Error deleting item: {e}")
            raise

    def query_by_partition_key(
        self,
        partition_key_name: str,
        partition_key_value: Any,
        limit: int = 100
    ) -> List[Dict]:
        """
        Query items by partition key.

        Args:
            partition_key_name: Name of partition key attribute
            partition_key_value: Value to query
            limit: Maximum items to return

        Returns:
            List of items
        """
        try:
            response = self.table.query(
                KeyConditionExpression=Key(partition_key_name).eq(partition_key_value),
                Limit=limit
            )
            return response.get('Items', [])
        except Exception as e:
            logger.error(f"Error querying: {e}")
            raise

    def scan_with_filter(
        self,
        filter_attr: str,
        filter_value: Any,
        limit: int = 100
    ) -> List[Dict]:
        """
        Scan table with filter (use sparingly, expensive).

        Args:
            filter_attr: Attribute to filter on
            filter_value: Value to match
            limit: Maximum items

        Returns:
            List of matching items
        """
        try:
            response = self.table.scan(
                FilterExpression=Attr(filter_attr).eq(filter_value),
                Limit=limit
            )
            return response.get('Items', [])
        except Exception as e:
            logger.error(f"Error scanning: {e}")
            raise
```

### Query Optimization Patterns

**Template: queries/optimization.py**

```python
"""Query optimization patterns."""
from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload, joinedload

# N+1 Query Problem - BAD
def get_posts_bad(db: Session):
    """This causes N+1 queries."""
    posts = db.query(Post).all()
    for post in posts:
        print(post.author.name)  # Separate query for each post!

# Solution 1: Eager loading with joinedload (one query with JOIN)
def get_posts_joined(db: Session):
    """Load posts with authors in one query using JOIN."""
    posts = db.query(Post).options(joinedload(Post.author)).all()
    for post in posts:
        print(post.author.name)  # No additional queries

# Solution 2: Eager loading with selectinload (two queries)
def get_posts_select(db: Session):
    """Load posts with authors in two queries."""
    posts = db.query(Post).options(selectinload(Post.author)).all()
    for post in posts:
        print(post.author.name)  # No additional queries

# Pagination
def get_posts_paginated(db: Session, page: int = 1, per_page: int = 20):
    """Efficient pagination."""
    offset = (page - 1) * per_page
    posts = db.query(Post).offset(offset).limit(per_page).all()
    total = db.query(func.count(Post.id)).scalar()
    return {
        "items": posts,
        "total": total,
        "page": page,
        "per_page": per_page
    }

# Efficient counting
def count_active_users(db: Session):
    """Count without loading all records."""
    return db.query(func.count(User.id)).filter(User.is_active == True).scalar()

# Bulk insert
def bulk_insert_users(db: Session, users_data: list):
    """Efficient bulk insert."""
    db.bulk_insert_mappings(User, users_data)
    db.commit()
```

### Security Considerations

- [ ] Parameterized queries (SQLAlchemy handles this)
- [ ] Input validation before database operations
- [ ] Connection pooling limits
- [ ] No database credentials in code
- [ ] Least privilege database users
- [ ] Encrypted connections (SSL/TLS)

## Edge Cases & Error Handling

1. **Edge case**: Database connection lost
   - **Handling**: Connection pool pre-ping, automatic reconnection

2. **Edge case**: Concurrent updates (race conditions)
   - **Handling**: Use optimistic locking or database transactions

3. **Error**: Migration conflicts
   - **Message**: "Alembic conflict: multiple heads detected"
   - **Recovery**: Merge migrations or resolve manually

## Testing Strategy

### Validation Tests

- [ ] Verify SKILL.md has valid YAML frontmatter
- [ ] Verify Python templates are syntactically valid
- [ ] Verify alembic.ini is valid configuration

### Manual Testing

- [ ] Use SQLAlchemy templates in test project
- [ ] Run Alembic migrations
- [ ] Test DynamoDB client with LocalStack
- [ ] Verify query optimization patterns

## Dependencies

- **Blocked by**: documentation-improvements
- **Blocks**: None
- **Related**: examples (can use database patterns)

## Implementation Notes

### Decisions Made

- 2026-01-17 - Support both SQL (SQLAlchemy) and NoSQL (DynamoDB)
- 2026-01-17 - Include migration management (Alembic)
- 2026-01-17 - Show query optimization patterns (common pain point)
- 2026-01-17 - Connection pooling by default

### Integration with install.sh

Add to plugin selection:

```bash
5) Database Plugin - SQLAlchemy, Alembic, DynamoDB patterns
```

Update verify.sh:

```bash
echo "Plugin: database"
check_file "plugins/database/skill.md"
check_file "plugins/database/templates/sqlalchemy/models.py"
check_file "plugins/database/templates/alembic/alembic.ini"
```

## References

- SQLAlchemy: https://docs.sqlalchemy.org/
- Alembic: https://alembic.sqlalchemy.org/
- DynamoDB best practices: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html

---

**Template Version**: 1.0
**Last Updated**: 2026-01-17
