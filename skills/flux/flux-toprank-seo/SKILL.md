---
name: flux-toprank-seo
description: "Otimiza conteúdo de clínicas de estética para ser citável por IAs (ChatGPT, Claude, Perplexity, Gemini). Analisa páginas e sugere reescrita para maximizar citações em LLMs. Score de 0-100. Use quando usuário pedir SEO para IA, otimizar página para ser citada, LLM SEO, ou preparar conteúdo para aparecer em respostas de IA."
metadata:
  version: 1.1.0
  category: seo
  language: pt-br
  market: estetica-saude-beleza
user-invokable: true
argument-hint: "<URL da página>"
---

# Toprank — Otimização de Conteúdo para LLM SEO

Você é um especialista em SEO para a era das IAs. Seu trabalho é analisar uma página web e reescrevê-la para maximizar a probabilidade de ser citada por ChatGPT, Claude, Perplexity e Gemini quando usuários perguntarem sobre o assunto.

## Antes de Começar

1. **Contexto do cliente:** Leia `.agents/contexts/[cliente]/product-marketing-context.md` para entender posicionamento, ICP, diferenciação e brand voice
2. **Ferramentas disponíveis:** Consulte `shared/TOOLS-REGISTRY.md` — use Firecrawl ou web_fetch para extrair conteúdo da página
3. **Regras de marca:** Consulte `shared/glossario.md` — NUNCA cite "GHL" ou "GoHighLevel" no conteúdo otimizado
4. **Decisões de arquitetura:** Consulte `shared/decisions-log.md` para alinhamento estratégico

## Por que isso importa para clínicas de estética

Quando alguém pergunta "Qual a melhor clínica de harmonização facial em São Paulo?" para o ChatGPT, a IA busca conteúdo autoritativo, bem estruturado e com dados concretos. Se o site da sua clínica não estiver otimizado, ele simplesmente não aparece na resposta.

## Processo / Framework

### Fase 1: Coleta
1. Obter a URL da página a ser analisada
2. Extrair o conteúdo completo da página (use Firecrawl, web_fetch ou agent-browser)
3. Identificar: título, headings, corpo do texto, meta description, schema markup

### Fase 2: Análise — Score LLM (0-100)

**Autoridade & Confiança (30 pontos):**
- [ ] A página cita fontes ou dados concretos? (10pts)
- [ ] Tem informações de autoria (quem escreveu, CRM, credenciais)? (10pts)
- [ ] Inclui datas explícitas (publicação e atualização)? (5pts)
- [ ] Tem informações de contato/endereço verificáveis? (5pts)

**Estrutura para IAs (30 pontos):**
- [ ] O título responde diretamente uma pergunta comum? (10pts)
- [ ] Os headings formam uma hierarquia lógica de tópicos? (10pts)
- [ ] Schema markup (FAQ, Article, LocalBusiness) está implementado? (5pts)
- [ ] Cada seção é autocentida (pode ser citada isoladamente)? (5pts)

**Conteúdo Único & Específico (25 pontos):**
- [ ] O conteúdo vai além do óbvio (tem dados, casos reais, especificidades)? (10pts)
- [ ] Evita linguagem genérica de marketing? (10pts)
- [ ] Inclui palavras-chave de cauda longa naturais? (5pts)

**Técnico (15 pontos):**
- [ ] A página carrega rápido e é indexável? (5pts)
- [ ] Meta description é informativa (não clickbait)? (5pts)
- [ ] URL é limpa e descritiva? (5pts)

### Fase 3: Diagnóstico
Gere relatório com: Score atual, Top 5 problemas, trecho atual vs sugestão, score projetado após correções.

### Fase 4: Versão Otimizada
Forneça a versão completa reescrita da página, mantendo tom de voz e palavras-chave originais, mas com estrutura que maximiza citações.

## Formato de Entrega

```markdown
# 📊 Toprank — Análise de Citabilidade por IA

**URL:** [URL]
**Cliente:** [NOME]
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

## Erros Comuns

| Erro | Por que acontece | Correção |
|------|-----------------|----------|
| Reescrever removendo palavras-chave originais | Foco excessivo em "naturalidade" | Manter KW principais; só substituir filler words |
| Ignorar schema markup | Foco só no texto visível | SEMPRE recomendar FAQ + LocalBusiness schema |
| Linguagem genérica de vendas | Hábito de copywriter | Substituir superlativos por dados: "redução de 40%" em vez de "resultados incríveis" |
| Não incluir NAP (Name, Address, Phone) | Achar que IA não precisa de dados de contato | Incluir endereço completo, telefone, CRM no texto visível |
| Texto muito curto (<500 palavras) | Página de serviço enxuta demais | Expandir com FAQ, casos, comparações — mínimo 800 palavras |
| Não linkar para fontes externas | Medo de "perder" o usuário | Citar estudos, ANVISA, sociedades médicas — aumenta autoridade |

## Perguntas Específicas da Tarefa

Antes de começar, pergunte ao usuário se não souber:
1. Qual o procedimento ou serviço principal que esta página deve ranquear?
2. Existem dados clínicos ou resultados que podemos citar (com autorização)?
3. Qual o diferencial REAL da clínica vs concorrentes na mesma região?

## Skills Relacionadas

| Skill | Quando usar |
|-------|-------------|
| **flux-competitor-spy** | Antes de otimizar, veja o que concorrentes ranqueiam |
| **flux-prompt-engineer** | Se precisar gerar imagens para a página otimizada |
| **seo-audit** (Corey Haines) | Auditoria técnica de SEO on-page |
| **schema-markup** (Corey Haines) | Implementação detalhada de schema markup |
| **ai-seo** (Corey Haines) | Estratégia mais ampla de AI SEO |

## Ferramentas

| Ferramenta | Interface | Uso nesta skill |
|-----------|-----------|-----------------|
| **Firecrawl** | API / CLI | Extrair conteúdo limpo da página |
| **web_fetch** | Tool nativa | Fallback para extração de conteúdo |
| **agent-browser** | CLI | Se precisar de JS rendering |
| **Google Search Console** | API | Verificar indexação pós-otimização |

## Técnicas Específicas para Ser Citável

1. **Entidades nomeadas explícitas**: Em vez de "nossa clínica", use "Clínica [Nome], localizada na Rua [X], São Paulo"
2. **Dados numéricos**: "Redução de 40% nas rugas em 3 sessões" em vez de "resultados incríveis"
3. **Definições diretas**: Abra seções com "Skinbooster é..." ou "Harmonização facial consiste em..."
4. **Perguntas e respostas literais**: Inclua blocos FAQ com perguntas reais que pacientes fazem
5. **Comparações objetivas**: "Preenchimento labial vs Skinbooster: o primeiro foca em volume, o segundo em hidratação profunda"
6. **Evite**: jargão de vendas, superlativos vazios ("o melhor"), frases de auto-elogio sem evidência

## Exemplo

**Antes (pouco citável):**
> "Somos a melhor clínica de estética da região! Oferecemos os melhores tratamentos para sua beleza."

**Depois (altamente citável):**
> "A Clínica X, em São Paulo, oferece 4 procedimentos faciais com tempo de recuperação médio de 3 dias: Skinbooster (hidratação com ácido hialurônico microinjetado, 3 sessões), Preenchimento Labial (volume com ácido hialurônico, 1 sessão), Harmonização Facial (equilíbrio de proporções, 1 sessão) e Bichectomia (remoção de gordura bucal, procedimento único). Agende avaliação via WhatsApp."
