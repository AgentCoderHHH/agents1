from typing import Dict, Any, List, Optional
import asyncpg
from loguru import logger
import json
from datetime import datetime
import hashlib
from cachetools import TTLCache
import os
from dotenv import load_dotenv

load_dotenv()

class PostgreSQLDataSource:
    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string or os.getenv("POSTGRES_URI")
        self.pool: Optional[asyncpg.Pool] = None
        self.cache = TTLCache(maxsize=1000, ttl=300)  # 5-minute cache
        self.schema_validators = {}
        self.connected = False

    async def connect(self) -> None:
        """Establish connection to PostgreSQL."""
        try:
            if not self.connection_string:
                raise ValueError("PostgreSQL connection string not provided")
            
            self.pool = await asyncpg.create_pool(self.connection_string)
            self.connected = True
            logger.info("Successfully connected to PostgreSQL")
            
            # Initialize schema validators
            self._initialize_schema_validators()
            
            # Create tables if they don't exist
            await self._create_tables()
            
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {str(e)}")
            raise

    def _initialize_schema_validators(self) -> None:
        """Initialize schema validators for different tables."""
        self.schema_validators = {
            "goals": {
                "type": "object",
                "required": ["id", "title", "status", "created_at"],
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "status": {"type": "string", "enum": ["pending", "in_progress", "completed", "blocked"]},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"},
                    "due_date": {"type": "string", "format": "date-time"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]}
                }
            },
            "tasks": {
                "type": "object",
                "required": ["id", "title", "status", "goal_id"],
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "status": {"type": "string", "enum": ["pending", "in_progress", "completed", "blocked"]},
                    "goal_id": {"type": "string"},
                    "assignee": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"},
                    "due_date": {"type": "string", "format": "date-time"},
                    "dependencies": {"type": "array", "items": {"type": "string"}}
                }
            },
            "progress": {
                "type": "object",
                "required": ["id", "goal_id", "status", "timestamp"],
                "properties": {
                    "id": {"type": "string"},
                    "goal_id": {"type": "string"},
                    "status": {"type": "string"},
                    "progress": {"type": "number", "minimum": 0, "maximum": 100},
                    "timestamp": {"type": "string", "format": "date-time"},
                    "notes": {"type": "string"}
                }
            }
        }

    async def _create_tables(self) -> None:
        """Create necessary tables if they don't exist."""
        async with self.pool.acquire() as conn:
            # Create goals table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    due_date TIMESTAMP WITH TIME ZONE,
                    priority TEXT
                )
            """)
            
            # Create tasks table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    goal_id TEXT NOT NULL REFERENCES goals(id),
                    assignee TEXT,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
                    due_date TIMESTAMP WITH TIME ZONE,
                    dependencies TEXT[]
                )
            """)
            
            # Create progress table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS progress (
                    id TEXT PRIMARY KEY,
                    goal_id TEXT NOT NULL REFERENCES goals(id),
                    status TEXT NOT NULL,
                    progress NUMERIC(5,2),
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
                    notes TEXT
                )
            """)

    def _validate_data(self, table: str, data: Dict[str, Any]) -> bool:
        """Validate data against schema."""
        if table not in self.schema_validators:
            logger.warning(f"No schema validator found for table: {table}")
            return True

        validator = self.schema_validators[table]
        # Basic validation - in production, use a proper JSON schema validator
        for required_field in validator.get("required", []):
            if required_field not in data:
                logger.error(f"Missing required field: {required_field}")
                return False

        return True

    def _get_cache_key(self, table: str, query: Dict[str, Any]) -> str:
        """Generate cache key for query."""
        query_str = json.dumps(query, sort_keys=True)
        return f"{table}:{hashlib.md5(query_str.encode()).hexdigest()}"

    async def query(self, table: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query data from PostgreSQL with caching."""
        if not self.connected:
            raise ConnectionError("Not connected to PostgreSQL")

        try:
            # Check cache first
            cache_key = self._get_cache_key(table, query)
            if cache_key in self.cache:
                logger.debug(f"Cache hit for query: {query}")
                return self.cache[cache_key]

            # Build SQL query
            conditions = []
            params = []
            for key, value in query.items():
                conditions.append(f"{key} = ${len(params) + 1}")
                params.append(value)

            sql = f"SELECT * FROM {table}"
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            # Execute query
            async with self.pool.acquire() as conn:
                results = await conn.fetch(sql, *params)
                results = [dict(row) for row in results]
            
            # Store in cache
            self.cache[cache_key] = results
            return results

        except Exception as e:
            logger.error(f"Error querying PostgreSQL: {str(e)}")
            raise

    async def insert(self, table: str, data: Dict[str, Any]) -> str:
        """Insert data into PostgreSQL with validation."""
        if not self.connected:
            raise ConnectionError("Not connected to PostgreSQL")

        try:
            # Validate data
            if not self._validate_data(table, data):
                raise ValueError("Data validation failed")

            # Add timestamps
            now = datetime.utcnow()
            data["created_at"] = now
            data["updated_at"] = now

            # Build SQL query
            columns = list(data.keys())
            values = list(data.values())
            placeholders = [f"${i+1}" for i in range(len(values))]
            
            sql = f"""
                INSERT INTO {table} ({', '.join(columns)})
                VALUES ({', '.join(placeholders)})
                RETURNING id
            """

            # Execute query
            async with self.pool.acquire() as conn:
                result = await conn.fetchval(sql, *values)
            
            # Invalidate cache
            self.cache.clear()
            
            return str(result)

        except Exception as e:
            logger.error(f"Error inserting into PostgreSQL: {str(e)}")
            raise

    async def update(self, table: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """Update data in PostgreSQL."""
        if not self.connected:
            raise ConnectionError("Not connected to PostgreSQL")

        try:
            # Add updated_at timestamp
            update_data["updated_at"] = datetime.utcnow()

            # Build SQL query
            set_clause = ", ".join([f"{key} = ${i+1}" for i, key in enumerate(update_data.keys())])
            where_clause = " AND ".join([f"{key} = ${i+len(update_data)+1}" for i, key in enumerate(query.keys())])
            
            sql = f"""
                UPDATE {table}
                SET {set_clause}
                WHERE {where_clause}
            """

            # Execute query
            async with self.pool.acquire() as conn:
                result = await conn.execute(sql, *list(update_data.values()), *list(query.values()))
            
            # Invalidate cache
            self.cache.clear()
            
            return int(result.split()[-1])

        except Exception as e:
            logger.error(f"Error updating PostgreSQL: {str(e)}")
            raise

    async def delete(self, table: str, query: Dict[str, Any]) -> int:
        """Delete data from PostgreSQL."""
        if not self.connected:
            raise ConnectionError("Not connected to PostgreSQL")

        try:
            # Build SQL query
            where_clause = " AND ".join([f"{key} = ${i+1}" for i, key in enumerate(query.keys())])
            sql = f"DELETE FROM {table} WHERE {where_clause}"

            # Execute query
            async with self.pool.acquire() as conn:
                result = await conn.execute(sql, *list(query.values()))
            
            # Invalidate cache
            self.cache.clear()
            
            return int(result.split()[-1])

        except Exception as e:
            logger.error(f"Error deleting from PostgreSQL: {str(e)}")
            raise

    async def close(self) -> None:
        """Close PostgreSQL connection."""
        try:
            if self.pool:
                await self.pool.close()
                self.connected = False
                logger.info("PostgreSQL connection closed")
        except Exception as e:
            logger.error(f"Error closing PostgreSQL connection: {str(e)}")
            raise 