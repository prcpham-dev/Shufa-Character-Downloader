def readFile():
    result = []
    with open("shufa.txt", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Skip when file is empty
    if not lines:
        return result

    # Author name
    result.append(lines[0])

    # Character extract. Unique only
    seen = set()
    for line in lines[1:]:
        for ch in line:
            if ch not in seen:
                seen.add(ch)
                result.append(ch)

    return result


if __name__ == "__main__":
    extracted = readFile()
    print(extracted)
