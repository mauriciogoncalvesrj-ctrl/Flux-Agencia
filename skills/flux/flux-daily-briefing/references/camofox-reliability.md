# CamoFox Web Search Reliability Log

## Summary
CamoFox MCP (`mcp_camofox_web_search`) é o método primário de busca para o daily briefing. Apresenta timeouts frequentes (50%+ das buscas) com Google. Bing falha com erro interno.

## Known Failure Patterns (2026-05-12)

| Pattern | Engine | Error | Rate |
|---------|--------|-------|------|
| TIMEOUT após 30s | Google | `CamoFox API request timed out after 30000ms` | ~50% |
| INTERNAL_ERROR | Bing | `url or macro required` | 100% |
| NAVIGATION_FAILED | Bing | `Internal server error` | 100% |

## Working Methods (in order of preference)

1. **CamoFox Google** — tentar com query curta (≤5 palavras). Se falhar 2x, abandonar.
2. **DuckDuckGo curl** — `curl -s "https://html.duckduckgo.com/html/?q=..."`. Funcionou ~0% em 2026-05-12 (bloqueio).
3. **Google curl direto** — NUNCA funciona. Google bloqueia por captcha/403.
4. **browser_navigate** — requer Chrome instalado (`agent-browser install`). Não disponível no ambiente atual.
5. **Conhecimento próprio** — último recurso. Declarar "Sem novidades" se não tiver dados confiáveis.

## Recomendação
Se o padrão de 50%+ de timeouts persistir por 3+ dias consecutivos, considerar migrar busca para API direta (SerpAPI, Brave Search API) em vez de CamoFox browser-based.
