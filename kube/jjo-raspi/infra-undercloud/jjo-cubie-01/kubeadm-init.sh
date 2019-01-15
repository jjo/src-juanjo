sudo ./kubeadm-init.raspi-slow.sh &
sudo kubeadm init --ignore-preflight-errors Swap --token-ttl=0 --pod-network-cidr 10.244.0.0/16 --apiserver-cert-extra-sans jjo-raspi.kube.jjo.com.ar "$@"
