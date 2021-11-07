function check_compat_le(version_arr, len_version_arr, require_arr, len_require_arr,  i) {
    for (i = 1; i <= len_require_arr; i++) {
        if (require_arr[i] == "") {
            continue
        }
        if (i > len_version_arr) {
            return 1
        }
        if (version_arr[i] < require_arr[i]) {
            return 1
        }
        if (version_arr[i] > require_arr[i]) {
            return 0
        }
    }
    if (i <= len_version_arr) {
        return 0
    }
    return 1
}

function check_compat_ge(version_arr, len_version_arr, require_arr, len_require_arr,  i) {
    for (i = 1; i <= len_require_arr; i++) {
        if (require_arr[i] == "") {
            continue
        }
        if (i > len_version_arr) {
            return 0
        }
        if (version_arr[i] < require_arr[i]) {
            return 0
        }
        if (version_arr[i] > require_arr[i]) {
            return 1
        }
    }
    return 1
}

function check_compat_gt(version_arr, len_version_arr, require_arr, len_require_arr,  i) {
    for (i = 1; i <= len_require_arr; i++) {
        if (require_arr[i] == "") {
            continue
        }
        if (i > len_version_arr) {
            return 0
        }
        if (version_arr[i] > require_arr[i]) {
            return 1
        }
    }
    return 0
}

function check_compat(version_arr, len_version_arr, require,  require_arr, len_require_arr, pos, i) {
    len_require_arr = split(require, require_arr, ".")

    pos = match(require_arr[1], /^>=/)
    if (pos != 0) {
        require_arr[1] = substr(require_arr[1], pos + RLENGTH)
        return check_compat_ge(version_arr, len_version_arr, require_arr, len_require_arr)
    }

    pos = match(require_arr[1], /^>/)
    if (pos != 0) {
        require_arr[1] = substr(require_arr[1], pos + RLENGTH)
        return check_compat_gt(version_arr, len_version_arr, require_arr, len_require_arr)
    }

    pos = match(require_arr[1], /^<=/)
    if (pos != 0) {
        require_arr[1] = substr(require_arr[1], pos + RLENGTH)
        return check_compat_le(version_arr, len_version_arr, require_arr, len_require_arr)
    }

    if (len_version_arr < len_require_arr) {
        return 0
    } else {
        for (i = 1; i <= len_require_arr; i++) {
            if (require_arr[i] == "") {
                continue
            }
            if (require_arr[i] != version_arr[i]) {
                return 0
            }
        }
    }
    return 1
}

BEGIN {
    len_all_require_arr = split(all_require, all_require_arr, ",")

    if (len_all_require_arr > 0)
        compated = 0
    else
        compated = 1

    len_version_arr = split(version, version_arr, ".")

    for (i = 1; i <= len_all_require_arr; i++) {
        all_require_arr[i] = strip(all_require_arr[i])
        one_compated = check_compat(version_arr, len_version_arr, all_require_arr[i])
        if (one_compated == 1) {
            compated = 1
            break
        }
    }

    if (compated == 0) {
        printf("F")
    } else {
        printf("T")
    }
}
