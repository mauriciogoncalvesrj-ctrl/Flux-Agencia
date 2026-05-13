# Status Flux — Estado Atual da Operação

> *Last updated: 2026-05-12 20:45 BRT · Mantido por Atlas*

---

## 📊 Visão Geral

| Área | Status | Notas |
|---|---|---|
| **VPS / Infra** | ✅ Operacional | Hostinger 8GB, OpenClaw rodando |
| **Atlas (Agente)** | ✅ Ativo | OpenClaw + Telegram bot |
| **Meta Ads** | ✅ Ativo | Relatórios semanais/mensais no ar |
| **GHL** | ⚠️ Parcial | Location tools com erro 401 |
| **Google Ads** | ❓ Pendente | Credenciais fornecidas, setup não confirmado |
| **Fal.ai** | 🔴 Offline | Saldo zerado |
| **Git Sync** | ✅ Ativo | `mauriciogoncalvesrj-ctrl/Flux-Agencia` |

---

## 👥 Clientes Ativos

| Cliente | Nicho | Status | Meta Ads | GHL | Context Doc |
|---|---|---|---|---|---|
| **Taciana** | Estética | 🟡 Aguardando preenchimento | ❓ | ❓ | Template criado |
| **Luana Sampaio** | Estética (Jundiaí + Cajamar) | 🟢 Ativo | ✅ Split 50/50 | ❓ | Parcial |
| **Proton** | [PREENCHER] | 🟡 Aguardando preenchimento | ❓ | ❓ | Template criado |
| **Alpha** | [PREENCHER] | 🟡 Aguardando preenchimento | ❓ | ❓ | Template criado |

---

## 🤖 Agentes

| Agente | Runtime | Modelo | Status |
|---|---|---|---|
| **Atlas** 🏛️ | OpenClaw (VPS) | kimi-k2.6 (deepseek-v4-pro fallback) | ✅ Ativo |
| **Claude Code** | Local (Windows Mauricio) | Sonnet 4.6 / Opus 4.7 | ✅ Ativo (sob demanda) |
| **Hermes** (legado) | Nous Research (VPS) | deepseek-v4-pro | 🔴 Desligado — backup preservado |

---

## 📅 Entregas Recorrentes

| Entrega | Frequência | Schedule | Responsável | Status |
|---|---|---|---|---|
| Relatório Meta Ads (semanal) | Toda segunda | 12:10 UTC | Atlas | ✅ Ativo |
| Relatório Meta Ads (mensal) | Dia 1 | 12:10 UTC | Atlas | ✅ Ativo |
| Pipeline de conteúdo | Toda segunda | 9:00 UTC | ❓ Atlas/Claude Code | ❓ Confirmar |
| Anúncios | Toda segunda | 9:30 UTC | ❓ Atlas/Claude Code | ❓ Confirmar |
| Template de entrega (dom→seg) | Semanal | Domingo noite | ❓ Atlas | 🔴 Não criado |

---

## 📋 Pendências por Prioridade

### 🔴 Crítico
- [ ] Preencher `product-marketing-context.md` dos 4 clientes (Mauricio)
- [ ] Corrigir GHL Location Token (401)
- [ ] Criar template de entrega semanal (domingo → segunda)

### 🟠 Alto
- [ ] Confirmar cron jobs de conteúdo e anúncios (Claude Code)
- [ ] Preencher `status-flux.md` com dados reais dos clientes (Mauricio)
- [ ] Padronizar skills Flux com template consistente
- [ ] Adicionar "Common Mistakes" nas skills Flux existentes
- [ ] Recarregar FAL_KEY

### 🟡 Médio
- [ ] Instalar skills novas (customer-research, competitor-profiling, directory-submissions)
- [ ] Criar evals/ para skills Flux
- [ ] Adaptar skills Corey Haines para PT-BR e mercado de estética
- [ ] Setup Google Ads MCP

### 🟢 Baixo
- [ ] Migrar memória estável → shared/ (aprovar com Mauricio)
- [ ] Reescrever USER.md em pt-br consolidado
- [ ] Instalar co-marketing, community-marketing, image, video skills

---

## 💰 Comercial Flux

| Plano | Preço | Status |
|---|---|---|
| **Start** | R$ 1.500/mês | Ativo |
| **Conversão** | R$ 2.500/mês | Ativo |
| **Autônomo** (flagship) | R$ 4.500-6.500/mês | Ativo |

**Regras comerciais:**
- Contrato mínimo 6 meses
- Garantia de processo, nunca de resultado (CFM/ANVISA)
- Cliente final NUNCA sabe que é GHL → "Sistema Flux 360"
- Termos internos (GHL, MCP, API) nunca em material de cliente

---

## 🎯 Metas

- **Meta de agência:** R$ 100k/mês
- **Fase atual:** Estruturação operacional (transição solopreneur → operação escalável)
- **Próximo marco:** 4 clientes no Autônomo com operação padronizada

---

> **Instrução para Mauricio:** Revisar e preencher campos marcados com ❓ ou [PREENCHER]. Este documento deve refletir o estado REAL da operação.
