. parse_version_info.sh

main() {
  local func="$1"
  shift
  $func "$@"
}

main "$@"
