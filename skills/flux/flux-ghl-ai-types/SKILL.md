---
name: flux-ghl-ai-types
description: Guia completo de todos os tipos de IA no GoHighLevel — Conversation AI, Agent Studio, Voice AI, Workflow AI, Brand Voice, Ask AI, e integrações externas. Matriz de decisão para quando usar cada tipo.
version: 1.0.0
---

# Tipos de IA no GoHighLevel — Guia Completo

Guia de referência para todos os agentes de IA disponíveis no ecossistema GHL, suas capacidades, limitações, preços e casos de uso ideais para agências de marketing digital com foco em clínicas de estética e negócios locais.

---

## Arquitetura de IA do GHL (Mapa Mental)

```
                    ┌──────────────────────────────────┐
                    │         BRAND VOICE               │
                    │   (Persona Transversal a TUDO)    │
                    └──────┬───────────────────────────┘
                           │
        ┌──────────────────┼──────────────────────┐
        │                  │                       │
        ▼                  ▼                       ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ CONVERSATION │  │   AGENT      │  │   VOICE AI       │
│     AI       │  │   STUDIO     │  │   AGENTS         │
│  (Chatbot)   │  │ (Multi-Agent)│  │  (Telefonia)     │
└──────┬───────┘  └──────┬───────┘  └────────┬─────────┘
       │                 │                    │
       └────────┬────────┴──────────┬─────────┘
                │                   │
                ▼                   ▼
        ┌──────────────┐  ┌──────────────────┐
        │  WORKFLOW AI │  │    ASK AI        │
        │ (Ações em    │  │ (Assistente      │
        │  Workflows)  │  │  Interno do GHL) │
        └──────────────┘  └──────────────────┘
```

---

## 1. CONVERSATION AI (Chatbot de Texto)

### O que é
Chatbot nativo do GHL que responde conversas de texto automaticamente via IA treinada no conteúdo do negócio.

### Canais suportados
- Web Chat (widget no site)
- SMS
- WhatsApp
- Facebook Messenger
- Instagram DM
- Áudio (responde a mensagens de voz)

### Como funciona
1. Alimentação com URLs (site, FAQ) ou upload de documentos
2. IA treina automaticamente sobre esse conteúdo
3. Responde perguntas baseado nesse conhecimento
4. Pode ser ativada/desativada dinamicamente por workflows

### O que faz bem
- FAQ e suporte nível 1
- Captura de dados iniciais (nome, telefone, email)
- Respostas 24/7 em múltiplos canais
- Fácil de configurar (upload de URLs = pronto)
- Custo incluso no plano (com créditos)

### Limitações
- Sem memória persistente entre conversas
- Respostas literais ao conteúdo treinado (não raciocina)
- Não lida bem com objeções complexas
- Stateless — cada interação é tratada como nova
- Não faz upsell / cross-sell de forma inteligente

### Quando usar
- **Clínicas de estética**: FAQ sobre procedimentos, valores, horários
- **E-commerce**: status de pedido, política de troca
- **Negócios locais**: horário de funcionamento, agendamento simples
- **Primeiro nível de atendimento** antes de passar pra humano

### Preço
- Incluso no GHL com créditos de IA
- Plano AI Employee Unlimited remove limite de créditos

### Na conta Flux
- Configurado como "IA Sofia" — ativado/desativado via workflow
- 2 workflows controlando: "00 - Ativa IA Sofia v3" (published) + "05 - Desativar IA" (published)

---

## 2. AGENT STUDIO (Multi-Agent Builder)

### O que é
Plataforma no-code/low-code com editor visual de nodes e edges para criar agentes de IA sofisticados com lógica condicional, múltiplos agentes especialistas, e integração com APIs externas. É o produto mais avançado de IA do GHL.

### Funcionalidades principais

| Feature | Descrição |
|---------|-----------|
| AI Agent Node | Node principal de IA — toma decisões, responde, classifica |
| Router Tool | AI Router (roteamento por intenção) e Conditional Router (determinístico) |
| Sequential Node | Fluxos lineares com múltiplos passos encadeados |
| Capture Tools | Coleta inputs estruturados do usuário (formulário conversacional) |
| API Call Tool | Chama APIs externas (suporta import cURL) |
| Knowledge Base Tool | Conecta base de conhecimento para FAQ/respostas |
| Generative AI Tools | Gera texto, áudio, imagens e vídeos via IA dentro do agente |
| Multi-Agent System | Orquestra múltiplos agentes especialistas trabalhando juntos |
| Triggers | Inicia agentes por eventos: formulário, tag, mensagem, webhook |
| Chat Emulator | Testa conversas em tempo real durante o desenvolvimento |

### Ciclo de vida
1. **Draft** → constrói e testa no Chat Emulator
2. **Staging** → versão de desenvolvimento
3. **Deploy** → publica como versão imutável em produção
4. **Agent Logs** → monitora, debug, métricas de performance

