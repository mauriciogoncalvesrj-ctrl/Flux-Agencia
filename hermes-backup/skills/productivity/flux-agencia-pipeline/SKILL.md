---
name: flux-agencia-pipeline
category: productivity
description: Pipeline automatizado da Agência Flux — gera conteúdo semanal, anúncios e estratégia de tráfego para clínicas de estética a partir de dados do cliente.
triggers:
  - pipeline flux
  - gerar conteúdo semanal
  - criar campanha
  - pipeline de conteúdo
  - fluxo de anúncios
related_skills:
  - flux-agencia-conteudo
  - flux-agencia-copywriting
  - flux-agencia-trafego
  - flux-agencia-crm
  - flux-agencia-estrategia
---

# 🏭 Pipeline Automatizado da Agência Flux

> Sistema de produção em linha de montagem: você define o cliente, o sistema gera tudo.

## Como Usar

Quando o usuário acionar esta skill, execute o fluxo completo abaixo para o cliente especificado.

Se o usuário não especificar um cliente, pergunte:
1. Nome da clínica
2. Cidade
3. Tratamentoprincipal
4. Objetivo (awareness / conversão / agendamento)

---

## Fluxo de Produção Semanal

### Etapa 1: Briefing do Cliente

 Colete ou confirme:

- **Clínica**: nome, cidade, diferenciais
- **Tratamento**: procedimento principal para a semana
- **Público**: mulheres 25-55, classe A/B (padrão, ajustar se necessário)
- **Objetivo da semana**: awareness / conversão / agendamento
- **Canais**: Instagram + Meta Ads (+ Google Ads se relevante)
- **Orçamento de mídia**: R$ informados ou sugerir R$1.500-3.000

Se o usuário já forneceu algum dado, NÃO pergunte de novo — use o que já tem.

### Etapa 2: Conteúdo Orgânico (7 dias)

Use a skill `flux-agencia-conteudo` para gerar:

**Formato de saída — Calendário Editorial:**

```
📊 SEMANA {data_inicio} a {data_fim}
🎯 Objetivo: { awareness | conversão | agendamento }
💊 Tratamento: {tratamento}

SEG — 📝 Post Carrossel (Educação)
  Pilar: Educação
  Tema: {tema}
  Título: "{headline}"
  Slides: 5 cards (gerar SVGs)
  Legenda: {legenda completa}
  Hashtags: #estética #{cidade} #beleza #{tratamento}

TER — 🎬 Reels (Prova Social)
  Pilar: Prova Social
  Formato: Antes & Depois ou Depoimento
  Roteiro: {roteiro completo}
  Legenda: {legenda}
  Hashtags: 3-5 relevantes

QUA — 📝 Post Único (Autoridade)
  Pilar: Autoridade
  Tema: {tema}
  Copy: {texto completo}
  Sugestão visual: {descrição}

QUI — 🎬 Reels (Educação)
  Pilar: Educação
  Formato: Tutorial ou Myth-busting
  Roteiro: {roteiro completo}

SEX — 📝 Post Carrossel (Venda Sutil 10%)
  Pilar: Venda Sutil
  Tema: {tema}
  Slides: 5 cards (gerar SVGs)
  CTA:_agendar avaliação

SÁB — 📱 Stories (Prova Social + Urgência)
  3-5 stories: bastidores, resultado, URGENTE agende

DOM — 📱 Stories (Educação + Autoridade)
  3-5 stories: dica, myth-busting, conveniência
```

### Etapa 3: Anúncios (Meta Ads)

Use a skill `flux-agencia-copywriting` para gerar:

**Para cada etapa do funil, gerar:**

```
🔥 CAMPANHA: {nome_campanha}
📊 Etapa: {Aquisição | Conversão | Remarketing}
🎯 Público: {descrição}
💰 Orçamento: R${valor}/dia

📝 COPY 1 — Framework {PAS | AIDA | StorySelling}
Headline: "{headline}"
Texto Primário: "{copy_completa}"
CTA: Agendar Avaliação | Saiba Mais | Enviar Mensagem

📝 COPY 2 — Framework {PAS | AIDA | StorySelling}
Headline: "{headline}"
Texto Primário: "{copy_completa}"
CTA: Agendar Avaliação

📝 COPY 3 — Variação {Remarketing | Urgência}
Headline: "{headline}"
Texto Primário: "{copy_completa}"
CTA: Enviar Mensagem

🎨 SUGESTÃO DE CRIATIVO:
- Tipo: Imagem estática | Carrossel | Vídeo
- Descrição: {descrição detalhada}
- Texto na imagem: "{texto_curto}"
- Formato: 1080x1080 | 1080x1920
```

### Etapa 4: Estratégia de Tráfego

Use a skill `flux-agencia-trafego` para gerar:

