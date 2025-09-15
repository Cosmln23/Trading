from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field('', alias='DATABASE_URL')
    pgvector_dim: int = Field(768, alias='PGVECTOR_DIM')

    vertex_project_id: str = Field('', alias='VERTEX_PROJECT_ID')
    vertex_location: str = Field('', alias='VERTEX_LOCATION')
    embed_model: str = Field('', alias='EMBED_MODEL')
    google_application_credentials: str = Field('', alias='GOOGLE_APPLICATION_CREDENTIALS')

    rerank_url: str = Field('', alias='RERANK_URL')
    rerank_api_key: str = Field('', alias='RERANK_API_KEY')

    llm_url: str = Field('', alias='LLM_URL')
    llm_api_key: str = Field('', alias='LLM_API_KEY')
    llm_model: str = Field('', alias='LLM_MODEL')
    llm_temperature: float = Field(0.2, alias='LLM_TEMPERATURE')

    retrieval_k: int = Field(24, alias='RETRIEVAL_K')
    retrieval_n: int = Field(5, alias='RETRIEVAL_N')
    relevance_tau: float = Field(0.20, alias='RELEVANCE_TAU')
    recency_boost: str = Field('news', alias='RECENCY_BOOST')
    context_only: bool = Field(True, alias='CONTEXT_ONLY')

    class Config:
        extra = 'ignore'
        env_file = None

settings = Settings()
