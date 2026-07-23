from workflow.gates import IT_PORTS


def test_modern_infra_ports_present():
    for p in (111, 623, 2049, 2375, 5060, 6443, 10250):  # rpcbind,IPMI,NFS,Docker,SIP,k8s,kubelet
        assert p in IT_PORTS, f"port {p} missing from IT_PORTS"
