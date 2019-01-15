ARCH=arm
VERSION=${1:?missing version}
(set -x
wget -O kubernetes-client-linux-${ARCH}.${VERSION}.tar.gz --no-clobber https://dl.k8s.io/${VERSION}/kubernetes-client-linux-${ARCH}.tar.gz
wget -O kubernetes-node-linux-${ARCH}.${VERSION}.tar.gz --no-clobber https://dl.k8s.io/${VERSION}/kubernetes-node-linux-${ARCH}.tar.gz
wget -O kubernetes-server-linux-${ARCH}.${VERSION}.tar.gz --no-clobber https://dl.k8s.io/${VERSION}/kubernetes-server-linux-${ARCH}.tar.gz
)

echo "Extract with:"
echo sudo tar -C / -zxvf kubernetes-node-linux-${ARCH}.${VERSION}.tar.gz --xform='s,kubernetes/node,/usr,' --show-transformed kubernetes/node/bin/kubectl
echo sudo tar -C / -zxvf kubernetes-node-linux-${ARCH}.${VERSION}.tar.gz --xform='s,kubernetes/node,/usr,' --show-transformed kubernetes/node/bin/kubeadm
echo sudo tar -C / -zxvf kubernetes-node-linux-${ARCH}.${VERSION}.tar.gz --xform='s,kubernetes/node,/usr,' --show-transformed kubernetes/node/bin/kubelet
