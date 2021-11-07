# parse_version_info

awk在split时的类型转换行为。

字符串2大于14，数字2小于14。split前后比对结果不一致。

```bash
awk '
BEGIN {
    one="2"
    two="14"
    split(one, one_arr)
    split(two, two_arr)
    print (one >= two)
    print (one_arr[1] >= two_arr[1])
}
'
```