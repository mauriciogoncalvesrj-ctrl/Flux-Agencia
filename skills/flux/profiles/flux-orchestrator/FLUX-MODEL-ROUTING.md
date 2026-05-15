# Flux Model Routing Guide

## Mapa de perfis → especialistas de modelo para orquestração

### Status

**Criado:** 2025-05-14  
**Atualizado:** 2026-05-15  
**Total de perfis:** 7 ativos + legados arquivados  
**Arquitetura vigente:** GPT/OpenAI Codex + OpenCode Go, sem Ollama Cloud  
**Smoketest pós-migração:** pendente neste ciclo

---

## Perfis Ativos

| Perfil | Modelo primário | Provider | Fallbacks | Função |
|---|---|---|---|---|
| `flux-orchestrator` | `deepseek-v4-pro` | `opencode-go` | `deepseek-v4-flash` → `qwen3.5-plus` → `kimi-k2.6` | Planejamento, decomposição, coordenação, síntese |
| `flux-devops` | `gpt-5.5` | `openai-codex` | `deepseek-v4-pro` → `deepseek-v4-flash` → `kimi-k2.6` | Código, Hermes, infra, debugging |
| `flux-research` | `deepseek-v4-pro` | `opencode-go` | `deepseek-v4-flash` → `gpt-5.5` | Pesquisa, benchmarks, documentação |
| `flux-creative` | `deepseek-v4-pro` | `opencode-go` | `deepseek-v4-flash` → `gpt-5.5` | Copy, ideação, narrativa, engenharia de prompt |
| `flux-meta-ads` | `deepseek-v4-flash` | `opencode-go` | `deepseek-v4-pro` → `gpt-5.5` | Métricas, funil, diagnóstico de campanhas |
| `flux-vision` | `qwen3.5-plus` | `opencode-go` | `qwen3.6-plus` → `gpt-5.5` | OCR, screenshots, QA visual, análise de referências |
| `flux-compress` | `deepseek-v4-flash` | `opencode-go` | `deepseek-v4-pro` | Compressão, triagem, títulos, resumos rápidos |

---

## Regras de Roteamento para Orquestrador

### 1. Tarefa multi-domínio (padrão Flux)

```text
flux-orchestrator → classifica → decompõe → delega por domínio compatível → sintetiza
```

Quando subtarefas exigirem modelos diferentes, não misturar tudo em um único `delegate_task`; separar por perfil/processo ou etapa.

### 2. Tarefa pura por domínio

```text
DevOps/código        → flux-devops
Pesquisa/documentos  → flux-research
Criativo/copy        → flux-creative
Análise de Ads       → flux-meta-ads
QA visual/OCR        → flux-vision
Compressão/resumo    → flux-compress
```

### 3. Fallback automático

Os perfis definem fallback local. A regra operacional é:

1. DeepSeek Flash para volume/velocidade.
2. DeepSeek Pro para qualidade/análise.
3. GPT/OpenAI Codex para premium/código/alto impacto.
4. `kimi-k2.6` apenas como fallback emergencial single-turn.

---

## Notas Operacionais

### ⚠️ `--profile` no `hermes chat` pode não carregar o config do perfil

**Uso recomendado:**

```bash
hermes profile use flux-compress
hermes chat -q "Diga apenas: OK"
```

### ⚠️ Fallback automático pode ser invisível

Se o modelo configurado não existir no provider, o Hermes pode tentar fallback. Validação obrigatória:

```bash
hermes profile use <perfil>
hermes chat -q "Diga apenas: OK"
# Verificar se o cabeçalho exibe o modelo correto
```

### ⚠️ OpenCode Go e Cloudflare

Para smoke tests diretos no endpoint, usar `curl` com header:

```bash
-H "User-Agent: Hermes-Agent/1.0"
```

Chamadas Python diretas podem receber `403 / 1010`.

---

## Perfis Legados Arquivados

Perfis antigos em `profiles-legacy/` continuam apenas como histórico. Não usar como fonte de roteamento atual.

---

## Comandos Úteis

```bash
# Listar todos os perfis
hermes profile list

# Trocar para um perfil
hermes profile use flux-meta-ads

# Ver detalhes
hermes profile show flux-research

# Iniciar gateway de um perfil
hermes gateway start
```
