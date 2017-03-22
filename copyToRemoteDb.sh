#!/bin/bash
if [ $# -eq 0 ]
then
  echo "Missing database arg"
  exit 1
fi
mysqldump -u$1 -p$1 $1 | ssh linode mysql -u$1 -p$1 $1
