def init_actions_(service, args):
    """
    this needs to returns an array of actions representing the depencies between actions.
    Looks at ACTION_DEPS in this module for an example of what is expected
    """
    return {
        'test': ['install']
    }


def authenticate(g8client):
    import requests
    url = 'https://' + g8client.model.data.url
    username = g8client.model.data.login
    password = g8client.model.data.password

    login_url = url + '/restmachine/system/usermanager/authenticate'
    credential = {'name': username,
                  'secret': password}

    session = requests.Session()
    session.post(url=login_url, data=credential)
    return session


def test(job):
    import sys, json, time
    service = job.service
    RESULT_OK = 'OK : %s '
    RESULT_FAILED = 'FAILED : %s'
    RESULT_ERROR = 'ERROR : %s'
    try:
        g8client = service.producers['g8client'][0]
        session = authenticate(g8client)

        vm = service.producers['node'][0]
        vmID = vm.model.data.machineId
        url = 'https://' + g8client.model.data.url
        API_URL = url + '/restmachine/cloudapi/machines/getHistory'
        API_BODY = {'machineId': vmID, 'size': 10}

        response = session.post(url=API_URL, data=API_BODY)
        if response.status_code == 200:
            content = response.json()
            if content == json.loads(vm.model.data.vmHistory):
                service.model.data.result = RESULT_OK % 'test_get_virtualmachine_history'
            else:
                service.model.data.result = RESULT_FAILED % 'test_get_virtualmachine_history'
        else:
            response_data = {'status_code': response.status_code,
                             'content': response.content}
            service.model.data.result = RESULT_ERROR % str(response_data)+str(vmID)
    except Exception as e:
        service.model.data.result = RESULT_ERROR % (str(sys.exc_info()[:2]) + str(e))
    finally:
        if 'g8client' in service.producers and 'node' in service.producers:
            session = authenticate(service.producers['g8client'][0])
            node = service.producers['node'][0]
            API_URL = 'https://%s/restmachine/cloudapi/machines/delete' % g8client.model.data.url
            API_BODY = {'machineId': node.model.data.machineId}

            session.post(url=API_URL, data=API_BODY)

    service.save()
