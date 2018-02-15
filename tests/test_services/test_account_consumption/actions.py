def init_actions_(service, args):
    """
    This needs to return an array of actions representing the depencies between actions.
    Looks at ACTION_DEPS in this module for an example of what is expected
    """

    # some default logic for simple actions

    return {
        'test': ['install']
    }


def test(job):
    import sys, time
    service = job.service
    cl = None
    acc = None
    space = None
    try:
        g8client = service.producers['g8client'][0]

        account = service.producers['account'][0]
        account_data = account.model.data
        config_instance = "{}_{}".format(g8client.aysrepo.name, g8client.model.data.instance)
        cl = j.clients.openvcloud.get(instance=config_instance, create=False, die=True, sshkey_path="/root/.ssh/ays_repos_key")
        acc = cl.account_get(account.model.dbobj.name)
        space = acc.space_get('%sVdcConsumption' % account.model.dbobj.name, cl.config.data['address'].split('.')[0])
        while space.model['status'] != 'DEPLOYED':
            time.sleep(3)
            space = acc.space_get('%sVdcConsumption' % account.model.dbobj.name, cl.config.data['address'].split('.')[0])
        actual_consumption = acc.get_consumption(start=account_data.consumptionFrom, end=account_data.consumptionTo)

        if account.model.data.consumptionData == actual_consumption:
            service.model.data.result = 'OK : test_create_accounts_with_specs'
        else:
            service.model.data.result = 'FAILED : test_create_accounts_with_specs'
    except:
        service.model.data.result = 'ERROR :  %s %s' % ('test_create_accounts_with_specs', str(sys.exc_info()[:2]))
    finally:
        if space is not None:
            space.delete()
            acc.delete()
    service.save()
