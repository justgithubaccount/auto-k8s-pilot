from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Core
    DEFAULT_NAMESPACE: str = "default"
    ALLOW_MUTATING: bool = False
    KUBECONFIG: Optional[str] = None
    KUBECTL_TIMEOUT: int = 20

    # ArgoCD
    ARGOCD_BASE_URL: Optional[str] = None
    ARGOCD_API_TOKEN: Optional[str] = None

    # Loki
    LOKI_URL: str = "http://loki:3100"

    # GitHub
    GITHUB_TOKEN: Optional[str] = None

    # Cloudflare
    CLOUDFLARE_API_TOKEN: Optional[str] = None
    CLOUDFLARE_ZONE_ID: Optional[str] = None

    # OpenRouter (LLM Gateway)
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_SITE_URL: Optional[str] = None  # optional Referer
    OPENROUTER_APP_NAME: Optional[str] = None  # optional X-Title

    # MCP Kubernetes server
    MCP_K8S_SERVER_URL: Optional[str] = None   # ws:// or wss:// if applicable
    MCP_K8S_API_KEY: Optional[str] = None
    MCP_K8S_INSECURE: bool = False
    MCP_K8S_CMD: Optional[str] = None          # optional: stdio command (e.g., "mcp-server-kubernetes")

    class Config:
        env_file = ".env"
        case_sensitive = False


SETTINGS = Settings()

