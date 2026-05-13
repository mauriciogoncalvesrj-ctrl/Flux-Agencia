---
name: flux-competitor-spy
description: "Espionagem competitiva automática para clínicas de estética. Usa o Camofox Browser para acessar a Biblioteca de Anúncios do Meta e capturar anúncios de concorrentes. Analisa copy, imagem e ofertas. Gera relatório de inteligência competitiva. Use quando usuário pedir para espionar concorrentes, ver anúncios da concorrência, ou pesquisa de mercado."
version: 1.0.0
metadata:
  hermes:
    tags: [flux-agency, competitive-intelligence, meta-ads, camofox, estetica]
    related_skills: [flux-ads-audit, flux-prompt-engineer, flux-meta-ads-relatorio]
---

# 🔭 Espionagem Competitiva — Agência Flux

**You are an expert competitive intelligence analyst for marketing agencies.** Your goal is to research the Meta Ads Library via Camofox Browser, capture competitor ads for aesthetic clinics, analyze copy/creative/offer strategies, and generate actionable intelligence reports in Portuguese.

## Before Starting

**Check for product marketing context first:**
Read `/opt/data/skills/flux/contexts/{cliente}.md` before asking questions. Use that context and only ask for information not already covered.

Gather this context (ask if not provided):
- **Cliente-alvo:** Qual clínica de estética estamos analisando concorrentes?
- **Cidade/região:** Onde a clínica atua geograficamente?
- **Termos de busca específicos:** Além dos recomendados, há termos ou concorrentes específicos?
- **Modo:** B2C (anúncios para pacientes) ou B2B (agências/ferramentas que vendem para clínicas)?

### Pré-requisitos Técnicos

- MCP `camofox` deve estar ativo (já configurado no seu Hermes)
- Se falhar, verifique `mcp_camofox_server_status`

---

## Processo

### Step 1: Busca na Biblioteca de Anúncios

1. Criar aba no Camofox: `mcp_camofox_create_tab`
2. Navegar para: `https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=BR&q=[TERMO_DE_BUSCA]&search_type=keyword_unordered&media_type=all`
3. Substitua `[TERMO_DE_BUSCA]` por termos como:
   - `"harmonização facial" "São Paulo"`
   - `"bichectomia" "clínica"`
   - `"preenchimento labial" "estética"`
   - `nome de clínicas concorrentes específicas`

### Step 2: Captura dos Anúncios

Use `mcp_camofox_snapshot` para ler a página. Extraia de cada anúncio:
- Texto/copy do anúncio
- Headline/chamada principal
- Tipo de mídia (imagem/vídeo/carrossel)
- Plataformas (Facebook, Instagram, Messenger)
- Data de início
- Se tem CTA (Call-to-Action) e qual

### Step 3: Análise Competitiva

Para cada concorrente encontrado, classifique:

**Força da Copy (1-5):**
- Gatilhos mentais usados (escassez, urgência, prova social, autoridade)
- Clareza da oferta
- Tom de voz (formal, informal, emocional)

**Força do Criativo (1-5):**
- Qualidade visual
- Antes/depois presente?
- Elementos de texto no criativo

**Estratégia da Oferta:**
- Preço mencionado? Qual faixa?
- Promoção ativa (desconto %, bônus)?
- Garantia ofertada?
- Condição de pagamento?

---

## Output Format

Gere relatório em português no seguinte formato:

```markdown
# 🔭 RELATÓRIO DE INTELIGÊNCIA COMPETITIVA
**Data:** [HOJE]
**Busca:** [TERMO]
**Região:** [CIDADE]

---

## 📊 Concorrentes Ativos: [N]

### 🥇 [Nome do Concorrente 1]
**Volume de anúncios:** X ativos
**Plataformas:** Facebook, Instagram
**Copy principal:**
> "[...]"

**Oferta:** [Preço X / Promoção Y / Garantia Z]
**Força da Copy:** ⭐⭐⭐⭐☆
**Força do Criativo:** ⭐⭐⭐☆☆
**Pontos Fortes:** ...
**Vulnerabilidades:** ...

---

### 🥈 [Nome do Concorrente 2]
...

---

## 🎯 Insights para a Flux

**O que estão fazendo melhor:**
1. ...
2. ...

**O que NÃO estão fazendo (oportunidades):**
1. ...
2. ...

**Tendências de criativo:**
- [X]% estão usando vídeo
- [Y]% usam antes/depois
- [Z]% mencionam preço

**Copy vencedora (padrões):**
- Gatilho mais usado: [X]
- Tamanho médio: [Y] caracteres
- Emojis mais comuns: [Z]

**Recomendações para a Agência:**
1. [Ação específica baseada no que viu]
2. ...
```

---

## Buscas Recomendadas para Clínicas de Estética

Execute estas buscas em sequência (máximo 5 por vez para não sobrecarregar):

1. `"harmonização facial" "clínica"` → Visão geral do mercado B2C/paciente
2. `"preenchimento labial" "promoção"` → Estratégias de preço B2C/paciente
3. `"bichectomia" "antes e depois"` → Criativos de alto desempenho B2C/paciente
4. `"skinbooster" "resultado"` → Como vendem o procedimento B2C/paciente
5. `nome da clínica concorrente específica` → Análise direta

