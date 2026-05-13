# Decomposition Playbook — Exemplos Reais

Este arquivo contém exemplos concretos de como o orquestrador decompõe requests do Mauricio em subtasks para especialistas.

---

## Exemplo 1: Criativo Completo

**Request do Mauricio:**
> "Cria um carrossel de 5 slides sobre harmonização facial pra Taciana, foco em rejuvenescimento sem cirurgia"

**Classificação:**
- Cliente: Taciana
- Domínios: Criativo (carrossel) + Pesquisa (concorrência) + Ads (auditoria)
- Paralelizável: ✅ (3 subtasks independentes)

**Decomposição:**

```python
delegate_task(tasks=[
  {
    goal: "Pesquisar concorrentes de harmonização facial e tendências de rejuvenescimento não-cirúrgico",
    context: """
      Cliente: Taciana (clínica de estética no Rio de Janeiro)
      Voz da marca: [conteúdo de contexts/taciana.md]
      
      Objetivo: Identificar 3-5 concorrentes diretos que anunciam harmonização facial.
      Para cada um: headlines usadas, diferenciais, faixa de preço, fraquezas visíveis.
      Extrair também 3 tendências atuais em rejuvenescimento não-cirúrgico.
      
      Output: Tabela com concorrentes + tendências + ângulo de ataque sugerido.
    """,
    toolsets: ["web", "browser", "search", "file"]
  },
  {
    goal: "Criar estrutura de carrossel 5 slides + copy persuasiva PT-BR sobre harmonização facial para Taciana",
    context: """
      Cliente: Taciana
      Serviço: Harmonização Facial com foco em rejuvenescimento sem cirurgia
      Voz da marca: [conteúdo de contexts/taciana.md]
      Público: Mulheres 35-55, classe A/B, Rio de Janeiro
      
      Skill instructions: [conteúdo de flux-copy-estetica/SKILL.md]
      
      Estrutura esperada:
      Slide 1: Gancho (problema/dor)
      Slide 2: Agitação (por que métodos tradicionais falham)
      Slide 3: Solução (harmonização facial Taciana)
      Slide 4: Prova social + diferenciais
      Slide 5: CTA + urgência
      
      Output: Para cada slide: headline, corpo do texto (máx 150 chars), CTA, sugestão visual.
    """,
    toolsets: ["file"]
  },
  {
    goal: "Auditar campanhas ativas da Taciana no Meta Ads",
    context: """
      Cliente: Taciana
      Meta Ads account: act_911737697183748
      Account ID: TLERdShLsQMxv59zM9Yw
      
      Verificar: campanhas ativas, gasto diário, CTR, conversões.
      Identificar: canibalização entre campanhas, oportunidades de otimização.
      
      Output: status das campanhas + recomendações.
    """,
    toolsets: ["file"]
  }
])
```

**Síntese do Orquestrador (após coletar outputs):**

```
## Síntese Estratégica — Carrossel Harmonização Facial para Taciana

### Insights Cruzados
- Concorrentes estão focando em PREÇO (a partir de R$X) — Taciana pode contra-atacar com TECNOLOGIA
- Campanha atual da Taciana ["Nome"] tem CTR 0.8% — novo criativo deve mirar >1.5%
- Tendência: "baby botox" e "harmonização natural" estão em alta

### Recomendação
Ângulo: "Rejuvenescimento Natural com Tecnologia Avançada" (não competir por preço)

### Entregáveis
[Carrossel completo com 5 slides + copy + sugestões visuais]
[Relatório de auditoria de campanhas ativas]
```

---

## Exemplo 2: Relatório Semanal

**Request:**
> "Relatório semanal da Alpha — como estão os anúncios, leads e pipeline?"

**Classificação:**
- Cliente: Alpha
- Domínios: Ads + CRM + Concorrência (opcional)
- Paralelizável: ✅

**Decomposição:**

```python
delegate_task(tasks=[
  {
    goal: "Gerar relatório de performance Meta Ads da Alpha (últimos 7 dias)",
    context: """
      Cliente: Alpha
      Meta Ads: act_912031229902602
      
      Coletar: impressões, cliques, CTR, CPC, conversões, gasto total.
      
      Skill: [instruções de flux-meta-ads-relatorio]
      Output: tabela de métricas + tendência vs semana anterior.
    """,
    toolsets: ["file"]
  },
  {
    goal: "Analisar pipeline e leads recentes da Alpha no GHL",
    context: """
      Cliente: Alpha
      
      Verificar: novos leads nos últimos 7 dias, status do pipeline, conversões.
      Identificar gargalos: onde os leads estão parando?
      
      Output: funnel de conversão + gargalo principal + recomendação.
    """,
    toolsets: ["file"]
  }
])
```

**Síntese:**
O orquestrador cruza Ads vs Pipeline:
- "Gastamos R$X em ads e geramos Y leads. Taxa de conversão ads→lead: Z%. O gargalo está no follow-up (leads parados há 3+ dias). Recomendação: ativar automação de follow-up no GHL."

---

## Exemplo 3: Landing Page Completa

**Request:**
> "Cria landing page para Botox Premium da Proton"

