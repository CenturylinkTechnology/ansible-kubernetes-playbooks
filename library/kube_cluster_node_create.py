#!/usr/bin/python

HAS_HTTPLIB2 = True
try:
    import httplib2
except ImportError:
    HAS_HTTPLIB2 = False

import json

def main():

    module = AnsibleModule(
        argument_spec = dict(
            endpoint = dict(required=False, default='http://wf-cntnr-api-svc-v1.service.consul:32000'),
            authorization = dict(required=True),
            account_alias = dict(required=True),
            cluster_id = dict(required=True),
            data = dict(required=True)
        )
    )

    if not HAS_HTTPLIB2:
        module.fail_json(msg="httplib2 is not installed")

    endpoint = module.params['endpoint']
    authorization = module.params['authorization']
    account_alias = module.params['account_alias']
    cluster_id = module.params['cluster_id']
    data = module.params['data']
    h = httplib2.Http()

    response, content = h.request(endpoint + '/kube/' + account_alias +
            '/clusters/' + cluster_id + '/nodes', method='POST', body=json.dumps({'data' : data}), 
            headers={'Authorization' :  authorization, 'Content-Type' : 'application/json'})

    if response.status != 204:
        
        module.fail_json(changed=False, msg=response)

    module.exit_json(changed=True, content=content)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