### O que faz bem
- Automações complexas multicanal
- Orquestração de múltiplos agentes especialistas
- Integração com APIs externas
- Lógica condicional + IA no mesmo fluxo
- Geração de conteúdo (texto/imagem/vídeo) dentro do agente

### Limitações
- Curva de aprendizado alta (editor visual complexo)
- Ainda novo — bugs e limitações na fase inicial
- Comunidade reporta que é melhor pra suporte que vendas complexas
- Requer plano superior

### Quando usar
- **Orquestração complexa**: rotear leads entre agentes especialistas
- **Automação de agência**: múltiplos clientes, múltiplos fluxos
- **Integração com sistemas externos**: puxar dados de API no meio da conversa
- **Geração de assets**: criar imagem de orçamento, gerar PDF, etc. durante o chat

### Preço
- Parte do AI Employee — requer plano específico
- Créditos de IA por uso (ou Unlimited)

### Na conta Flux
- 1 agente ativo: "Novo agente sem título" (criado 27/04/2026 — inexplorado)
- Product ID: `agent_studio`

---

## 3. VOICE AI AGENTS (Agentes de Voz)

### O que é
Agentes de IA que atendem chamadas telefônicas — inbound e outbound. Falam com voz natural (TTS), entendem o que o lead diz (STT), e executam ações programáveis.

### Funcionalidades

| Feature | Descrição |
|---------|-----------|
| Inbound | Atende chamadas que entram no número GHL |
| Outbound | Faz chamadas ativas (confirmação, follow-up) |
| Appointment Booking | Agenda horários em calendários do GHL durante a chamada |
| Custom Actions | Dispara webhooks/APIs externas mid-call |
| Custom Variables | Insere dados dinâmicos do contato no prompt |
| Noise Cancellation | Filtra ruído de fundo |
| Backchanneling | Respostas naturais ("uh-huh", "entendi") pra soar humano |
| Call Transfer | Transfere pra humano quando necessário |
| Multi-idioma | Suporta dezenas de idiomas |
| Working Hours | Só atende em horário configurado |
| Folders | Organiza agentes por pasta |
| Granular Permissions | Controle granular de permissões por agente |

### O que faz bem
- Qualificação telefônica inicial — filtra leads antes de passar pro vendedor
- Confirmação de agendamento — reduz no-show
- Follow-up automático de leads que não responderam texto
- Captura de informação que lead não quis digitar
- Funciona 24/7, nunca perde uma chamada

### Limitações
- Custo por minuto
- Latência perceptível (especialmente em PT-BR)
- Sotaques fortes e ruído de fundo degradam qualidade
- Lida mal com objeções complexas de vendas
- Comunidade reporta que não substitui vendedor humano em vendas consultivas

### Quando usar
- **Confirmação de consulta**: "Sua consulta amanhã às 14h está confirmada?"
- **Pré-qualificação**: "Já fez algum procedimento antes? Tem orçamento em mente?"
- **Follow-up de no-show**: "Vimos que você não compareceu, quer reagendar?"
- **Captura de informações**: dados que lead não deu por texto
- **Tratamento de objeções simples**: preço, horário, localização

### Quando NÃO usar
- Vendas consultivas complexas (ex: fechar contrato de móveis planejados)
- Atendimento que exige empatia profunda (reclamações graves)

### Preço
- Custo por minuto + créditos de IA
- Preços variam por país/operadora

### Na conta Flux
- 1 agente: "My Agent 180" — configurado em INGLÊS, sem ações customizadas
- Prompt genérico de customer support
- **Precisa ser refeito em PT-BR** com prompt focado em vendas/qualificação

---

## 4. WORKFLOW AI (Ações de IA em Workflows)

### O que é
Dentro dos workflows do GHL, existem ações específicas que usam IA para processar dados e tomar decisões automaticamente. Não interage diretamente com leads — é processamento interno.

### Ações de IA disponíveis em workflows

| Ação | O que faz |
|------|-----------|
| AI Chat/Response | Gera resposta contextual baseada em histórico |
| AI Classification | Classifica leads: quente/morno/frio, intenção, perfil |
| AI Summary | Resume conversas longas para humanos |
| AI Sentiment | Analisa sentimento da conversa (positivo/negativo/neutro) |
| External AI Models | Conecta modelos externos (OpenAI, etc.) |

### O que faz bem
- Automação pós-chat sem agente humano
- Classificação e roteamento inteligente de leads
- Resumo automático pra vendedor ler rápido
- Dispara alertas baseado em sentimento

### Limitações
- Não interage diretamente com o lead (é processamento interno)
- Dependente dos créditos de IA

### Quando usar
- **Classificar lead após primeira interação** → manda pro pipeline certo
- **Resumir conversa** → vendedor lê em 10s em vez de 5min
- **Alertar gerente** se sentimento for negativo
- **Gerar resposta sugerida** que humano revisa e envia

