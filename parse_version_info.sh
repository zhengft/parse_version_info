#!/bin/bash

get_require_packages() {
    local _outvar="$1"
    local _version_info_path="$2"
    local _packages

    if [ ! -f "${_version_info_path}" ]; then
        eval "${_outvar}=\"\""
        return 1
    fi

    _packages=$(awk '
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

        BEGIN {
            len_packages = 0
        }
        /^require_package_.+=/ {
            split($0, line_tokens, "=")
            len_require_tokens = split(line_tokens[1], require_tokens, "_")
            len_package_names = 0
            for (i = 3; i <= len_require_tokens; i++) {
                len_package_names++
                package_names[len_package_names] = require_tokens[i]
            }
            package_name = join(package_names, len_package_names, "_")

            len_packages += 1
            packages[len_packages] = package_name
            
        }
        END {
            if (len_packages >= 1) {
                printf("%s", packages[1])
                for (i = 2; i <= len_packages; i++) {
                    printf(" %s", packages[i])
                }
            }
        }
    ' "${_version_info_path}")
    eval "${_outvar}=\"${_packages}\""
}

get_require_package_info() {
    local _outvar="$1"
    local _version_info_path="$2"
    local _pkg_name="$3"
    local _require_pkg_name

    if [ ! -f "${_version_info_path}" ]; then
        eval "${_outvar}=\"\""
        return 1
    fi

    _require_pkg_name="require_package_${_pkg_name}"
    # Init require_pkg_name variable.
    eval "${_require_pkg_name}=\"\""

    . "${_version_info_path}"
    eval "${_outvar}=\"\${${_require_pkg_name}}\""
}

get_package_version() {
    local _outvar="$1"
    local _version_info_path="$2"
    local Version=""

    if [ ! -f "${_version_info_path}" ]; then
        eval "${_outvar}=\"\""
        return 1
    fi

    . "${_version_info_path}"
    eval "${_outvar}=\"${Version}\""
}

check_version_compat() {
    local version="$1"
    local require="$2"
    local result

    if [ "${version}" = "${require}" ]; then
        return 0
    fi

    result=$(awk -v version="${version}" -v all_require="${require}" '
        function check_compat(version_arr, len_version_arr, require) {
            len_require_arr = split(require, require_arr, ".")

            if (len_version_arr < len_require_arr) {
                return 0
            } else {
                for (i = 1; i <= len_require_arr; i++) {
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
    ')
    if [ "${result}" = "T" ]; then
        return 0
    fi

    return 1
}