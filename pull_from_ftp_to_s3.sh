#!/bin/bash

# Build a diff between s3 bucket and ftp folder
# and then upload files from ftp to s3
#
# The MIT License (MIT)
#
# Copyright (c) 2016-01-20 fomistoklus@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

 # s3cmd utilite is required, but better use `aws s3` instead
set -x

#becase of scipt was used as a rundeck job, I need to use basename with full path
[[ "$(/sbin/pidof -x /home/panda/bin/data/panda-fetch-to-s3.sh )" != $$ ]] && echo "last pid still running" && exit

#store your keys here
source ~/etc/aws/panda_s3_user.cfg

FTP_SERVER="ftp.exmample.com"
mkdir /tmp/panda.$$
WORK_DIR=/tmp/panda.$$
cd $WORK_DIR
S3_PATH="s3://my_bucket/upload_prefix"

FTP_PATH="/OUT"

SYNC_FOLDERS="Folder1
              Folder2
              FolderX"

#create subfolders
mkdir $WORK_DIR/{s3,ftp}


for folder in $SYNC_FOLDERS
do
  #build list of files on S3
  s3cmd ls $S3_PATH/$folder/ | cut -d/ -f5,6 | awk  '{ print var$1 }' var='/' | sort -d > $WORK_DIR/s3/$folder

  #build list of files on FTP
  lftp -e "ls $FTP_PATH/$folder/*.zip; bye" $FTP_SERVER | awk '{ print $9 }' | sort -d | egrep -v 'ARC|issue' | sed 's/\/OUT//g' > $WORK_DIR/ftp/$folder

  #build list of files which should be uploaded
  grep  -Fx -v  -f  $WORK_DIR/s3/$folder $WORK_DIR/ftp/$folder >> $WORK_DIR/to_upload

done

#download file from ftp and upload to s3 bucket
for file in `cat $WORK_DIR/to_upload`
do
  lftp -e "pget -n 3  $FTP_PATH$file; bye" $FTP_SERVER
  echo "$FTP_PATH$file downloaded"
  s3cmd put $(echo $file | cut -d/ -f3) $S3_PATH/$(echo $file | cut -d/ -f2)/ && rm $(echo $file | cut -d/ -f3)
done

rm -rf $WORK_DIR
