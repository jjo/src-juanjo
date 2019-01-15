#!/bin/bash
[ $(id -u) -ne 0 ] && echo "Must be root" && exit 1
while test -f /etc/kubernetes/manifests/kube-apiserver.yaml;do
  sleep 5
done
until test -f /etc/kubernetes/manifests/kube-apiserver.yaml;do
  sleep 5
done
set -x
echo "*** PATCHING /etc/kubernetes/manifests/kube-apiserver.yaml for raspi"
sed -i 's/failureThreshold: .*/failureThreshold: 600/;s/initialDelaySeconds: .*/initialDelaySeconds: 300/;s/timeoutSeconds: .*/timeoutSeconds: 10/' /etc/kubernetes/manifests/kube-apiserver.yaml
echo "*** PATCHING /etc/kubernetes/manifests/etcd.yaml for raspi"
sed -i 's/failureThreshold: .*/failureThreshold: 20/;s/initialDelaySeconds: .*/initialDelaySeconds: 120/;s/timeoutSeconds: .*/timeoutSeconds: 120/;s/--election-timeout=.*/--election-timeout=10000/;s/--heartbeat-interval=.*/--heartbeat-interval=1000/' /etc/kubernetes/manifests/etcd.yaml