```
📈 ESTRATÉGIA DE TRÁFEGO — {nome_clínica}

🎯 OBJETIVO: {objetivo}
💰 ORÇAMENTO TOTAL: R${valor}/mês

DISTRIBUIÇÃO:
- Aquisição: 50% → R${valor}/dia
- Conversão: 30% → R${valor}/dia
- Remarketing: 15% → R${valor}/dia
- Reativação: 5% → R${valor}/dia

PÚBLICOS:
Aquisição: {descrição detalhada}
Conversão: {descrição}
Remarketing: {descrição}
Reativação: {descrição}

KPIs META:
- CPL: R$15-25 (inicial) → R$8-15 (otimizado)
- CTR: >2%
- Taxa de Conversão: >5%
- CAC: R$150-300

CHECKLIST DE LANÇAMENTO:
[ ] Pixel instalado
[ ] Página de destino configurada
[ ] Criativos aprovados
[ ] Orçamento configurado
[ ] Público definido
[ ] Copy revisada
[ ] Extension de WhatsApp configurada
[ ] Automação de GHL ativa
```

### Etapa 5: Configuração CRM (se solicitado)

Use a skill `flux-agencia-crm` para gerar a configuração GoHighLevel correspondente:

- Tags necessárias para a campanha
- Automação de follow-up para leads da campanha
- Template de WhatsApp para resposta rápida

---

## Integração com Meta Ads MCP

Quando os MCP servers `meta-ads` e `ghl` estiverem configurados no Hermes, o pipeline pode operar end-to-end:

- **Meta Ads MCP** (29 ferramentas): criar campanhas, conjuntos, anúncios, criativos, upload de imagens, insights de performance, segmentação por interesse/demografia/localização, orçamento
- **GHL MCP** (163+ ferramentas): criar contatos, atualizar pipeline, tags, automações
- **n8n MCP** (1618+ stars): orquestrar workflows visuais (publicação, webhooks, aprovações)

Para ativar, configure as variáveis de ambiente no `/opt/data/.env`:
- `META_ACCESS_TOKEN` e `META_AD_ACCOUNT_ID` (ou Pipeboard token)
- `GHL_API_KEY`
- `N8N_API_URL` e `N8N_API_KEY`

Veja `skills/mcp/native-mcp/references/meta-ads-mcp.md` para detalhes de setup e segurança.

## Regras do Pipeline

1. **Nunca invente dados** — se não tiver informação, pergunte
2. **Linguagem sempre em português BR** — como a cliente fala
3. **Foco em transformação, não em procedimento** — a cliente compra autoestima
4. **CTA único e claro** em cada peça
5. **Disclaimers** quando necessário (resultados variam, etc.)
6. **Sempre priorizar** clareza sobre criatividade vazia
7. **Gerar variações** — nunca entregar só 1 opção de copy
8. **Formato Telegram** — sem tabelas pipe, usar listas e key:value

## Saída Final

Entregue tudo em **uma mensagem estruturada** com seções claras:

1. 📊 **Conteúdo Semanal** — calendário completo
2. 🔥 **Anúncios** — 3 cópias por etapa do funil
3. 📈 **Estratégia de Tráfego** — orçamento, públicos, KPIs
4. ⚙️ **Configuração CRM** (se aplicável) — tags, automação, templates

O usuário revisa, aprova e publica. Sem improvisação.

## MCP Integration (Campaign Management)

When MCP servers are connected (meta-ads, GHL, n8n), the pipeline can go beyond content generation into **full campaign execution**:

- **meta-ads MCP**: Create campaigns, ad sets, ads, creatives, upload images, get insights, manage budgets — all via chat
- **GHL MCP**: Create contacts, update pipelines, trigger automations, manage follow-up
- **n8n MCP**: Orchestrate multi-step workflows (generate → approve → publish → track)

**Setup status**: MCP servers configured in `/opt/data/config.yaml` but inactive until API keys are provided. See `references/meta-ads-mcp-reference.md` for setup instructions.

**Pitfall**: Meta Ads MCP has security audit score 0/100 (Issue #69 — 167 findings across 35 tools). Critical: data exfiltration paths, injection bypass in `create_ad_creative`/`get_insights`, credential exposure in 13 tools. Use **local mode** (not remote Pipeboard) for production. Campaign data is low-sensitivity but tokens should be rotated regularly. Never store tokens in prompts or logs.

**Pitfall**: Do NOT install Ruflo (ruvnet/ruflo ⭐47K) as a full platform — it duplicates Hermes functionality (delegate_task, cron, skills, memory, MCP) and would add 100+ agents + 32 plugins to an already-loaded VPS. The useful parts (SONA self-learning, AgentDB HNSW, swarm coordination) can be added as MCP server (`npx -y ruflo mcp start`) if needed later, but current bottleneck is API tokens, not orchestration capacity.

**Pitfall**: OpenClaw's `ollama` provider is redundant when `opencode-go` uses the same baseUrl. The `ollama/` prefix causes 404 HTML error pages. Always disable `ollama` plugin and use `opencode-go/*` model IDs exclusively.

**Pitfall**: OpenClaw Telegram/WhatsApp plugins require native dependencies not in the container. Enabling them via WebUI will crash the gateway (SIGTERM). Never attempt to activate them.

## References

- `references/automation-tools-and-mcp.md` — MCP servers (meta-ads, GHL, n8n), image/video generation tools, auto-posting services, and integration priority roadmap
- `references/meta-ads-mcp-reference.md` — Meta Ads MCP: 29 tools, setup options (local vs remote), security audit findings, Meta Developer App setup guide