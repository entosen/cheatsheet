#!/bin/sh

echo "これは STDOUT に出力される1"
echo "これは STDERR に出力される1" >&2
echo "これは STDOUT に出力される2"
echo "これは STDERR に出力される2" >&2
echo "これは STDOUT に出力される3"
echo "これは STDERR に出力される3" >&2

exit $1
