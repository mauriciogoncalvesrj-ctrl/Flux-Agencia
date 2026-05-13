# Scoring and Prompt Database Update Process

## Quality Audit Procedure (Portão 5 Extension)

During image generation and auditing, follow this enhanced process:

1. **Generate image** with the selected model
2. **Audit result** using the 5-point quality rubric:
   - Legibilidade (Legibility): Text clarity and readability
   - Coerência (Coherence): Logical consistency of elements
   - Hierarquia (Hierarchy): Visual priority and flow
   - CTA: Visibility and effectiveness of call-to-action
   - Qualidade premium: Overall luxury/executive feel

3. **Score each criterion** 1-10, calculate average
4. **Decision threshold**: 
   - Score ≥ 8: Approved
   - Score < 8: Rejected - return to appropriate gate for revision

5. **Database Updates** (when approved):
   - For NEW prompts: Add to prompts-db.json with initial score
   - For EXISTING prompts: Update the 'score' field with new audit value
   - Always include: model, aspect_ratio, prompt, negative, notes, category, approved_by, score

## Example Update Entry

```json
"bichectomia_educativo_slide1_v2": {
  "model": "image_generate",
  "aspect_ratio": "portrait",
  "prompt": "[UPDATED PROMPT TEXT HERE]",
  "negative": "people, person, face, text, logo, watermark, clutter",
  "notes": "Versão 2 com iluminação ajustada baseado em teste A/B",
  "category": "bichectomia",
  "approved_by": "flux-prompt-engineer",
  "score": 9
}
```

## Scoring Guidelines

- **9-10**: Exceptional - exceeds all criteria, ready for immediate deployment
- **7-8**: Good - meets minimum threshold, acceptable for use
- **5-6**: Fair - needs improvement in 1-2 areas
- **<5**: Poor - requires fundamental revision

## Common Score Improvement Triggers

| Score Issue | Likely Cause | Recommended Fix |
|-------------|--------------|-----------------|
| Legibilidade < 6 | Text too small/busy background | Increase text contrast, simplify background |
| Coerência < 6 | Elements don't belong together | Review art direction, ensure thematic unity |
| Hierarquia < 6 | Unclear visual flow | Adjust size/position/color weighting |
| CTA < 6 | Poor placement/visibility | Move to bottom safe zone, increase contrast |
| Qualidade premium < 6 | Looks generic/cheap | Add luxury references (Editorial, Architectural Digest) |

## Version Control Notes

When updating existing prompts in the database:
1. Create new entry with descriptive suffix (_v2, _optimized, etc.)
2. Preserve original for A/B testing comparison
3. Document specific changes in 'notes' field
4. Only promote to primary name after multiple successful tests