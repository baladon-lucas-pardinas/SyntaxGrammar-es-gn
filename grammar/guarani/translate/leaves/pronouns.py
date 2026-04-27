def translate_pronouns(tree, pronounCSV):
    pronounsRes = []
    label = tree["label"]
    agreement = label["AGR"]
    num = agreement.get("NUM") if agreement.get("NUM") else "N"
    per = agreement["PER"]
    word = tree["word"].lower()
    is_polite = str(label.get("POLITE", "0")).lower() == "p"
    found = False

    for row in pronounCSV:
        if (
            row[11] == tree["word"]
            and str(row[4]) == str(per)
            and row[6].lower() == num.lower()
        ):
            pronounsRes.append((row[0], {"AGR": {"INC": row[8]}, "POS": row[9]}))
            found = True

    # Spanish polite pronouns (usted/ustedes) agree syntactically as 3rd person,
    # while the Guarani pronoun lexicon stores them as 2nd person.
    if not found and is_polite and word in {"usted", "ustedes"}:
        for row in pronounCSV:
            if row[11].lower() == word and row[6].lower() == num.lower():
                pronounsRes.append((row[0], {"AGR": {"INC": row[8]}, "POS": row[9]}))
                found = True

    if not found:
        pronounsRes.append((tree["word"], {"AGR": {}, "POS": "B"}))
    return pronounsRes
