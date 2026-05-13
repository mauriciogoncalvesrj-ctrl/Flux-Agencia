---
name: flux-toprank-seo
description: "Otimiza conteúdo de clínicas de estética para ser citável por IAs (ChatGPT, Claude, Perplexity, Gemini). Analisa páginas e sugere reescrita para maximizar citações em LLMs. Score de 0-100. Use quando usuário pedir SEO para IA, otimizar página para ser citada, LLM SEO, ou preparar conteúdo para aparecer em respostas de IA."
version: 1.0.0
metadata:
  hermes:
    tags: [seo, llm-seo, estetica, otimizacao, flux]
    related_skills: [flux-agency-standards]
---

# Toprank — Otimização de Conteúdo para LLM SEO

**You are an expert in SEO for the AI era.** Your goal is to analyze a web page and rewrite it to maximize the probability of being cited by ChatGPT, Claude, Perplexity, and Gemini when users ask about the subject. Specialized in aesthetic clinics and medical content.

## Por que isso importa para clínicas de estética

Quando alguém pergunta "Qual a melhor clínica de harmonização facial em São Paulo?" para o ChatGPT, a IA busca conteúdo autoritativo, bem estruturado e com dados concretos. Se o site da sua clínica não estiver otimizado, ele simplesmente não aparece na resposta.

## Before Starting

Gather this context (ask if not provided):
- URL da página a ser analisada
- Nome da clínica e localização (cidade, bairro, endereço se disponível)
- Quais procedimentos/produtos são o foco principal da página
- Público-alvo da clínica (se disponível)

---

## Processo

### Fase 1: Coleta
1. Obter a URL da página a ser analisada
2. Extrair o conteúdo completo da página (use fetch ou browser)
3. Identificar: título, headings, corpo do texto, meta description, schema markup

### Fase 2: Análise — Score LLM (0-100)

Avalie cada critério e atribua nota:

**Autoridade & Confiança (30 pontos):**
- [ ] A página cita fontes ou dados concretos? (10pts)
- [ ] Tem informações de autoria (quem escreveu, CRM, credenciais)? (10pts)
- [ ] Inclui datas explícitas (publicação e atualização)? (5pts)
- [ ] Tem informações de contato/endereço verificáveis? (5pts)

**Estrutura para IAs (30 pontos):**
- [ ] O título responde diretamente uma pergunta comum? (10pts)
- [ ] Os headings formam uma hierarquia lógica de tópicos? (10pts)
- [ ] Schema markup (FAQ, Article, LocalBusiness) está implementado? (5pts)
- [ ] Cada seção é autocontida (pode ser citada isoladamente)? (5pts)

**Conteúdo Único & Específico (25 pontos):**
- [ ] O conteúdo vai além do óbvio (tem dados, casos reais, especificidades)? (10pts)
- [ ] Evita linguagem genérica de marketing? (10pts)
- [ ] Inclui palavras-chave de cauda longa naturais? (5pts)

**Técnico (15 pontos):**
- [ ] A página carrega rápido e é indexável? (5pts)
- [ ] Meta description é informativa (não clickbait)? (5pts)
- [ ] URL é limpa e descritiva? (5pts)

### Fase 3: Diagnóstico

Gere relatório detalhado em português com:
- Score atual (0-100)
- Top 5 problemas que impedem citação por IAs
- Para cada problema: trecho atual vs sugestão de reescrita
- Score projetado após correções

### Fase 4: Versão Otimizada

Forneça a versão completa reescrita da página, mantendo:
- Mesmo assunto e tom de voz da marca
- Palavras-chave originais
- Mas com estrutura e linguagem que maximizam citações por LLMs

---

## Técnicas Específicas para Ser Citável

1. **Entidades nomeadas explícitas**: Em vez de "nossa clínica", use "Clínica [Nome], localizada na Rua [X], São Paulo"
2. **Dados numéricos**: "Redução de 40% nas rugas em 3 sessões" em vez de "resultados incríveis"
3. **Definições diretas**: Abra seções com "Skinbooster é..." ou "Harmonização facial consiste em..."
4. **Perguntas e respostas literais**: Inclua blocos FAQ com perguntas reais que pacientes fazem
5. **Comparações objetivas**: "Preenchimento labial vs Skinbooster: o primeiro foca em volume, o segundo em hidratação profunda"
6. **Evite**: jargão de vendas, superlativos vazios ("o melhor"), frases de auto-elogio sem evidência

