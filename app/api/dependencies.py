from app.services.vector_engine import VectorEngine


def get_vector_engine() -> VectorEngine:
    return VectorEngine.get_instance()