### Na conta Flux
- 37 workflows, incluindo "SOFIA IA FLUX - N8N" (v75) — integração custom com N8N
- "[GHL]SOFIA IA FLUX" — versão nativa do mesmo conceito
- Workflows de ativação/desativação de IA operacionais

---

## 5. BRAND VOICE (Sistema de Persona Transversal)

### O que é
Camada de personalidade que define como TODOS os agentes de IA se comunicam. Configurado uma vez, aplicado em Conversation AI, Agent Studio, Voice AI, e Generative AI.

### O que define
- **Tom**: formal, casual, técnico, empático
- **Estilo**: frases curtas vs longas, direto vs elaborado
- **Vocabulário**: termos preferidos, gírias permitidas, palavras proibidas
- **Brand Kit**: assets visuais (logo, cores, fontes) para Generative AI

### Por que importa
- Consistência em todos os canais
- Muda uma vez, aplica em tudo
- API pública disponível (programático)
- Integrado ao Agent Studio (Generation Nodes usam Brand Voice + Brand Kit)

### Preço
- Incluso em todos os planos

---

## 6. ASK AI (Assistente Interno do GHL)

### O que é
Assistente de IA dentro da interface do GHL — ajuda VOCÊ (operador da agência), não os leads.

### Funcionalidades
- **Funnel Creation Agent**: Cria funis via chat ("crie um funil de captura pra clínica de estética")
- **Content Generation**: Gera copy, email, SMS templates
- **Automação**: Sugere workflows baseado em descrição
- Integração com Agent Studio: pode rotear queries do Ask AI para agentes customizados

### Quando usar
- Criar estruturas rapidamente (funnels, emails, templates)
- Brainstorm de automações
- Acelerar setup de novos clientes

---

## 7. PLANOS E PREÇOS (AI Employee)

| Produto | Modelo |
|---------|--------|
| Conversation AI | Créditos de IA (no plano base) |
| Agent Studio | AI Employee (plano específico) |
| Voice AI | AI Employee + custo/minuto |
| Ask AI | Pay-per-use (créditos) |
| Workflow AI | Créditos de IA |
| Brand Voice | Incluso |
| AI Employee Unlimited | Preço fixo, uso ilimitado de todos os anteriores |

### AI Usage Dashboard
- Dashboard centralizado de gastos com IA
- Visão por produto, por location, por período
- Essencial pra agência controlar margem

---

## 8. INTEGRAÇÕES EXTERNAS (Terceiros)

### Closebot
- Foco: qualificação + agendamento
- Integração: webhook + API GHL
- Limitação: stateless, não lembra conversas passadas
- Ideal: high-volume, ticket baixo

### MagicBlocks
- Foco: agente de vendas completo
- Framework HAPPA (Hook → Align → Personalize → Pitch → Action)
- Memória persistente cross-channel
- 97.5% taxa de sucesso reportada
- Ideal: ticket alto, venda consultiva

### ZappyChat
- Sendo adquirido pelo Closebot
- **⚠️ Sunset Janeiro/2026**

### N8N + OpenAI (Custom)
- Stack que a Flux já domina (SOFIA IA FLUX - N8N)
- Máxima flexibilidade, mas requer manutenção
- Ideal para lógicas muito específicas que o nativo não cobre

---

## Matriz de Decisão — Quando usar cada tipo

| Cenário | Melhor IA | Por quê |
|---------|-----------|---------|
| FAQ simples, horários, preços | Conversation AI | Fácil, barato, incluso |
| Roteamento inteligente multicanal | Agent Studio | Router + Multi-Agent |
| Qualificação telefônica inicial | Voice AI | Filtra antes do vendedor |
| Confirmação/redução de no-show | Voice AI | Automático e escala |
| Classificar leads pós-chat | Workflow AI | Processamento interno |
| Venda consultiva complexa | Agent Studio + N8N/OpenAI | Nativo não basta |
| Gerar assets durante chat | Agent Studio (Gen AI) | Imagem, PDF, vídeo |
| Consistência de marca | Brand Voice | Aplica em todos |
| Criar funis rapidamente | Ask AI | Assiste VOCÊ, não o lead |
| Alta complexidade/external APIs | N8N + OpenAI | Flex total |

---

## Oportunidades Imediatas na Flux

O que já existe na conta e não está sendo usado:

1. **Agent Studio** — agente ativo sem configurar. Construir agente de vendas consultivas
2. **Voice AI** — agente em inglês com prompt genérico. Refatorar pra PT-BR com script de qualificação de leads
3. **Conversation AI (Sofia)** — já integrada com workflows. Refinar prompts e base de conhecimento
4. **Brand Voice** — verificar se está configurado para aplicar consistência
