# Prompts Aprovados — Base de Conhecimento

Local no disco: `/opt/data/flux-tools/prompts-db.json`

## Categorias e Templates (11 aprovados)

| Key | Modelo | Formato | Uso |
|-----|--------|---------|-----|
| `spa_ambiente` | Flux 2 Pro | square | Ambiente de clínica, Architectural Digest |
| `carrossel_capa_luxo` | image_generate | portrait 4:5 | Capa de carrossel com texto integrado |
| `anuncio_meta_beleza` | Flux 2 Pro | 3:4 | Anúncio Meta produto de beleza |
| `bichectomia_educativo_slide1` | image_generate | portrait 4:5 | Slide educativo bichectomia |
| `harmonizacao_educativo_slide1` | image_generate | portrait 4:5 | Slide educativo harmonização |
| `preenchimento_labial_slide1` | image_generate | portrait 4:5 | Slide educativo preenchimento |
| `skinbooster_educativo_slide1` | image_generate | portrait 4:5 | Slide educativo skinbooster |
| `promo_vagas_limitadas` | image_generate | portrait 4:5 | Slide promocional urgência |
| `cta_agende_whatsapp` | image_generate | portrait 4:5 | CTA final WhatsApp |
| `antes_depois_resultado` | image_generate | portrait 4:5 | Antes/depois abstrato |
| `faq_slide_template` | image_generate | portrait 4:5 | Slide FAQ genérico |

## Templates de Carrossel Completo

Arquivo: `/opt/data/flux-tools/templates-instagram-estetica.md`

5 procedimentos × 5 formatos = 25 templates:
- Bichectomia: B1-B5
- Harmonização: H1-H5  
- Preenchimento Labial: P1-P5
- Skinbooster: S1-S5

Cada template com: formato, estrutura de slides, copy/legenda, hashtags, CTA.

## Paleta de Cores Padrão (Clínica de Estética Luxo)

| Elemento | Cor | Hex |
|----------|-----|-----|
| Background principal | Warm Ivory | #F5F0E8 |
| Background escuro | Dark Navy | #0a1628 |
| Texto principal | White | #FFFFFF |
| Texto secundário | Gray | #888888 |
| Accent/Gold | Soft Gold | #C9A96E |
| Alert | Red | #DC5046 |
| Success | Green | #50C878 |

## Regras para Adicionar Novo Prompt

1. Executar pipeline completo (consulta → engenharia → geração)
2. Score ≥ 7 para aprovar
3. Adicionar ao JSON com campos obrigatórios: model, prompt, negative, category, score
4. Documentar notas de contexto no campo `notes`