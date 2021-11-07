. parse_version_info.sh

main() {
  local func="$1"
  local ret
  shift
  $func "outvar" "$@"
  ret=$?
  printf "%s" "${outvar}"
  return $ret
}

main "$@"