**Classificação:**
- Cliente: Proton
- Domínios: Criativo (copy + estrutura) + Pesquisa (SEO + concorrência)
- Paralelizável: ✅

**Decomposição:**

```python
delegate_task(tasks=[
  {
    goal: "Pesquisar landing pages de Botox dos concorrentes e keywords SEO para 'botox premium'",
    context: """
      Cliente: Proton
      
      1. Encontrar 3-5 landing pages concorrentes de Botox
      2. Analisar estrutura: seções, headlines, CTAs, prova social
      3. Extrair top 10 keywords SEO para "botox premium" ou "botox [cidade]"
      
      Output: benchmark competitivo + lista de keywords + recomendações de estrutura.
    """,
    toolsets: ["web", "browser", "search"]
  },
  {
    goal: "Escrever copy completa para landing page de Botox Premium da Proton",
    context: """
      Cliente: Proton
      Serviço: Botox Premium
      Voz da marca: [contexts/proton.md]
      
      Estrutura da LP:
      1. Hero section: headline + subheadline + CTA
      2. Problema/Dor
      3. Solução (Botox Premium Proton)
      4. Diferenciais (3-4 bullets)
      5. Prova social (template para depoimentos)
      6. Preço/Oferta
      7. FAQ (5 perguntas)
      8. CTA final + urgência
      
      Output: copy completa PT-BR para cada seção + meta description SEO.
    """,
    toolsets: ["file"]
  }
])
```

---

## Exemplo 4: Pesquisa de Mercado

**Request:**
> "O que está funcionando em anúncios de estética agora? Quero saber tendências pra todas as clínicas."

**Classificação:**
- Cliente: Todos
- Domínios: Pesquisa (web) + Ads (concorrência)
- Paralelizável: ✅ (múltiplos research agents com focos diferentes)

**Decomposição:**

```python
delegate_task(tasks=[
  {
    goal: "Pesquisar tendências de marketing para clínicas de estética em 2026",
    context: """
      Pesquisar: formatos de anúncio que estão performando, tendências de copy,
      novas features do Meta Ads, mudanças no algoritmo.
      
      Fontes: blogs de marketing, Meta Ads blog, Jon Loomer, Social Media Examiner.
      
      Output: top 5 tendências com exemplos e aplicação prática para clínicas.
    """,
    toolsets: ["web", "search"]
  },
  {
    goal: "Analisar biblioteca de anúncios Meta de clínicas de estética concorrentes",
    context: """
      Usar browser para acessar Facebook Ads Library.
      Buscar: harmonização facial, botox, preenchimento, rejuvenescimento.
      Identificar: anúncios ativos há mais de 30 dias (sinal de performance),
      formatos mais usados (imagem vs vídeo vs carrossel), headlines recorrentes.
      
      Output: padrões de criativos que estão performando + exemplos.
    """,
    toolsets: ["web", "browser"]
  }
])
```

---

## Exemplo 5: Tarefa Simples (NÃO Delegar)

**Request:**
> "Qual o saldo da Luana?"

**Classificação:**
- Cliente: Luana
- Domínios: Ads (único)
- Complexidade: Trivial

**Ação: Orquestrador executa direto.**
Sem delegação — uma única chamada MCP `mcp_meta_ads_get_insights` ou script `meta_ads_real_balance.py`.

---

## Exemplo 6: Infra / DevOps

**Request:**
> "O paperclip não está abrindo, consegue ver o que aconteceu?"

**Classificação:**
- Domínio: DevOps (único)
- Complexidade: Média

**Ação: Delegar para DevOps Agent.**

```python
delegate_task(
  goal: "Diagnosticar por que o Paperclip não está respondendo em paperclip.somosflux.com.br",
  context: """
    Paperclip: container paperclip-tjjz-paperclip-1, porta 3100, domínio paperclip.somosflux.com.br
    Servidor: VPS Hostinger, Traefik como reverse proxy
    
    1. Verificar status do container (docker ps)
    2. Verificar logs recentes (docker logs --tail 50)
    3. Testar saúde do serviço (curl localhost:3100/health)
    4. Verificar rota Traefik
    5. Se necessário, reiniciar serviço
    
    Skill: docker-traefik-routing
    
    Output: diagnóstico + ação corretiva aplicada.
  """,
  toolsets: ["terminal", "file"]
)
```

---

## Padrões de Contexto para Sub-Agentes

SEMPRE incluir no `context` de cada sub-agente:

### 1. Contexto do Cliente
```
Cliente: [nome]
Meta Ads account: [act_ID]
Voz da marca: [copiar de contexts/{cliente}.md]
Público: [ICP do contexto]
Diferenciais: [top 3 diferenciais]
```

### 2. Instruções da Skill Relevante
```
Skill instructions: [copiar seções relevantes da SKILL.md]
Output esperado: [formato exato]
```

### 3. Formato de Output Esperado
```
Output: [template específico — tabela, JSON, bullet list, parágrafos]
```

### 4. Constraint Específica
```
PT-BR obrigatório para todo texto visível
Seguir voz da marca — não genérico
Se precisar de dados que não tem, marcar como [CONSULTAR MAURICIO]
```
