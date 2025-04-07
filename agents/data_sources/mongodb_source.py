from typing import Dict, Any, List, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from loguru import logger
import json
from datetime import datetime
import hashlib
from cachetools import TTLCache
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDBDataSource:
    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string or os.getenv("MONGODB_URI")
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.cache = TTLCache(maxsize=1000, ttl=300)  # 5-minute cache
        self.schema_validators = {}
        self.connected = False

    async def connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
            if not self.connection_string:
                raise ValueError("MongoDB connection string not provided")
            
            self.client = MongoClient(self.connection_string)
            self.db = self.client.get_database()
            self.connected = True
            logger.info("Successfully connected to MongoDB")
            
            # Initialize schema validators
            self._initialize_schema_validators()
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    def _initialize_schema_validators(self) -> None:
        """Initialize schema validators for different collections."""
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

    def _validate_data(self, collection: str, data: Dict[str, Any]) -> bool:
        """Validate data against schema."""
        if collection not in self.schema_validators:
            logger.warning(f"No schema validator found for collection: {collection}")
            return True

        validator = self.schema_validators[collection]
        # Basic validation - in production, use a proper JSON schema validator
        for required_field in validator.get("required", []):
            if required_field not in data:
                logger.error(f"Missing required field: {required_field}")
                return False

        return True

    def _get_cache_key(self, collection: str, query: Dict[str, Any]) -> str:
        """Generate cache key for query."""
        query_str = json.dumps(query, sort_keys=True)
        return f"{collection}:{hashlib.md5(query_str.encode()).hexdigest()}"

    async def query(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query data from MongoDB with caching."""
        if not self.connected:
            raise ConnectionError("Not connected to MongoDB")

        try:
            # Check cache first
            cache_key = self._get_cache_key(collection, query)
            if cache_key in self.cache:
                logger.debug(f"Cache hit for query: {query}")
                return self.cache[cache_key]

            # Execute query
            coll: Collection = self.db[collection]
            results = list(coll.find(query))
            
            # Store in cache
            self.cache[cache_key] = results
            return results

        except Exception as e:
            logger.error(f"Error querying MongoDB: {str(e)}")
            raise

    async def insert(self, collection: str, data: Dict[str, Any]) -> str:
        """Insert data into MongoDB with validation."""
        if not self.connected:
            raise ConnectionError("Not connected to MongoDB")

        try:
            # Validate data
            if not self._validate_data(collection, data):
                raise ValueError("Data validation failed")

            # Add timestamps
            now = datetime.utcnow().isoformat()
            data["created_at"] = now
            data["updated_at"] = now

            # Insert data
            coll: Collection = self.db[collection]
            result = coll.insert_one(data)
            
            # Invalidate cache
            self.cache.clear()
            
            return str(result.inserted_id)

        except Exception as e:
            logger.error(f"Error inserting into MongoDB: {str(e)}")
            raise

    async def update(self, collection: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """Update data in MongoDB."""
        if not self.connected:
            raise ConnectionError("Not connected to MongoDB")

        try:
            # Add updated_at timestamp
            update_data["updated_at"] = datetime.utcnow().isoformat()

            # Update data
            coll: Collection = self.db[collection]
            result = coll.update_many(query, {"$set": update_data})
            
            # Invalidate cache
            self.cache.clear()
            
            return result.modified_count

        except Exception as e:
            logger.error(f"Error updating MongoDB: {str(e)}")
            raise

    async def delete(self, collection: str, query: Dict[str, Any]) -> int:
        """Delete data from MongoDB."""
        if not self.connected:
            raise ConnectionError("Not connected to MongoDB")

        try:
            coll: Collection = self.db[collection]
            result = coll.delete_many(query)
            
            # Invalidate cache
            self.cache.clear()
            
            return result.deleted_count

        except Exception as e:
            logger.error(f"Error deleting from MongoDB: {str(e)}")
            raise

    async def close(self) -> None:
        """Close MongoDB connection."""
        try:
            if self.client:
                self.client.close()
                self.connected = False
                logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {str(e)}")
            raise 