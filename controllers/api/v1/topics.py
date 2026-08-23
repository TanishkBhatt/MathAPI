from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from asyncio import gather
from collections import Counter
from typing import List, Dict, Any
from utils.database import get_documents
from utils.helpers import validate_api_key

async def get_topics(
        database: AsyncIOMotorClient,
        api_key: str | None
    ) -> Dict[str, Any]:

    await validate_api_key(database, api_key)

    # RETRIEVING ALL TOPICS + ALL METADATA COLLECTIONS IN A SINGLE PARALLEL BATCH
    try:
        topics, formulae_data, sources_data, examples_data, questions_data = await gather(
            get_documents(database, "datasets", "topics"),
            get_documents(database, "datasets", "formulae"),
            get_documents(database, "datasets", "sources"),
            get_documents(database, "datasets", "examples"),
            get_documents(database, "datasets", "questions")
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{str(e)}"
        )

    # BUILDING topic_id -> COUNT MAPS (FIRST DOC WINS, MATCHING OLD [0] SEMANTICS)
    sources_counts: Dict[str, int] = {}
    for doc in sources_data:
        sources_counts.setdefault(doc["topic_id"], len(doc.get("learning_sources", [])))

    formulae_counts: Dict[str, int] = {}
    for doc in formulae_data:
        formulae_counts.setdefault(doc["topic_id"], len(doc.get("formulae", [])))

    example_counts = Counter(doc["topic_id"] for doc in examples_data)
    question_counts = Counter(doc["topic_id"] for doc in questions_data)

    # ATTACHING RESOURCE COUNTS VIA PURE LOOKUPS - NO I/O IN THE LOOP
    for topic in topics:
        topic_id = topic["topic_id"]
        topic["learning_sources_available"] = sources_counts.get(topic_id, 0)
        topic["formulae_available"] = formulae_counts.get(topic_id, 0)
        topic["examples_available"] = example_counts.get(topic_id, 0)
        topic["questions_available"] = question_counts.get(topic_id, 0)

    # RETURN OBJECT
    return {
        "success": True,
        "message": "Data Successfully Retrieved",
        "total_topics": len(topics),
        "topics": topics
    }
