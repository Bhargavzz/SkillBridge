from core.config import settings
from core.database import get_db_session  # noqa: F401  re-exported for router Depends()


def get_llm_client():
    from langchain_groq import ChatGroq
    return ChatGroq(
        model="llama3-70b-8192",
        api_key=settings.groq_api_key,
        temperature=0,
    )
