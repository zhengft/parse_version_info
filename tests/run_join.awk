BEGIN {
    len = split(input, items, " ")
    result = join(items, len, sep)
    printf(result)
}