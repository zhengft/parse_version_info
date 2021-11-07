function join(items, len, sep,  result, i) {
    if (len >= 1) {
        result = items[1]
        for (i = 2; i <= len; i++) {
            result = sprintf("%s%s%s", result, sep, items[i])
        }
        return result
    }
    return ""
}