---
name: reference-flux-visual
description: Padrao visual Flux Agency — brand-profile + preset banana + skill ads-carousel + pasta de refs no Drive
metadata: 
  node_type: memory
  type: reference
  originSessionId: bd704387-842c-4ce4-90b2-4f2ce47dc477
---

Padrao visual de criativos Flux (clinicas de estetica) — 4 sub-estilos: Cyber/Tech, Luxo/Educacional, Alerta/Polemico, Personal-Brand Mauricio.

**Onde estao os artefatos:**

- **Brand profile completo (JSON):** `projects/c--Users-windows--claude/docs/creative/flux-brand/flux-brand-profile.json` — paleta, voice, tipografia, sub-estilos, hooks padrao
- **Banana preset:** `~/.banana/presets/flux-clinicas.json` — paleta + 4 sub-estilos prontos para injecao em prompts
- **Skill text-heavy carrossel:** `~/.claude/skills/ads-carousel/SKILL.md` — diferente da `ads-generate` (essa permite e exige texto na imagem)
- **Pasta de referencias visuais (25 imagens):** `J:/Meu Drive/#01 - AGENCIA MOTIVA DIGITAL/#07 - CLIENTES/01 - ATIVOS/01 - SOMOS FLUX/#09 - Conteudo/ABRIL/images/`

**Paleta canonica:**
- `#0A0A0A` preto profundo (background dominante)
- `#C9A961` / `#D4AF37` dourado premium (accent principal)
- `#00D4FF` cyan eletrico (sub-estilo Cyber)
- `#FFB400` / `#D62828` amarelo alerta + vermelho perigo (sub-estilo Alerta)

**Regras criticas:**
1. Headline ocupa 50-65% da imagem, UPPERCASE, fonte condensada bold (Anton/Bebas/Oswald)
2. Sempre PT-BR com acentuacao correta
3. Numeracao de slide top-right (1/7, 5/10)
4. CTA final formato: "Comenta '[PALAVRA]' e eu te mostro [beneficio]"
5. PROIBIDO: rosa pastel, lilas, azul-bebe, fundo branco dominante, stock photo de equipe sorrindo, mockup apple-style

**Quando usar qual skill:**
- `/ads carousel` (ads-carousel) — para carrosseis Instagram no padrao Flux com TEXTO na imagem
- `/ads generate` (ads-generate) — para criativos genericos SEM texto (estilo SaaS minimalista). NAO usar para clientes Flux/clinicas

Linkado: [[user-mauricio]] (perfil), [[feedback-brand-flux]] (brand rules), [[project-flux-contexto]] (stack)
