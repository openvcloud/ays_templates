def install(job):
    service = job.service
    vdc = service.producers["vdc"][0]
    g8client = vdc.producers["g8client"][0]
    config_instance = "{}_{}".format(g8client.aysrepo.name, g8client.model.data.instance)
    cl = j.clients.openvcloud.get(instance=config_instance, create=False, die=True, sshkey_path="/root/.ssh/ays_repos_key")
    acc = cl.account_get(vdc.model.data.account)
    # if space does not exist, it will create it
    space = acc.space_get(vdc.model.dbobj.name, vdc.model.data.location)

    data = service.model.data
    for location in cl.locations:
        if location['name'] == space.model['location']:
            gid = location['gid']

    space.add_external_network(name=data.name,
                               subnet=data.publicSubnetCIDR,
                               gateway=data.gatewayIPAddress,
                               startip=data.startIPAddress,
                               endip=data.endIPAddress,
                               gid=gid,
                               vlan=data.vLANID)
