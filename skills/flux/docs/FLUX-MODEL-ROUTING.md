# Flux Model Routing Guide
## Mapa de perfis → especialistas de modelo para orquestração

### Status
**Criado:** 2025-05-14  
**Atualizado:** 2025-05-14 16:03 BRT  
**Total de perfis:** 7 ativos + 8 legados arquivados  
**Smoketest:** ✅ Todos válidos — 2025-05-14 15:50–16:00

---

## Perfis Ativos (Smoketest Validado)

| Perfil | Modelo | Provider | Toolsets | Máx. Turns | Função | Status |
|--------|--------|----------|----------|-----------|--------|--------|
| `flux-orchestrator` | `kimi-k2.6` | ollama-cloud | web, search, browser, file, delegation, todo, memory, skills, terminal | 30 | Planejamento, decomposição, coordenação, síntese | ✅ |
| `flux-devops` | `glm-5.1` | opencode-go | terminal, file, web, memory, skills | 40 | Configuração Hermes, debugging, scripts, infra | ✅ |
| `flux-research` | `deepseek-v4-flash` | ollama-cloud | web, search, browser, file, memory, skills | 25 | Pesquisa profunda, benchmarks, comparação de ferramentas | ✅ |
| `flux-creative` | `gemma4:31b` | ollama-cloud | image_gen, vision, file, web, memory, skills | 25 | Copy PT-BR, ideação, carrosséis, narrativas | ✅ |
| `flux-meta-ads` | `deepseek-v4-pro` | ollama-cloud | file, web, memory, skills, terminal | 30 | Análise de performance, diagnóstico de campanhas, funil | ✅ |
| `flux-vision` | `qwen3-vl:235b` | ollama-cloud | vision, image_gen, file, memory, skills | 25 | OCR, QA visual, screenshots, dashboards | ✅ |
| `flux-compress` | **`ministral-3:8b`** | ollama-cloud | file, memory, skills | 15 | Compressão, triagem, títulos, resumos | ✅ |

> ⚠️ `qwen3-next:80b` foi substituído por `ministral-3:8b` (modelo não encontrado no Ollama Cloud — retorna `Error: unauthorized` e fallback automático para `kimi-k2.6`).

---

## Regras de Roteamento para Orquestrador

### 1. Tarefa Multi-domínio (padrão Flux)
```
flux-orchestrator → decompõe → envia sub-tarefas para especialistas
→ orquestrador realiza síntese final (não muda de perfil nas subtarefas)
```

### 2. Tarefa Pura por Domínio
```
DevOps puro → flux-devops
Pesquisa rápida → flux-research
Criativo puro → flux-creative
Análise de Ads → flux-meta-ads
QA visual → flux-vision
Compressão/resumo → flux-compress
```

### 3. Fallback Automático
O main `config.yaml` define `fallback_providers` para OpenCode (glm-5.1 → kimi-k2.6).
Perfis individuais herdam esse fallback se o provider primário falhar.

---

## Notas Operacionais

### ⚠️ `--profile` no `hermes chat` NÃO carrega o config do perfil
**Comportamento observado:**
```bash
hermes chat --profile flux-compress   # ❌ Ignora model do perfil → usa default
```

**Uso correto:**
```bash
hermes profile use flux-compress      # Carrega o profile env
hermes chat -q "Diga apenas: OK"    # ✅ Usa o model do perfil
```

### ⚠️ Fallback automático invisível
Se o modelo configurado não existir no provider, o Hermes:
1. Tenta o próximo `fallback_providers` no config
2. Silenciosamente usa `model.default` do config raiz
3. **Não avisa o usuário** — apenas exibe cabeçalho diferente (ex: `⚡ usando kimi-k2.6`)

**Validação obrigatória:**
```bash
hermes profile use <perfil>
hermes chat -q "Diga apenas: OK"
# Verificar se o cabeçalho exibe o modelo correto
```

---

## Perfis Legados Arquivados

**Caminho:** `/opt/data/profiles-legacy/`

| Perfil | Motivo do arquivamento |
|--------|------------------------|
| conteudo-flux | Modelo obsoleto (claude-3-haiku) |
| copy-flux | Modelo obsoleto (claude-3-sonnet) |
| flux-crm | Modelo obsoleto (gpt-4o-mini) |
| flux-estrategista | Modelo obsoleto (deepseek-chat) |
| flux-inteligencia | Modelo obsoleto (deepseek-chat) |
| flux-ops | Modelo obsoleto (gpt-4o-mini) |
| flux-sdr | Modelo obsoleto (deepseek-chat) |
| flux-trafego | Modelo obsoleto (gpt-4o) |

---

## Comandos Úteis

```bash
# Listar todos os perfis
hermes profile list

# Trocar para um perfil (recomendado)
hermes profile use flux-meta-ads

# Ver detalhes
hermes profile show flux-research

# Iniciar gateway de um perfil
hermes gateway start
```