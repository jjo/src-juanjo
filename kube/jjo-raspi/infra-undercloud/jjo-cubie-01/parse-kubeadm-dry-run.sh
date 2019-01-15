sed -rn '/^.dryrun. Attached.object/,/^\S+/p' kubeadm-init.dry-run.out |sed -r '/Would/d;s/.*Attached.*/        ---/'|sed -rn 's/^ {8}//p' |less