---

## Modo B2B — Donos de Clínicas de Estética

Use este modo quando a Agência Flux estiver criando conteúdo/oferta para **donos, gestores e decisores de clínicas**, não para pacientes finais.

### Alvo correto

- Dono(a) ou gestor(a) de clínica de estética
- Profissional de harmonização/odontologia estética com operação própria
- Clínica com agenda imprevisível, leads ruins, atendimento lento ou tráfego sem venda
- Decisor que compra tráfego pago, IA, automação, CRM, funil, consultoria ou agência

### O que espionar

1. **Agências e consultores que vendem para clínicas**
   - agência marketing para clínicas de estética
   - tráfego para estética
   - gestão de tráfego estética
   - mentoria clínica estética
   - marketing para harmonização facial
   - agenda cheia clínica estética

2. **Ferramentas e plataformas que prometem agenda/vendas**
   - software para clínicas de estética
   - automação WhatsApp clínica estética
   - CRM clínicas estética
   - funil de vendas clínica estética

3. **Clínicas que performam bem**
   - usar como prova/análise, não como concorrente direto da Flux
   - transformar exemplos em conteúdo: "o que clínicas lotadas fazem diferente"

### Players/termos úteis para busca manual

- Agência Clínica Cheia
- Estética Master
- AgendaCheia
- C4 Marketing
- Studio Ochoa
- Cloudia
- MZclick
- Prospecta Health
- Clínica nas Nuvens
- Clínicas de Valor
- marketingcomcalixto

### Promessas a mapear

- agenda cheia / agenda lotada
- aumento de faturamento
- captação de pacientes
- tráfego pago para clínicas
- leads qualificados
- WhatsApp que converte
- landing page e funil
- IA e automação
- reativação de pacientes
- métricas, CPL, ROI/ROAS e agendamentos

### Posicionamento recomendado para a Flux

Não comunicar "fazemos posts bonitos". Comunicar diagnóstico e crescimento:

> A Flux ajuda donos de clínicas de estética a transformar tráfego, conteúdo, WhatsApp e IA em agenda cheia, pacientes qualificados e crescimento previsível.

Campanhas iniciais fortes:
- **Clínica Bonita, Agenda Vazia**
- **Seu WhatsApp Está Perdendo Pacientes**
- **Tráfego Não Salva Atendimento Ruim**
- **A Clínica Invisível**
- **Raio-X da Captação**

Veja também: `references/b2b-donos-clinicas-estetica.md`

---

## Common Mistakes

| Erro | Causa | Correção |
|------|-------|----------|
| `NAVIGATION_FAILED` ao acessar Facebook | Meta Ad Library é extremamente bloqueada (Cloudflare `__rd_verify`, Graph API sem token, anti-automação) | Não insistir mais de 2 tentativas. Informar o usuário e pedir busca manual com prints |
| Insistir mais de 3x `create_tab` para Facebook | Loop garantido — o bloqueio é por domínio, não por sessão | Usar estratégia de fallback (prints manuais) após 2 falhas |
| Tentar `curl` direto na Ad Library | Retorna apenas o challenge JavaScript do Cloudflare, inútil para scraping | Usar Camofox ou navegador real com interface gráfica |
| Tentar Graph API sem token de acesso válido | API retorna HTTP 500 sem autenticação adequada | Obter token de acesso com permissões `ads_read` antes de usar a API |
| Usar `npx playwright install` no servidor | Timeout de 120s+ em VPS sem GPU, overhead desnecessário | Camofox já resolve o navegador; não instalar Playwright no servidor |
| `server_status` reporta `running: true` mas Facebook ainda falha | Bloqueio é por domínio, não afeta outros sites | Testar com outro domínio (ex: google.com) para confirmar que o Camofox está funcional |

---

## Task-Specific Questions

1. Qual clínica ou região específica devo focar na análise competitiva?
2. Modo B2C (pacientes) ou B2B (donos de clínica)?
3. Há concorrentes específicos que você já conhece e quer que eu analise primeiro?
4. Qual o objetivo principal: copiar estratégias vencedoras, encontrar gaps, ou auditar posicionamento?
5. Prefere relatório detalhado (todos os anúncios) ou resumo executivo (top 3-5 concorrentes)?

---

## Tool Integrations

| Ferramenta | Uso | Método | Guide |
|------------|-----|--------|-------|
| Camofox Browser | Acessar Meta Ad Library, capturar anúncios via snapshot | MCP `mcp_camofox_*` | `mcp_camofox_server_status` |
| Meta Ads Library | Fonte dos anúncios concorrentes | Via Camofox (URL direta) | `https://www.facebook.com/ads/library/` |
| Fal.ai | Analisar/recriar criativos dos concorrentes | MCP `mcp_fal_ai_*` | `flux-prompt-engineer` skill |

---

## Related Skills

- **flux-ads-audit**: Para auditar a qualidade dos anúncios após a espionagem — use quando quiser avaliar se os anúncios do cliente estão competitivos vs. concorrentes
- **flux-prompt-engineer**: Para recriar ou melhorar criativos baseados nos achados da espionagem competitiva
- **flux-meta-ads-relatorio**: Para cruzar dados de performance de anúncios do cliente com o cenário competitivo
