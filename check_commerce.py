with open('question_bank_generator_4.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = [
    ('Commerce icse:true', "icse:true,  cbse:false }" in html),
    ('Grade 11 page1', 'value="11">Grade 11' in html),
    ('Grade 12 page1', 'value="12">Grade 12' in html),
    ('getPromptKey Commerce', "COMMERCE_ICSE" in html and "state.subject === 'Commerce'" in html),
    ('COMMERCE_ICSE in PROMPTS', "'COMMERCE_ICSE':" in html),
    ('isCommerce flag', 'const isCommerce = state.subject' in html),
    ('commerce_glossary step', 'commerce_glossary' in html),
    ('prereq skips Commerce', '!isCommerce' in html),
    ('glossary skips Commerce', '!isCommerce && hasGlossarySection' in html),
    ('subjective skips Commerce', '!isGeoNano && !isCommerce' in html),
    ('buildCommerceObjectivePrompt fn', 'function buildCommerceObjectivePrompt' in html),
]
for name, ok in checks:
    print(('OK  ' if ok else 'FAIL'), name)
