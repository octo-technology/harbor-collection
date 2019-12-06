FROM aquasec/kube-bench:0.2.1

WORKDIR /opt/kube-bench/

RUN apk --no-cache add curl bash python py-pip jq

# A remplacer par minio-client ?
RUN pip install awscli

COPY entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]
