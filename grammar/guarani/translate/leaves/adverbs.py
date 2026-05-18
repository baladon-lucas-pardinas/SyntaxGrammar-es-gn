def translate_adverbs(tree, adv_csv):
    adv_list = []
    adverb = tree["word"]
    found = False

    for row in adv_csv:
        if row[1].lower() == adverb.lower():
            adv_list.append((row[0], {"AGR": {}}))
            found = True

    if not found:
        adv_list.append((adverb, {"AGR": {}}))

    return adv_list
