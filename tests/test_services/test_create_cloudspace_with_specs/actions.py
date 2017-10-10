def init_actions_(service, args):
    """
    this needs to returns an array of actions representing the depencies between actions.
    Looks at ACTION_DEPS in this module for an example of what is expected
    """

    # some default logic for simple actions


    return {
        'test_create_cloudspace_with_specs': ['install']
    }


def authenticate(g8client):
    import requests
    username = g8client.model.data.login
    password = g8client.model.data.password
    url = 'https://' + g8client.model.data.url

    login_url = url + '/restmachine/system/usermanager/authenticate'
    credential = {'name': username,
                  'secret': password}

    session = requests.Session()
    session.post(url=login_url, data=credential)
    return session


def test_create_cloudspace_with_specs(job):
    import sys, time
    service = job.service
    try:
        g8client = service.producers['g8client'][0]
        session = authenticate(g8client)

        vdc = service.producers['vdc'][0]
        vdcId = vdc.model.data.cloudspaceID
        maxMemoryCapacity = vdc.model.data.maxMemoryCapacity
        maxCPUCapacity = vdc.model.data.maxCPUCapacity
        maxDiskCapacity = vdc.model.data.maxDiskCapacity
        maxNumPublicIP = vdc.model.data.maxNumPublicIP

        url = 'https://' + g8client.model.data.url
        API_URL = url + '/restmachine/cloudapi/cloudspaces/get'
        API_BODY = {'cloudspaceId': vdcId}

        response = session.post(url=API_URL, data=API_BODY)

        limits = response.json()['resourceLimits']
        actual = [limits['CU_M'], limits['CU_D'], limits['CU_I'], limits['CU_C']]
        expected = [maxMemoryCapacity, maxDiskCapacity, maxNumPublicIP, maxCPUCapacity]

        if response.status_code == 200 and actual == expected:
            service.model.data.result = 'OK : %s ' % 'test_create_cloudspace'
        else:
            response_data = {'status_code': response.status_code,
                             'content': response.content}
            service.model.data.result = 'FAILED : %s %s' % ('test_create_cloudspace', str(response_data))

    except:
        service.model.data.result = 'ERROR : %s %s' % ('test_create_cloudspace', str(sys.exc_info()[:2]))
    finally:
        if 'g8client' in service.producers and 'vdc' in service.producers:
            session = authenticate(service.producers['g8client'][0])
            vdc = service.producers['vdc'][0]
            API_URL_DELETE = 'https://%s/restmachine/cloudapi/cloudspaces/delete' % g8client.model.data.url
            API_URL_GET = 'https://%s/restmachine/cloudapi/cloudspaces/get' % g8client.model.data.url
            API_BODY = {'cloudspaceId': vdc.model.data.cloudspaceID}
            res = session.post(url=API_URL_GET, data=API_BODY)
            while res.json()['status'] != 'DEPLOYED' and res.status_code == 200:
                time.sleep(5)
                res = session.post(url=API_URL_GET, data=API_BODY)

            session.post(url=API_URL_DELETE, data=API_BODY)
    service.save()
