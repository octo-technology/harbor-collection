{
  "id": "2",
  "version": "1.13",
  "text": "Worker Node Security Configuration",
  "node_type": "node",
  "tests": [
    {
      "section": "2.1",
      "pass": 4,
      "fail": 8,
      "warn": 1,
      "info": 1,
      "desc": "Kubelet",
      "results": [
        {
          "test_number": "2.1.1",
          "test_desc": "Ensure that the --anonymous-auth argument is set to false (Scored)",
          "audit": "/bin/ps -fC kubelet",
          "AuditConfig": "/bin/cat /var/lib/kubelet/kubeconfig",
          "type": "",
          "remediation": "If using a Kubelet config file, edit the file to set authentication: anonymous: enabled to\nfalse .\nIf using executable arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_SYSTEM_PODS_ARGS variable.\n--anonymous-auth=false\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "If using a Kubelet config file, edit the file to set authentication: anonymous: enabled to\nfalse .\nIf using executable arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_SYSTEM_PODS_ARGS variable.\n--anonymous-auth=false\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "FAIL",
          "actual_value": "",
          "scored": true,
          "expected_result": ""
        },
        {
          "test_number": "2.1.2",
          "test_desc": "Ensure that the --authorization-mode argument is not set to AlwaysAllow (Scored)",
          "audit": "/bin/ps -fC kubelet",
          "AuditConfig": "/bin/cat /var/lib/kubelet/kubeconfig",
          "type": "",
          "remediation": "If using a Kubelet config file, edit the file to set authorization: mode to Webhook.\nIf using executable arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_AUTHZ_ARGS variable.\n--authorization-mode=Webhook\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "If using a Kubelet config file, edit the file to set authorization: mode to Webhook.\nIf using executable arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_AUTHZ_ARGS variable.\n--authorization-mode=Webhook\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "FAIL",
          "actual_value": "",
          "scored": true,
          "expected_result": ""
        },
        {
          "test_number": "2.1.3",
          "test_desc": "Ensure that the --client-ca-file argument is set as appropriate (Scored)",
          "audit": "/bin/ps -fC kubelet",
          "AuditConfig": "/bin/cat /var/lib/kubelet/kubeconfig",
          "type": "",
          "remediation": "If using a Kubelet config file, edit the file to set authentication: x509: clientCAFile to\nthe location of the client CA file.\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_AUTHZ_ARGS variable.\n--client-ca-file=<path/to/client-ca-file>\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "If using a Kubelet config file, edit the file to set authentication: x509: clientCAFile to\nthe location of the client CA file.\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_AUTHZ_ARGS variable.\n--client-ca-file=<path/to/client-ca-file>\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "FAIL",
          "actual_value": "",
          "scored": true,
          "expected_result": ""
        },
        {
          "test_number": "2.1.4",
          "test_desc": "Ensure that the --read-only-port argument is set to 0 (Scored)",
          "audit": "/bin/ps -fC kubelet",
          "AuditConfig": "/bin/cat /var/lib/kubelet/kubeconfig",
          "type": "",
          "remediation": "If using a Kubelet config file, edit the file to set readOnlyPort to 0 .\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_SYSTEM_PODS_ARGS variable.\n--read-only-port=0\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "If using a Kubelet config file, edit the file to set readOnlyPort to 0 .\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_SYSTEM_PODS_ARGS variable.\n--read-only-port=0\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "FAIL",
          "actual_value": "",
          "scored": true,
          "expected_result": ""
        },
        {
          "test_number": "2.1.5",
          "test_desc": "Ensure that the --streaming-connection-idle-timeout argument is not set to 0 (Scored)",
          "audit": "/bin/ps -fC kubelet",
          "AuditConfig": "/bin/cat /var/lib/kubelet/kubeconfig",
          "type": "",
          "remediation": "If using a Kubelet config file, edit the file to set streamingConnectionIdleTimeout to a\nvalue other than 0.\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_SYSTEM_PODS_ARGS variable.\n--streaming-connection-idle-timeout=5m\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "If using a Kubelet config file, edit the file to set streamingConnectionIdleTimeout to a\nvalue other than 0.\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_SYSTEM_PODS_ARGS variable.\n--streaming-connection-idle-timeout=5m\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "PASS",
          "actual_value": "UID          PID    PPID  C STIME TTY          TIME CMD\nroot        1429       1  3 09:40 ?        00:00:44 /home/kubernetes/bin/kubelet --v=2 --cloud-provider=gce --experimental-check-node-capabilities-before-mount=true --experimental-mounter-path=/home/kubernetes/containerized_mounter/mounter --cert-dir=/var/lib/kubelet/pki/ --cni-bin-dir=/home/kubernetes/bin --kubeconfig=/var/lib/kubelet/kubeconfig --experimental-kernel-memcg-notification=true --max-pods=110 --non-masquerade-cidr=0.0.0.0/0 --network-plugin=kubenet --node-labels=beta.kubernetes.io/fluentd-ds-ready=true,cloud.google.com/gke-nodepool=default-pool,cloud.google.com/gke-os-distribution=cos --volume-plugin-dir=/home/kubernetes/flexvolume --bootstrap-kubeconfig=/var/lib/kubelet/bootstrap-kubeconfig --node-status-max-images=25 --registry-qps=10 --registry-burst=20 --config /home/kubernetes/kubelet-config.yaml --pod-sysctls=net.core.somaxconn=1024,net.ipv4.conf.all.accept_redirects=0,net.ipv4.conf.all.forwarding=1,net.ipv4.conf.all.route_localnet=1,net.ipv4.conf.default.forwarding=1,net.ipv4.ip_forward=1,net.ipv4.tcp_fin_timeout=60,net.ipv4.tcp_keepalive_intvl=75,net.ipv4.tcp_keepalive_probes=9,net.ipv4.tcp_keepalive_time=7200,net.ipv4.tcp_max_syn_backlog=128,net.ipv4.tcp_max_tw_buckets=16384,net.ipv4.tcp_syn_retries=6,net.ipv4.tcp_tw_reuse=0,net.netfilter.nf_conntrack_generic_timeout=600,net.netfilter.nf_conntrack_tcp_timeout_close_wait=3600,net.netfilter.nf_conntrack_tcp_timeout_established=86400\n",
          "scored": true,
          "expected_result": "'--streaming-connection-idle-timeout' is present OR '--streaming-connection-idle-timeout' is not present"
        },
        {
          "test_number": "2.1.6",
          "test_desc": "Ensure that the --protect-kernel-defaults argument is set to true (Scored)",
          "audit": "/bin/ps -fC kubelet",
          "AuditConfig": "/bin/cat /var/lib/kubelet/kubeconfig",
          "type": "",
          "remediation": "If using a Kubelet config file, edit the file to set protectKernelDefaults: true .\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_SYSTEM_PODS_ARGS variable.\n--protect-kernel-defaults=true\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "If using a Kubelet config file, edit the file to set protectKernelDefaults: true .\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_SYSTEM_PODS_ARGS variable.\n--protect-kernel-defaults=true\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "FAIL",
          "actual_value": "",
          "scored": true,
          "expected_result": ""
        },
        {
          "test_number": "2.1.7",
          "test_desc": "Ensure that the --make-iptables-util-chains argument is set to true (Scored)",
          "audit": "/bin/ps -fC kubelet",
          "AuditConfig": "/bin/cat /var/lib/kubelet/kubeconfig",
          "type": "",
          "remediation": "If using a Kubelet config file, edit the file to set makeIPTablesUtilChains: true .\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nremove the --make-iptables-util-chains argument from the\nKUBELET_SYSTEM_PODS_ARGS variable.\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "If using a Kubelet config file, edit the file to set makeIPTablesUtilChains: true .\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nremove the --make-iptables-util-chains argument from the\nKUBELET_SYSTEM_PODS_ARGS variable.\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "PASS",
          "actual_value": "UID          PID    PPID  C STIME TTY          TIME CMD\nroot        1429       1  3 09:40 ?        00:00:44 /home/kubernetes/bin/kubelet --v=2 --cloud-provider=gce --experimental-check-node-capabilities-before-mount=true --experimental-mounter-path=/home/kubernetes/containerized_mounter/mounter --cert-dir=/var/lib/kubelet/pki/ --cni-bin-dir=/home/kubernetes/bin --kubeconfig=/var/lib/kubelet/kubeconfig --experimental-kernel-memcg-notification=true --max-pods=110 --non-masquerade-cidr=0.0.0.0/0 --network-plugin=kubenet --node-labels=beta.kubernetes.io/fluentd-ds-ready=true,cloud.google.com/gke-nodepool=default-pool,cloud.google.com/gke-os-distribution=cos --volume-plugin-dir=/home/kubernetes/flexvolume --bootstrap-kubeconfig=/var/lib/kubelet/bootstrap-kubeconfig --node-status-max-images=25 --registry-qps=10 --registry-burst=20 --config /home/kubernetes/kubelet-config.yaml --pod-sysctls=net.core.somaxconn=1024,net.ipv4.conf.all.accept_redirects=0,net.ipv4.conf.all.forwarding=1,net.ipv4.conf.all.route_localnet=1,net.ipv4.conf.default.forwarding=1,net.ipv4.ip_forward=1,net.ipv4.tcp_fin_timeout=60,net.ipv4.tcp_keepalive_intvl=75,net.ipv4.tcp_keepalive_probes=9,net.ipv4.tcp_keepalive_time=7200,net.ipv4.tcp_max_syn_backlog=128,net.ipv4.tcp_max_tw_buckets=16384,net.ipv4.tcp_syn_retries=6,net.ipv4.tcp_tw_reuse=0,net.netfilter.nf_conntrack_generic_timeout=600,net.netfilter.nf_conntrack_tcp_timeout_close_wait=3600,net.netfilter.nf_conntrack_tcp_timeout_established=86400\n",
          "scored": true,
          "expected_result": "'--make-iptables-util-chains' is present OR '--make-iptables-util-chains' is not present"
        },
        {
          "test_number": "2.1.8",
          "test_desc": "Ensure that the --hostname-override argument is not set (Scored)",
          "audit": "/bin/ps -fC kubelet ",
          "AuditConfig": "",
          "type": "",
          "remediation": "Edit the kubelet service file /etc/systemd/system/kubelet.service\non each worker node and remove the --hostname-override argument from the\nKUBELET_SYSTEM_PODS_ARGS variable.\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "Edit the kubelet service file /etc/systemd/system/kubelet.service\non each worker node and remove the --hostname-override argument from the\nKUBELET_SYSTEM_PODS_ARGS variable.\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "PASS",
          "actual_value": "UID          PID    PPID  C STIME TTY          TIME CMD\nroot        1429       1  3 09:40 ?        00:00:44 /home/kubernetes/bin/kubelet --v=2 --cloud-provider=gce --experimental-check-node-capabilities-before-mount=true --experimental-mounter-path=/home/kubernetes/containerized_mounter/mounter --cert-dir=/var/lib/kubelet/pki/ --cni-bin-dir=/home/kubernetes/bin --kubeconfig=/var/lib/kubelet/kubeconfig --experimental-kernel-memcg-notification=true --max-pods=110 --non-masquerade-cidr=0.0.0.0/0 --network-plugin=kubenet --node-labels=beta.kubernetes.io/fluentd-ds-ready=true,cloud.google.com/gke-nodepool=default-pool,cloud.google.com/gke-os-distribution=cos --volume-plugin-dir=/home/kubernetes/flexvolume --bootstrap-kubeconfig=/var/lib/kubelet/bootstrap-kubeconfig --node-status-max-images=25 --registry-qps=10 --registry-burst=20 --config /home/kubernetes/kubelet-config.yaml --pod-sysctls=net.core.somaxconn=1024,net.ipv4.conf.all.accept_redirects=0,net.ipv4.conf.all.forwarding=1,net.ipv4.conf.all.route_localnet=1,net.ipv4.conf.default.forwarding=1,net.ipv4.ip_forward=1,net.ipv4.tcp_fin_timeout=60,net.ipv4.tcp_keepalive_intvl=75,net.ipv4.tcp_keepalive_probes=9,net.ipv4.tcp_keepalive_time=7200,net.ipv4.tcp_max_syn_backlog=128,net.ipv4.tcp_max_tw_buckets=16384,net.ipv4.tcp_syn_retries=6,net.ipv4.tcp_tw_reuse=0,net.netfilter.nf_conntrack_generic_timeout=600,net.netfilter.nf_conntrack_tcp_timeout_close_wait=3600,net.netfilter.nf_conntrack_tcp_timeout_established=86400\n",
          "scored": true,
          "expected_result": "'--hostname-override' is not present"
        },
        {
          "test_number": "2.1.9",
          "test_desc": "Ensure that the --event-qps argument is set to 0 (Scored)",
          "audit": "/bin/ps -fC kubelet",
          "AuditConfig": "/bin/cat /var/lib/kubelet/kubeconfig",
          "type": "",
          "remediation": "If using a Kubelet config file, edit the file to set eventRecordQPS: 0 .\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_SYSTEM_PODS_ARGS variable.\n--event-qps=0\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "If using a Kubelet config file, edit the file to set eventRecordQPS: 0 .\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameter in KUBELET_SYSTEM_PODS_ARGS variable.\n--event-qps=0\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "FAIL",
          "actual_value": "",
          "scored": true,
          "expected_result": ""
        },
        {
          "test_number": "2.1.10",
          "test_desc": "Ensure that the --tls-cert-file and --tls-private-key-file arguments are set as appropriate (Scored)",
          "audit": "/bin/ps -fC kubelet",
          "AuditConfig": "/bin/cat /var/lib/kubelet/kubeconfig",
          "type": "",
          "remediation": "If using a Kubelet config file, edit the file to set tlsCertFile to the location of the certificate\nfile to use to identify this Kubelet, and tlsPrivateKeyFile to the location of the\ncorresponding private key file.\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameters in KUBELET_CERTIFICATE_ARGS variable.\n--tls-cert-file=<path/to/tls-certificate-file>\nfile=<path/to/tls-key-file>\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "If using a Kubelet config file, edit the file to set tlsCertFile to the location of the certificate\nfile to use to identify this Kubelet, and tlsPrivateKeyFile to the location of the\ncorresponding private key file.\nIf using command line arguments, edit the kubelet service file\n/etc/systemd/system/kubelet.service on each worker node and\nset the below parameters in KUBELET_CERTIFICATE_ARGS variable.\n--tls-cert-file=<path/to/tls-certificate-file>\nfile=<path/to/tls-key-file>\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "FAIL",
          "actual_value": "",
          "scored": true,
          "expected_result": ""
        },
        {
          "test_number": "2.1.11",
          "test_desc": "[DEPRECATED] Ensure that the --cadvisor-port argument is set to 0",
          "audit": "/bin/ps -fC kubelet ",
          "AuditConfig": "",
          "type": "skip",
          "remediation": "Edit the kubelet service file /etc/systemd/system/kubelet.service\non each worker node and set the below parameter in KUBELET_CADVISOR_ARGS variable.\n--cadvisor-port=0\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "Edit the kubelet service file /etc/systemd/system/kubelet.service\non each worker node and set the below parameter in KUBELET_CADVISOR_ARGS variable.\n--cadvisor-port=0\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "INFO",
          "actual_value": "",
          "scored": false,
          "expected_result": ""
        },
        {
          "test_number": "2.1.12",
          "test_desc": "Ensure that the --rotate-certificates argument is not set to false (Scored)",
          "audit": "/bin/ps -fC kubelet",
          "AuditConfig": "/bin/cat /var/lib/kubelet/kubeconfig",
          "type": "",
          "remediation": "If using a Kubelet config file, edit the file to add the line rotateCertificates: true.\nIf using command line arguments, edit the kubelet service file /etc/systemd/system/kubelet.service\non each worker node and add --rotate-certificates=true argument to the KUBELET_CERTIFICATE_ARGS variable.\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "If using a Kubelet config file, edit the file to add the line rotateCertificates: true.\nIf using command line arguments, edit the kubelet service file /etc/systemd/system/kubelet.service\non each worker node and add --rotate-certificates=true argument to the KUBELET_CERTIFICATE_ARGS variable.\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "PASS",
          "actual_value": "UID          PID    PPID  C STIME TTY          TIME CMD\nroot        1429       1  3 09:40 ?        00:00:44 /home/kubernetes/bin/kubelet --v=2 --cloud-provider=gce --experimental-check-node-capabilities-before-mount=true --experimental-mounter-path=/home/kubernetes/containerized_mounter/mounter --cert-dir=/var/lib/kubelet/pki/ --cni-bin-dir=/home/kubernetes/bin --kubeconfig=/var/lib/kubelet/kubeconfig --experimental-kernel-memcg-notification=true --max-pods=110 --non-masquerade-cidr=0.0.0.0/0 --network-plugin=kubenet --node-labels=beta.kubernetes.io/fluentd-ds-ready=true,cloud.google.com/gke-nodepool=default-pool,cloud.google.com/gke-os-distribution=cos --volume-plugin-dir=/home/kubernetes/flexvolume --bootstrap-kubeconfig=/var/lib/kubelet/bootstrap-kubeconfig --node-status-max-images=25 --registry-qps=10 --registry-burst=20 --config /home/kubernetes/kubelet-config.yaml --pod-sysctls=net.core.somaxconn=1024,net.ipv4.conf.all.accept_redirects=0,net.ipv4.conf.all.forwarding=1,net.ipv4.conf.all.route_localnet=1,net.ipv4.conf.default.forwarding=1,net.ipv4.ip_forward=1,net.ipv4.tcp_fin_timeout=60,net.ipv4.tcp_keepalive_intvl=75,net.ipv4.tcp_keepalive_probes=9,net.ipv4.tcp_keepalive_time=7200,net.ipv4.tcp_max_syn_backlog=128,net.ipv4.tcp_max_tw_buckets=16384,net.ipv4.tcp_syn_retries=6,net.ipv4.tcp_tw_reuse=0,net.netfilter.nf_conntrack_generic_timeout=600,net.netfilter.nf_conntrack_tcp_timeout_close_wait=3600,net.netfilter.nf_conntrack_tcp_timeout_established=86400\n",
          "scored": true,
          "expected_result": "'--rotate-certificates' is present OR '--rotate-certificates' is not present"
        },
        {
          "test_number": "2.1.13",
          "test_desc": "Ensure that the RotateKubeletServerCertificate argument is set to true (Scored)",
          "audit": "/bin/ps -fC kubelet",
          "AuditConfig": "/bin/cat /var/lib/kubelet/kubeconfig",
          "type": "",
          "remediation": "Edit the kubelet service file /etc/systemd/system/kubelet.service\non each worker node and set the below parameter in KUBELET_CERTIFICATE_ARGS variable.\n--feature-gates=RotateKubeletServerCertificate=true\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n",
          "test_info": [
            "Edit the kubelet service file /etc/systemd/system/kubelet.service\non each worker node and set the below parameter in KUBELET_CERTIFICATE_ARGS variable.\n--feature-gates=RotateKubeletServerCertificate=true\nBased on your system, restart the kubelet service. For example:\nsystemctl daemon-reload\nsystemctl restart kubelet.service\n"
          ],
          "status": "FAIL",
          "actual_value": "",
          "scored": true,
          "expected_result": ""
        },
        {
          "test_number": "2.1.14",
          "test_desc": "Ensure that the Kubelet only makes use of Strong Cryptographic Ciphers (Not Scored)",
          "audit": "/bin/ps -fC kubelet",
          "AuditConfig": "/bin/cat /var/lib/kubelet/kubeconfig",
          "type": "",
          "remediation": "If using a Kubelet config file, edit the file to set TLSCipherSuites: to TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256\nIf using executable arguments, edit the kubelet service file /etc/systemd/system/kubelet.service on each worker node and set the below parameter.\n--tls-cipher-suites=TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256\n",
          "test_info": [
            "If using a Kubelet config file, edit the file to set TLSCipherSuites: to TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256\nIf using executable arguments, edit the kubelet service file /etc/systemd/system/kubelet.service on each worker node and set the below parameter.\n--tls-cipher-suites=TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256\n"
          ],
          "status": "WARN",
          "actual_value": "",
          "scored": false,
          "expected_result": ""
        }
      ]
    },
    {
      "section": "2.2",
      "pass": 8,
      "fail": 2,
      "warn": 0,
      "info": 0,
      "desc": "Configuration Files",
      "results": [
        {
          "test_number": "2.2.1",
          "test_desc": "Ensure that the kubelet.conf file permissions are set to 644 or more restrictive (Scored)",
          "audit": "/bin/sh -c 'if test -e /var/lib/kubelet/kubeconfig; then stat -c %a /var/lib/kubelet/kubeconfig; fi' ",
          "AuditConfig": "",
          "type": "",
          "remediation": "Run the below command (based on the file location on your system) on the each worker\nnode. For example,\nchmod 644 /var/lib/kubelet/kubeconfig\n",
          "test_info": [
            "Run the below command (based on the file location on your system) on the each worker\nnode. For example,\nchmod 644 /var/lib/kubelet/kubeconfig\n"
          ],
          "status": "PASS",
          "actual_value": "600\n",
          "scored": true,
          "expected_result": "'644' is present OR '640' is present OR '600' is equal to '600'"
        },
        {
          "test_number": "2.2.2",
          "test_desc": "Ensure that the kubelet.conf file ownership is set to root:root (Scored)",
          "audit": "/bin/sh -c 'if test -e /var/lib/kubelet/kubeconfig; then stat -c %U:%G /var/lib/kubelet/kubeconfig; fi' ",
          "AuditConfig": "",
          "type": "",
          "remediation": "Run the below command (based on the file location on your system) on the each worker\nnode. For example,\nchown root:root /var/lib/kubelet/kubeconfig\n",
          "test_info": [
            "Run the below command (based on the file location on your system) on the each worker\nnode. For example,\nchown root:root /var/lib/kubelet/kubeconfig\n"
          ],
          "status": "PASS",
          "actual_value": "root:root\n",
          "scored": true,
          "expected_result": "'root:root' is equal to 'root:root'"
        },
        {
          "test_number": "2.2.3",
          "test_desc": "Ensure that the kubelet service file permissions are set to 644 or more restrictive (Scored)",
          "audit": "/bin/sh -c 'if test -e /etc/systemd/system/kubelet.service; then stat -c %a /etc/systemd/system/kubelet.service; fi' ",
          "AuditConfig": "",
          "type": "",
          "remediation": "Run the below command (based on the file location on your system) on the each worker\nnode. For example,\nchmod 755 /etc/systemd/system/kubelet.service\n",
          "test_info": [
            "Run the below command (based on the file location on your system) on the each worker\nnode. For example,\nchmod 755 /etc/systemd/system/kubelet.service\n"
          ],
          "status": "PASS",
          "actual_value": "644\n",
          "scored": true,
          "expected_result": "'644' is equal to '644' OR '640' is present OR '600' is present"
        },
        {
          "test_number": "2.2.4",
          "test_desc": "Ensure that the kubelet service file ownership is set to root:root (Scored)",
          "audit": "/bin/sh -c 'if test -e /etc/systemd/system/kubelet.service; then stat -c %U:%G /etc/systemd/system/kubelet.service; fi' ",
          "AuditConfig": "",
          "type": "",
          "remediation": "Run the below command (based on the file location on your system) on the each worker\nnode. For example,\nchown root:root /etc/systemd/system/kubelet.service\n",
          "test_info": [
            "Run the below command (based on the file location on your system) on the each worker\nnode. For example,\nchown root:root /etc/systemd/system/kubelet.service\n"
          ],
          "status": "PASS",
          "actual_value": "root:root\n",
          "scored": true,
          "expected_result": "'root:root' is present"
        },
        {
          "test_number": "2.2.5",
          "test_desc": "Ensure that the proxy kubeconfig file permissions are set to 644 or more restrictive (Scored)",
          "audit": "/bin/sh -c 'if test -e /var/lib/kubelet/kubeconfig; then stat -c %a /var/lib/kubelet/kubeconfig; fi' ",
          "AuditConfig": "",
          "type": "",
          "remediation": "Run the below command (based on the file location on your system) on the each worker\nnode. For example,\nchmod 644 /var/lib/kubelet/kubeconfig\n",
          "test_info": [
            "Run the below command (based on the file location on your system) on the each worker\nnode. For example,\nchmod 644 /var/lib/kubelet/kubeconfig\n"
          ],
          "status": "PASS",
          "actual_value": "600\n",
          "scored": true,
          "expected_result": "'644' is present OR '640' is present OR '600' is equal to '600'"
        },
        {
          "test_number": "2.2.6",
          "test_desc": "Ensure that the proxy kubeconfig file ownership is set to root:root (Scored)",
          "audit": "/bin/sh -c 'if test -e /var/lib/kubelet/kubeconfig; then stat -c %U:%G /var/lib/kubelet/kubeconfig; fi' ",
          "AuditConfig": "",
          "type": "",
          "remediation": "Run the below command (based on the file location on your system) on the each worker\nnode. For example,\nchown root:root /var/lib/kubelet/kubeconfig\n",
          "test_info": [
            "Run the below command (based on the file location on your system) on the each worker\nnode. For example,\nchown root:root /var/lib/kubelet/kubeconfig\n"
          ],
          "status": "PASS",
          "actual_value": "root:root\n",
          "scored": true,
          "expected_result": "'root:root' is present"
        },
        {
          "test_number": "2.2.7",
          "test_desc": "Ensure that the certificate authorities file permissions are set to 644 or more restrictive (Scored)",
          "audit": "/bin/sh -c 'if test -e /etc/kubernetes/pki/ca.crt; then stat -c %a /etc/kubernetes/pki/ca.crt; fi'",
          "AuditConfig": "",
          "type": "",
          "remediation": "Run the following command to modify the file permissions of the --client-ca-file\nchmod 644 <filename>\n",
          "test_info": [
            "Run the following command to modify the file permissions of the --client-ca-file\nchmod 644 <filename>\n"
          ],
          "status": "FAIL",
          "actual_value": "",
          "scored": true,
          "expected_result": ""
        },
        {
          "test_number": "2.2.8",
          "test_desc": "Ensure that the client certificate authorities file ownership is set to root:root (Scored)",
          "audit": "/bin/sh -c 'if test -e /etc/kubernetes/pki/ca.crt; then stat -c %U:%G /etc/kubernetes/pki/ca.crt; fi' ",
          "AuditConfig": "",
          "type": "",
          "remediation": "Run the following command to modify the ownership of the --client-ca-file .\nchown root:root <filename>\n",
          "test_info": [
            "Run the following command to modify the ownership of the --client-ca-file .\nchown root:root <filename>\n"
          ],
          "status": "FAIL",
          "actual_value": "",
          "scored": true,
          "expected_result": ""
        },
        {
          "test_number": "2.2.9",
          "test_desc": "Ensure that the kubelet configuration file ownership is set to root:root (Scored)",
          "audit": "/bin/sh -c 'if test -e /var/lib/kubelet/kubeconfig; then stat -c %U:%G /var/lib/kubelet/kubeconfig; fi' ",
          "AuditConfig": "",
          "type": "",
          "remediation": "Run the following command (using the config file location identied in the Audit step)\nchown root:root /var/lib/kubelet/kubeconfig\n",
          "test_info": [
            "Run the following command (using the config file location identied in the Audit step)\nchown root:root /var/lib/kubelet/kubeconfig\n"
          ],
          "status": "PASS",
          "actual_value": "root:root\n",
          "scored": true,
          "expected_result": "'root:root' is present"
        },
        {
          "test_number": "2.2.10",
          "test_desc": "Ensure that the kubelet configuration file has permissions set to 644 or more restrictive (Scored)",
          "audit": "/bin/sh -c 'if test -e /var/lib/kubelet/kubeconfig; then stat -c %a /var/lib/kubelet/kubeconfig; fi' ",
          "AuditConfig": "",
          "type": "",
          "remediation": "Run the following command (using the config file location identied in the Audit step)\nchmod 644 /var/lib/kubelet/kubeconfig\n",
          "test_info": [
            "Run the following command (using the config file location identied in the Audit step)\nchmod 644 /var/lib/kubelet/kubeconfig\n"
          ],
          "status": "PASS",
          "actual_value": "600\n",
          "scored": true,
          "expected_result": "'644' is present OR '640' is present OR '600' is equal to '600'"
        }
      ]
    }
  ],
  "total_pass": 12,
  "total_fail": 10,
  "total_warn": 1,
  "total_info": 1
}
