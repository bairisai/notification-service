class HealthService:
    """Provides health information about the application."""
    @staticmethod
    def get_health() -> dict[str, str]:
        return {
            "status": "UP"
            }