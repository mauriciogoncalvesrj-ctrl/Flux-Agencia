---
name: flux-competitor-spy
description: "Espionagem competitiva automática para clínicas de estética. Usa o Camofox Browser para acessar a Biblioteca de Anúncios do Meta e capturar anúncios de concorrentes. Analisa copy, imagem e ofertas. Gera relatório de inteligência competitiva. Use quando usuário pedir para espionar concorrentes, ver anúncios da concorrência, ou pesquisa de mercado."
user-invokable: true
argument-hint: "[termo de busca] [cidade/região]"
---

# 🔭 Espionagem Competitiva — Agência Flux

Usa o Camofox Browser para pesquisar a **Biblioteca de Anúncios do Meta** e capturar o que os concorrentes estão anunciando.

## Pré-requisitos

- MCP `camofox` deve estar ativo (já configurado no seu Hermes)
- Se falhar, verifique `mcp_camofox_server_status`

## Processo

### Passo 1: Busca na Biblioteca de Anúncios

1. Criar aba no Camofox: `mcp_camofox_create_tab`
2. Navegar para: `https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=BR&q=[TERMO_DE_BUSCA]&search_type=keyword_unordered&media_type=all`
3. Substitua `[TERMO_DE_BUSCA]` por termos como:
   - `"harmonização facial" "São Paulo"`
   - `"bichectomia" "clínica"`
   - `"preenchimento labial" "estética"`
   - `nome de clínicas concorrentes específicas`

### Passo 2: Captura dos Anúncios

Use `mcp_camofox_snapshot` para ler a página. Extraia de cada anúncio:
- Texto/copy do anúncio
- Headline/chamada principal
- Tipo de mídia (imagem/vídeo/carrossel)
- Plataformas (Facebook, Instagram, Messenger)
- Data de início
- Se tem CTA (Call-to-Action) e qual

### Passo 3: Análise Competitiva

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

### Passo 4: Relatório de Inteligência

Gere relatório em português:

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

## Buscas Recomendadas para Clínicas de Estética

Execute estas buscas em sequência (máximo 5 por vez para não sobrecarregar):

1. `"harmonização facial" "clínica"` → Visão geral do mercado
2. `"preenchimento labial" "promoção"` → Estratégias de preço
3. `"bichectomia" "antes e depois"` → Criativos de alto desempenho
4. `"skinbooster" "resultado"` → Como vendem o procedimento
5. `nome da clínica concorrente específica` → Análise direta

## ⚠️ PITFALLS — Leia antes de executar

### Meta Ad Library é EXTREMAMENTE bloqueada
O Meta implementa múltiplas camadas de proteção que impedem acesso automatizado:
- **Cloudflare `__rd_verify`** — desafio JavaScript que só navegadores reais resolvem
- **Graph API** — exige token de acesso com permissões específicas, retorna 500 sem ele
- **Camofox** — falhou repetidamente (`NAVIGATION_FAILED`, `Internal server error`) ao tentar acessar `facebook.com`, mesmo com o servidor rodando e outras abas funcionando

### Quando o Camofox falha no Facebook
- `mcp_camofox_create_tab` para URLs do Facebook → `NAVIGATION_FAILED`
- `mcp_camofox_navigate_and_snapshot` para Facebook → `NAVIGATION_FAILED`
- `mcp_camofox_server_status` pode reportar `running: true` mesmo assim — o bloqueio é por domínio
- `mcp_camofox_list_tabs` e `mcp_camofox_close_tab` continuam funcionando

### Estratégia de fallback
Se o acesso automatizado falhar (o que é o caso MAIS COMUM), NÃO insista mais de 2 tentativas. Em vez disso:
1. Informe o usuário que o Meta está bloqueando
2. Peça que ele faça a busca manualmente em https://www.facebook.com/ads/library/
3. Peça prints da tela de resultados
4. Analise os prints e gere o relatório

### O que NÃO fazer
- ❌ Tentar mais de 3x `create_tab` para Facebook (loop garantido)
- ❌ Tentar `curl` direto (retorna só o challenge JS, inútil)
- ❌ Tentar Graph API sem token de acesso válido (retorna 500)
- ❌ Usar `npx playwright install` no servidor (timeout de 120s+ em VPS sem GPU)

## Dica de Automação

Para automação confiável, use um **navegador desktop real** (não VPS):
- Abra a Ad Library manualmente 1x por semana
- Envie os prints para o Telegram @atlas_fluxia_bot
- O agente processa automaticamente

Cron jobs no servidor para esta skill NÃO são recomendados — a taxa de falha é >90%.
