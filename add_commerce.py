#!/usr/bin/env python3
"""Apply Commerce subject changes to question_bank_generator_4.html"""

with open('question_bank_generator_4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── 1. Enable Commerce in SUBJECTS ──────────────────────────────────────────
old = "{ id:'Commerce', icon:'💼',  label:'Commerce',       icse:false, cbse:false, soon:true },"
new = "{ id:'Commerce', icon:'💼',  label:'Commerce',       icse:true,  cbse:false },"
assert old in html, "SUBJECTS Commerce line not found"
html = html.replace(old, new, 1)

# ── 2. Add Grade 11 and 12 to page-1 grade selector ─────────────────────────
old_g = '            <option value="10">Grade 10</option>\n          </select>\n        </div>\n\n        <div class="btn-row">\n          <button class="btn btn-primary btn-lg" onclick="page1Next()">Continue to Chapter Structure →</button>'
new_g = '            <option value="10">Grade 10</option>\n            <option value="11">Grade 11</option>\n            <option value="12">Grade 12</option>\n          </select>\n        </div>\n\n        <div class="btn-row">\n          <button class="btn btn-primary btn-lg" onclick="page1Next()">Continue to Chapter Structure →</button>'
assert old_g in html, "Page-1 grade selector end not found"
html = html.replace(old_g, new_g, 1)

# ── 3. Update getPromptKey() to route Commerce ICSE ─────────────────────────
old_gpk = "function getPromptKey() {\n  if (state.subject === 'English' && state.curriculum === 'CBSE') return 'ENGLISH_CBSE';"
new_gpk = "function getPromptKey() {\n  if (state.subject === 'Commerce' && state.curriculum === 'ICSE') return 'COMMERCE_ICSE';\n  if (state.subject === 'English' && state.curriculum === 'CBSE') return 'ENGLISH_CBSE';"
assert old_gpk in html, "getPromptKey function start not found"
html = html.replace(old_gpk, new_gpk, 1)

# ── 4. Add COMMERCE_ICSE to PROMPTS (appended before closing of PROMPTS block) ─
# Find the end of the PROMPTS object. The PROMPTS object ends with "};" after the last key.
# Strategy: find the last big prompt key block boundary near line 970 area.
# We'll insert before the closing "};" of PROMPTS.
# Locate by searching for the unique closing pattern after the last prompt entry.

COMMERCE_PROMPT = r"""
'COMMERCE_ICSE': `
---
GLOSSARY_CREATION_PROMPT
You are an expert Commerce teacher for Grade {{Grade}} ICSE students.

Create a comprehensive Glossary for the chapter: **{{ChapterName}}**

INSTRUCTIONS:
- Generate 15–20 important commerce terms from this chapter
- Each term must have a clear, student-friendly definition (2–3 sentences)
- Include examples where applicable
- Focus on terms that are essential for understanding the chapter

OUTPUT FORMAT (plain text, no JSON):
Glossary — {{ChapterName}}

Term 1: [Term Name]
Definition: [Clear definition with example if applicable]

Term 2: [Term Name]
Definition: [Clear definition with example if applicable]

[Continue for all terms...]

---
TERMS_CREATION_PROMPT
You are an expert Commerce teacher for Grade {{Grade}} ICSE students.

Create detailed Terms and Definitions for the chapter/topic: **{{ChapterName}}** — **{{TopicName}}**

INSTRUCTIONS:
- Generate 10–15 key terms specific to this topic
- Provide precise, curriculum-aligned definitions
- Include the significance or application of each term in commerce context

OUTPUT FORMAT (plain text, no JSON):
Terms and Definitions — {{TopicName}}

1. [Term]: [Definition] — [Significance/Application]
2. [Term]: [Definition] — [Significance/Application]
[Continue...]

---
LO_CREATION_PROMPT
You are an expert Commerce teacher for Grade {{Grade}} ICSE students.

Generate Learning Outcomes for the chapter/topic: **{{ChapterName}}** — **{{TopicName}}**

INSTRUCTIONS:
- Write 8–12 specific, measurable Learning Outcomes
- Use Bloom's Taxonomy action verbs (define, explain, analyse, evaluate, apply, compare, etc.)
- Each LO should be achievable and relevant to ICSE Grade {{Grade}} Commerce curriculum
- Cover all cognitive levels: Factual, Understanding, Application, Analysing, Evaluating

OUTPUT FORMAT:
LO1: [Action verb] [specific learning outcome]
LO2: [Action verb] [specific learning outcome]
[Continue for all LOs...]

---
LO_VALIDATION_PROMPT
You are an expert Commerce teacher. Review and validate the following Learning Outcomes for {{TopicName}}:

{{LearningOutcomes}}

Ensure each LO is:
- Specific and measurable
- Aligned with ICSE Grade {{Grade}} Commerce curriculum
- Covering appropriate cognitive levels
- Using correct Bloom's Taxonomy verbs

Provide the validated/refined LOs in the same format.

---
PLT_CREATION_PROMPT
You are an expert Commerce teacher for Grade {{Grade}} ICSE students.

Create a Proficiency Level Transcript (PLT) for: **{{ChapterName}}** — **{{TopicName}}**

Based on these Learning Outcomes:
{{LearningOutcomes}}

INSTRUCTIONS:
- Create a structured transcript that covers all the LOs above
- Write in a clear, engaging narrative style suitable for Grade {{Grade}} students
- Include explanations, examples, and real-world applications
- The transcript should serve as a comprehensive study guide
- Cover Factual, Understanding, Application, Analysing, and Evaluating levels

OUTPUT FORMAT (plain text narrative):
Proficiency Level Transcript — {{TopicName}}

[Write a comprehensive, well-structured narrative covering all LOs with examples and explanations...]

---
PLT_VALIDATION_PROMPT
You are an expert Commerce teacher. Review the following PLT for {{TopicName}} and ensure it covers all the Learning Outcomes adequately.

Validate and refine if needed to ensure complete coverage of all LOs.

---
OBJECTIVE_CREATION_PROMPT
You are an expert Commerce teacher for Grade {{Grade}} ICSE students.

Generate objective questions for the chapter/topic: **{{ChapterName}}** — **{{TopicName}}**

Based on these Learning Outcomes:
{{LearningOutcomes}}

QUESTION TYPES TO GENERATE:
Generate a mix of the following 14 question types as appropriate for the topic:
1. SCQ — Single Correct Question (4 options, 1 correct)
2. MSQ — Multiple Select Question (4 options, 2+ correct)
3. TF — True/False
4. FIB — Fill in the Blank
5. MTF — Match the Following
6. OA — Ordering/Arrange in sequence
7. CS — Case Study based
8. DIA — Diagram/Chart based
9. CALC — Calculation based
10. DEF — Definition based
11. DIFF — Differentiate between
12. LIST — List/Enumerate
13. APPLY — Application based scenario
14. EVAL — Evaluate/Justify

INSTRUCTIONS:
- Generate 15–20 questions covering all cognitive levels (Factual, Understanding, Application, Analysing, Evaluating)
- Cover Easy, Medium, and Hard difficulty levels
- Each question must test a specific LO
- The "questionType" field must be one of the 14 types above
- For SCQ: provide exactly 4 options, 1 correct answer
- For MSQ: provide exactly 4 options, 2 or more correct answers
- For TF: options are ["True", "False"]
- For FIB: question contains a blank "_____", no options needed (options: [])
- For MTF: question contains two columns to match, options list the matching pairs
- For other types: options may be empty [] if not applicable; answers must still be provided

OUTPUT: Return ONLY a valid JSON array. No markdown, no explanation.

Every element MUST use EXACTLY this schema:
{
  "cognitiveLevel": "Understanding",
  "difficultyLevel": "Medium",
  "questionType": "SCQ",
  "question": "<question text>",
  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
  "answers": ["Correct option text exactly"],
  "solution": "Brief explanation of the correct answer"
}

MANDATORY RULES:
- "questionType" MUST be one of: SCQ, MSQ, TF, FIB, MTF, OA, CS, DIA, CALC, DEF, DIFF, LIST, APPLY, EVAL
- "answers" is always an array of strings
- "options" is always an array of strings (can be empty [] for FIB, LIST, DEF type)
- Allowed field names ONLY: cognitiveLevel, difficultyLevel, questionType, question, options, answers, solution
- FORBIDDEN fields: question_type, cognitive_level, difficulty, type_tag, correct_answer, explanation, hint, topic
- NEVER include marks or mark allocations inside the "question" string
- Do NOT wrap output in markdown code fences
`,"""

# Find location to insert — before closing of PROMPTS object
# The PROMPTS object ends before the line "// Steps for ICSE Science subjects"
MARKER = '  "MATHEMATICS_CBSE":'
assert MARKER in html, "MATHEMATICS_CBSE key not found in PROMPTS"
# Find the closing "};\n" that follows MATHEMATICS_CBSE entry (the one at line 973)
# We'll find the position of the last entry and locate the }; after it
math_pos = html.rfind(MARKER)
close_pos = html.find('\n};\n', math_pos)
assert close_pos != -1, "PROMPTS closing }; not found after MATHEMATICS_CBSE"
html = html[:close_pos] + ',\n' + COMMERCE_PROMPT.strip() + '\n' + html[close_pos:]

# ── 5. Add Commerce isCommerce flag and workflow in runConceptAgent ──────────
# After the isBio67 definition, add isCommerce
old_bio67 = "  // BIOLOGY_ICSE_67 now has all sections; use masterPrompt for everything\n  const isBio67 = state.subject === 'Biology' && state.curriculum === 'ICSE' && (state.grade === '06' || state.grade === '07');\n  const baseMasterPrompt = masterPrompt;"
new_bio67 = "  // BIOLOGY_ICSE_67 now has all sections; use masterPrompt for everything\n  const isBio67 = state.subject === 'Biology' && state.curriculum === 'ICSE' && (state.grade === '06' || state.grade === '07');\n  const isCommerce = state.subject === 'Commerce';\n  const baseMasterPrompt = masterPrompt;"
assert old_bio67 in html, "isBio67 block not found"
html = html.replace(old_bio67, new_bio67, 1)

# ── 6. Add commerce_glossary step before TERMS step ─────────────────────────
old_prereq_step = "  // PREREQ — runs in full mode (chapter only) OR in prereqOnly mode (chapter only)\n  await runStep('prereq', 'Pre-requisites', '🔍', isChapter && !isEnglish && (!singleStepMode || prereqOnly), async () => {"
new_prereq_step = """  // COMMERCE GLOSSARY — runs at chapter level before Terms (Commerce ICSE only)
  await runStep('commerce_glossary', 'Glossary', '📚', isCommerce && isChapter && !singleStepMode, async () => {
    const result = stripMarkdownFormatting(await callClaude(buildGlossaryPrompt(name, baseMasterPrompt), 40000));
    saveFile(ch + '/' + ch + '/' + ch + '_Glossary.txt', result);
    logStep(scopeLabel, 'Glossary', '📚', 'done');
  });

  // PREREQ — runs in full mode (chapter only) OR in prereqOnly mode (chapter only)
  await runStep('prereq', 'Pre-requisites', '🔍', isChapter && !isEnglish && !isCommerce && (!singleStepMode || prereqOnly), async () => {"""
assert old_prereq_step in html, "PREREQ step block not found"
html = html.replace(old_prereq_step, new_prereq_step, 1)

# ── 7. Modify TERMS step — Commerce skips single-step gate same as normal ────
#    Terms should run for Commerce too (both chapter and subtopic)
old_terms = "  // TERMS — skipped for English, single-step modes, and GeoHistCivICSE subtopic Case B\n  await runStep('terms', 'Terms and Definition', '📝', !singleStepMode && !isEnglish && !isGeoSubtopicCaseB, async () => {"
new_terms = "  // TERMS — skipped for English, single-step modes, and GeoHistCivICSE subtopic Case B\n  await runStep('terms', 'Terms and Definition', '📝', !singleStepMode && !isEnglish && !isGeoSubtopicCaseB, async () => {"
# No change needed — Commerce is not English, not GeoHistCivICSE, so it runs terms fine.

# ── 8. Modify GLOSSARY step — skip for Commerce (already done in commerce_glossary) ─
old_glossary = "  // GLOSSARY — runs in full mode (chapter only) OR in glossaryOnly mode (chapter only)\n  const hasGlossarySection = !!extractSection(baseMasterPrompt, 'GLOSSARY_CREATION_PROMPT');\n  await runStep('glossary', 'Glossary', '📚', isChapter && !isEnglish && hasGlossarySection && (!singleStepMode || glossaryOnly), async () => {"
new_glossary = "  // GLOSSARY — runs in full mode (chapter only) OR in glossaryOnly mode (chapter only)\n  const hasGlossarySection = !!extractSection(baseMasterPrompt, 'GLOSSARY_CREATION_PROMPT');\n  await runStep('glossary', 'Glossary', '📚', isChapter && !isEnglish && !isCommerce && hasGlossarySection && (!singleStepMode || glossaryOnly), async () => {"
assert old_glossary in html, "GLOSSARY step block not found"
html = html.replace(old_glossary, new_glossary, 1)

# ── 9. Modify OBJECTIVE step to use buildCommerceObjectivePrompt for Commerce ─
old_obj_call = "    const result = await callClaude(buildObjectivePrompt(name, item, masterPrompt, includeRA, loResult), 40000);"
new_obj_call = "    const result = isCommerce\n      ? await callClaude(buildCommerceObjectivePrompt(name, item, masterPrompt, loResult), 40000)\n      : await callClaude(buildObjectivePrompt(name, item, masterPrompt, includeRA, loResult), 40000);"
assert old_obj_call in html, "Objective callClaude line not found"
html = html.replace(old_obj_call, new_obj_call, 1)

# ── 10. Modify SUBJECTIVE step — skip for Commerce ──────────────────────────
old_subj_cond = "  const doSubjectiveHere = doSubjective && !isGeoNano;\n  const shouldRunSubj = isGeoSubtopicCaseB ? doSubjective : doSubjectiveHere;"
new_subj_cond = "  const doSubjectiveHere = doSubjective && !isGeoNano && !isCommerce;\n  const shouldRunSubj = isGeoSubtopicCaseB ? doSubjective : doSubjectiveHere;"
assert old_subj_cond in html, "doSubjectiveHere line not found"
html = html.replace(old_subj_cond, new_subj_cond, 1)

# ── 11. Add buildCommerceObjectivePrompt function after buildObjectivePrompt ─
old_after_obj = "function buildSubjectivePrompt(conceptName, item, masterPrompt, loText) {"
new_after_obj = """function buildCommerceObjectivePrompt(conceptName, item, masterPrompt, loText) {
  const rawSection = extractSection(masterPrompt, 'OBJECTIVE_CREATION_PROMPT') || masterPrompt;
  const section = applyPromptCountEdits(fillPlaceholders(rawSection, conceptName, item, loText));
  const countsText = (state.objMetadata || '').trim();
  const nanoList = item && item.level === 'subtopic' ? (item.nanoConcepts || []).join(', ') : '';

  const metaBlock = `\n\n---\nMETADATA INPUT:\nSubject: ${state.subject}\nCurriculum: ${state.curriculum}\nGrade: ${state.grade}\nChapter Name: ${state.chapterName}\nTopic/Concept Name: ${conceptName}\nTextbook: ${state.textbook}\n${nanoList ? 'Nano Concepts: ' + nanoList + '\\n' : ''}${countsText ? countsText + '\\n' : ''}${chapterScopeNote(item)}\n\n⚠️ STRICT COUNT COMPLIANCE: If counts are specified in METADATA INPUT above, generate EXACTLY those numbers.\n\nReturn ONLY a valid JSON array. No markdown code fences, no explanation, no text outside the array.\nEach element must have: cognitiveLevel, difficultyLevel, questionType, question, options, answers, solution\n- questionType must be one of: SCQ, MSQ, TF, FIB, MTF, OA, CS, DIA, CALC, DEF, DIFF, LIST, APPLY, EVAL\n- options is always an array (can be [] for non-MCQ types)\n- answers is always an array of strings`;

  return section + metaBlock;
}

function buildSubjectivePrompt(conceptName, item, masterPrompt, loText) {"""
assert old_after_obj in html, "buildSubjectivePrompt function start not found"
html = html.replace(old_after_obj, new_after_obj, 1)

# ── 12. Add COMMERCE_KEY to server.py ────────────────────────────────────────
# (handled separately in server.py)

with open('question_bank_generator_4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! All Commerce changes applied to question_bank_generator_4.html")
