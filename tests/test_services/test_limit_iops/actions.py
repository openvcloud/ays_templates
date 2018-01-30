def init_actions_(service, args):
    """
    this needs to returns an array of actions representing the depencies between actions.
    Looks at ACTION_DEPS in this module for an example of what is expected
    """
    return {
        'test': ['install']
    }


def test(job):
    import sys
    try:
        log = j.logger.get('test')
        log.addHandler(j.logger._LoggerFactory__fileRotateHandler('tests'))
        log.info('Test started')
        service = job.service
        vm_os = service.producers.get('os')[0]
        vm_exe = vm_os.executor.prefab

        log.info('Install fio')
        vm_exe.core.run('apt-get update')
        vm_exe.core.run('echo "Y" | apt-get install fio')

        log.info('Run fio on vdb, iops should be less than maxIOPS')
        vm = service.producers['node'][0]
        disk = vm.producers['disk'][0]
        maxIOPS = disk.model.data.maxIOPS
        readBytesSec = disk.model.data.readBytesSec
        writeBytesSec = disk.model.data.writeBytesSec
        fio_cmd = "fio --ioengine=libaio --group_reporting --filename=/dev/{1} "\
                  "--runtime=30 --readwrite=randrw --size=500M --name=test{0} "\
                  "--output={0}".format('b1', 'vdb')
        vm_exe.core.run(fio_cmd)
        outIops = vm_exe.core.run("cat %s | grep -o 'iops=[0-9]\{1,\}' | cut -d '=' -f 2" % 'b1')
        listIops = outIops[1].split('\n')
        outBytes = vm_exe.core.run("cat %s | grep -o 'bw=[0-9]\{1,\}\.[0-9]\{1,\}' | cut -d '=' -f 2" % 'b1')
        listBytes = outBytes[1].split('\n')
        int_listIops = [int(i) for i in listIops if int(i) > maxIOPS]
        float_listBytes = [float(i) * 1000 for i in listBytes]
        iops = len(int_listIops)
        if iops != 0 or float_listBytes[0] > readBytesSec or float_listBytes[1] > writeBytesSec:
            service.model.data.result = 'FAILED : {} {}'.format('test_limit_iops: disk limit not properly set')
            service.save()
            return

        log.info('Create another data disk (vdc) and set max_iops to 1000')
        vdc = vm.producers['vdc'][0]
        g8client = vdc.producers["g8client"][0]
        config_instance = "{}_{}".format(g8client.aysrepo.name, g8client.model.data.instance)
        client = j.clients.openvcloud.get(instance=config_instance, create=False, die=True, sshkey_path="/root/.ssh/ays_repos_key")
        acc = client.account_get(vdc.model.data.account)
        space = acc.space_get(vdc.model.dbobj.name, vdc.model.data.location)
        machine = space.machines[vm.name]
        disk_id = machine.add_disk(name='disk_c', description='test', size=50, type='D')
        machine.disk_limit_io(disk_id, 0, 4000000, 4000000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000)

        log.info('Run fio on vdc, iops should be less than 1000')
        fio_cmd = "fio --ioengine=libaio --group_reporting --filename=/dev/{1} "\
                  "--runtime=30 --readwrite=randrw --size=500M --name=test{0} "\
                  "--output={0}".format('c1', 'vdc')
        vm_exe.core.run(fio_cmd)
        outIops = vm_exe.core.run("cat %s | grep -o 'iops=[0-9]\{1,\}' | cut -d '=' -f 2" % 'c1')
        listIops = outIops[1].split('\n')
        outBytes = vm_exe.core.run("cat %s | grep -o 'bw=[0-9]\{1,\}\.[0-9]\{1,\}' | cut -d '=' -f 2" % 'c1')
        listBytes = outBytes[1].split('\n')
        int_listIops = [int(i) for i in listIops if int(i) > 1000]
        float_listBytes = [float(i) * 1000 for i in listBytes]
        iops = len(int_listIops)
        if iops != 0 or float_listBytes[0] > 4000000 or float_listBytes[1] > 4000000:
            service.model.data.result = 'FAILED : {} {}'.format('test_limit_iops: disk limit not properly set')
            service.save()
            return

        log.info('Run fio on vdc, iops should be less than 500')
        machine.disk_limit_io(disk_id, 0, 2000000, 2000000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 500)
        fio_cmd = "fio --ioengine=libaio --group_reporting --filename=/dev/{1} "\
                  "--runtime=30 --readwrite=randrw --size=500M --name=test{0} "\
                  "--output={0}".format('c2', 'vdc')
        vm_exe.core.run(fio_cmd)
        outIops = vm_exe.core.run("cat %s | grep -o 'iops=[0-9]\{1,\}' | cut -d '=' -f 2" % 'c2')
        listIops = outIops[1].split('\n')
        outBytes = vm_exe.core.run("cat %s | grep -o 'bw=[0-9]\{1,\}\.[0-9]\{1,\}' | cut -d '=' -f 2" % 'c2')
        listBytes = outBytes[1].split('\n')
        int_listIops = [int(i) for i in listIops if int(i) > 500]
        float_listBytes = [float(i) * 1000 for i in listBytes]
        iops = len(int_listIops)
        if iops != 0 or float_listBytes[0] > 2000000 or float_listBytes[1] > 2000000:
            service.model.data.result = 'FAILED : {} {}'.format('test_limit_iops: disk limit not properly set')
            service.save()
            return
        service.model.data.result = 'OK : {} '.format('test_limit_iops')
    except:
        service.model.data.result = 'ERROR : {} {}'.format('test_limit_iops', str(sys.exc_info()[:2]))
    log.info('Test Ended')
    service.save()
