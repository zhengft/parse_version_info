function strip(input) {
    sub("^ +", "", input)
    sub(" +$", "", input)
    return input
}