"""
Configuration management using pydantic-settings
Loads environment variables from .env file and provides typed settings
"""

from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConvergenceSettings(BaseSettings):
    """Convergence control settings inspired by industry best practices"""

    enabled: bool = Field(default=True, description="Enable convergence management")
    loop_detection_enabled: bool = Field(
        default=True, description="Enable infinite loop detection"
    )
    watchdog_enabled: bool = Field(default=True, description="Enable watchdog systems")
    consensus_threshold: float = Field(
        default=0.8, ge=0.0, le=1.0, description="Consensus agreement threshold"
    )
    goal_satisfaction_threshold: float = Field(
        default=0.95, ge=0.0, le=1.0, description="Goal satisfaction threshold"
    )

    model_config = SettingsConfigDict(env_prefix="CONVERGENCE_")


class ResourceSettings(BaseSettings):
    """Resource limits and constraints"""

    max_token_budget: int = Field(
        default=1000000, gt=0, description="Maximum tokens per session"
    )
    max_memory_threshold: str = Field(default="8GB", description="Maximum memory usage")
    max_session_timeout: int = Field(
        default=3600, gt=0, description="Maximum session time in seconds"
    )
    max_parallel_agents: int = Field(
        default=5, gt=0, le=20, description="Maximum concurrent agents"
    )
    max_iterations: int = Field(
        default=200, gt=0, description="Maximum iterations per task"
    )
    max_queue_length: int = Field(
        default=100, gt=0, description="Maximum task queue length"
    )

    model_config = SettingsConfigDict(env_prefix="")


class VESettings(BaseSettings):
    """Virtual Environment configuration"""

    timeout: int = Field(default=600, gt=0, description="VE timeout in seconds")
    retry_attempts: int = Field(default=3, gt=0, description="Number of retry attempts")
    load_balancing: str = Field(
        default="round_robin", description="Load balancing strategy"
    )

    @field_validator("load_balancing")
    @classmethod
    def validate_load_balancing(cls, v: str) -> str:
        allowed = ["round_robin", "least_loaded", "random", "weighted"]
        if v not in allowed:
            raise ValueError(f"load_balancing must be one of {allowed}")
        return v

    model_config = SettingsConfigDict(env_prefix="VE_")


class HumanSettings(BaseSettings):
    """Human expert integration settings"""

    escalation_timeout: int = Field(
        default=1800, gt=0, description="Human escalation timeout"
    )
    max_wait_time: int = Field(
        default=3600, gt=0, description="Maximum wait time for human response"
    )
    notification_enabled: bool = Field(
        default=True, description="Enable human notifications"
    )

    model_config = SettingsConfigDict(env_prefix="HUMAN_")


class ExecutionSettings(BaseSettings):
    """Execution strategy configuration"""

    strategy: str = Field(default="hybrid", description="Execution strategy")
    max_tree_depth: int = Field(
        default=10, gt=0, description="Maximum execution tree depth"
    )
    context_sharing_mode: str = Field(
        default="hierarchical", description="Context sharing mode"
    )

    @field_validator("strategy")
    @classmethod
    def validate_strategy(cls, v: str) -> str:
        allowed = ["dfs", "bfs", "hybrid"]
        if v not in allowed:
            raise ValueError(f"strategy must be one of {allowed}")
        return v

    @field_validator("context_sharing_mode")
    @classmethod
    def validate_context_sharing_mode(cls, v: str) -> str:
        allowed = ["hierarchical", "shared", "isolated"]
        if v not in allowed:
            raise ValueError(f"context_sharing_mode must be one of {allowed}")
        return v

    model_config = SettingsConfigDict(env_prefix="EXECUTION_")


class MonitoringSettings(BaseSettings):
    """Monitoring and observability settings"""

    logging_level: str = Field(default="INFO", description="Logging level")
    metrics_enabled: bool = Field(default=True, description="Enable metrics collection")
    dashboard_enabled: bool = Field(
        default=False, description="Enable monitoring dashboard"
    )
    telemetry_endpoint: Optional[str] = Field(
        default=None, description="Telemetry endpoint URL"
    )

    @field_validator("logging_level")
    @classmethod
    def validate_logging_level(cls, v: str) -> str:
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"logging_level must be one of {allowed}")
        return v.upper()

    model_config = SettingsConfigDict(env_prefix="")


class APISettings(BaseSettings):
    """API keys and external service configuration"""

    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(
        default=None, description="Anthropic API key"
    )
    google_api_key: Optional[str] = Field(default=None, description="Google API key")

    model_config = SettingsConfigDict(env_prefix="")


class DatabaseSettings(BaseSettings):
    """Database configuration for future use"""

    url: str = Field(
        default="sqlite:///./project_runtime.db", description="Database URL"
    )
    redis_url: str = Field(default="redis://localhost:6379", description="Redis URL")

    model_config = SettingsConfigDict(env_prefix="DATABASE_")


class Settings(BaseSettings):
    """Main settings class that combines all configuration sections"""

    # Basic project settings
    project_name: str = Field(default="keep-agent-running", description="Project name")
    environment: str = Field(default="development", description="Environment")
    debug: bool = Field(default=True, description="Debug mode")

    # Orchestration
    default_orchestration_model: str = Field(
        default="gpt-4-advanced", description="Default orchestration model"
    )
    available_models: List[str] = Field(
        default=["gpt-4", "claude-3.5-sonnet", "gpt-3.5-turbo"],
        description="Available models",
    )

    # Nested settings
    convergence: ConvergenceSettings = Field(default_factory=ConvergenceSettings)
    resources: ResourceSettings = Field(default_factory=ResourceSettings)
    ve: VESettings = Field(default_factory=VESettings)
    human: HumanSettings = Field(default_factory=HumanSettings)
    execution: ExecutionSettings = Field(default_factory=ExecutionSettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)
    api: APISettings = Field(default_factory=APISettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)

    # Development settings
    reload_on_change: bool = Field(default=True, description="Reload on file changes")
    profiling_enabled: bool = Field(default=False, description="Enable profiling")

    @field_validator("available_models", mode="before")
    @classmethod
    def parse_available_models(cls, v) -> List[str]:
        if isinstance(v, str):
            return [model.strip() for model in v.split(",")]
        return v

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


# Global settings instance
settings = Settings()