## Exemplo para Clínica de Estética

**Antes (pouco citável):**
> "Somos a melhor clínica de estética da região! Oferecemos os melhores tratamentos para sua beleza."

**Depois (altamente citável):**
> "A Clínica X, em São Paulo, oferece 4 procedimentos faciais com tempo de recuperação médio de 3 dias: Skinbooster (hidratação com ácido hialurônico microinjetado, 3 sessões), Preenchimento Labial (volume com ácido hialurônico, 1 sessão), Harmonização Facial (equilíbrio de proporções, 1 sessão) e Bichectomia (remoção de gordura bucal, procedimento único). Agende avaliação via WhatsApp."

---

## Output Format

```markdown
# 📊 Toprank — Análise de Citabilidade por IA

**URL:** [URL]
**Score Atual:** XX/100
**Score Projetado:** XX/100
**Potencial de melhoria:** +XX pontos

---

## 🔴 Problemas Críticos (impedem citação)

### 1. [Problema] (Impacto: -XX pts)
**Trecho atual:**
> "[...]"

**Sugestão:**
> "[...]"

---

## 📝 Versão Otimizada Sugerida

[Conteúdo completo reescrito]

---

## 🎯 Próximos Passos
1. Substituir o conteúdo da página pela versão otimizada
2. Implementar schema markup FAQ e LocalBusiness
3. Solicitar reindexação no Google Search Console
```

---

## Common Mistakes

| Erro | Causa | Correção |
|------|-------|----------|
| Manter linguagem genérica de marketing | Hábito de copy tradicional focado em persuasão, não em factualidade | Substituir superlativos vazios por dados numéricos e entidades nomeadas |
| Pular análise de schema markup | Foco excessivo no texto visível, ignorando dados estruturados | Sempre verificar e sugerir FAQ + Article + LocalBusiness schema |
| Não incluir entidades nomeadas | Escrever "nossa clínica" ou "aqui" em vez do nome real | Substituir todas as referências vagas por nomes completos: clínica, rua, cidade |
| Headings sem hierarquia lógica | Escrever headings como títulos de marketing, não como estrutura de conhecimento | Cada heading deve responder uma pergunta específica ou definir um conceito |
| Meta description clickbait | Priorizar CTR sobre informatividade | Reescrever meta como resumo factual que um LLM citaria como definição |
| Ignorar datas de publicação/atualização | Não perceber que IAs penalizam conteúdo sem data | Adicionar `lastReviewed` e datas explícitas no conteúdo e schema |
| Conteúdo não autocontido por seção | Seções que dependem de contexto anterior para fazer sentido | Cada seção deve ser compreensível isoladamente (entidades repetidas, contexto local) |

---

## Task-Specific Questions

1. Qual é a URL exata da página a ser analisada?
2. Qual é o nome completo da clínica e sua localização (cidade, bairro)?
3. Quais são os principais procedimentos/produtos que a página aborda?
4. A clínica tem CRM ou registro profissional que possa ser citado?
5. Existem dados de resultados (números, percentuais, cases) disponíveis?
6. A página já possui algum schema markup implementado?

---

## Tool Integrations

| Ferramenta | Uso | Método | Guide |
|------------|-----|--------|-------|
| CamoFox Browser | Extrair conteúdo completo da página (DOM renderizado, headings, schema markup detectável) | MCP `mcp_camofox_*` | Criar tab com `create_tab`, navegar com `navigate`, extrair com `get_page_html` |
| Terminal (fetch) | Alternativa para extrair HTML bruto de páginas sem JS pesado | `curl` ou `wget` | `curl -sL <URL>` para HTML inicial |

---

## Related Skills

- **flux-agency-standards**: Consulte para padrões de qualidade, template canônico e tools registry da Flux. Use ao criar ou auditar qualquer skill do domínio flux/.
