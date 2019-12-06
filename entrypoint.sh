#!/bin/bash -e

OUTPUTFILE=""
[ ! -z "$REPORT_FILENAME" ] && OUTPUTFILE="--outputfile ${REPORT_FILENAME}"
[ -z "$KUBERNETES_VERSION" ] && "echo KUBERNETES_VERSION is not set" && exit 1
[ -z "$S3_BUCKET_NAME" ] && "echo S3_BUCKET_NAME is not set" && exit 1

kube-bench --version ${KUBERNETES_VERSION} --json --logtostderr ${OUTPUTFILE}

[ -z "$REPORT_FILENAME" ] && exit 0

NODE_TYPE=$(cat ${REPORT_FILENAME} | jq -r .node_type)
aws s3 cp $REPORT_FILENAME s3://${S3_BUCKET_NAME}/$(date +%Y-%m-%d)/$NODE_TYPE/$REPORT_FILENAME
