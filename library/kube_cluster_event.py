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
            account_alias = dict(required=True),
            cluster_id = dict(required=True),
            message = dict(required=True)
        )
    )

    if not HAS_HTTPLIB2:
        module.fail_json(msg="httplib2 is not installed")

    endpoint = module.params['endpoint']
    account_alias = module.params['account_alias']
    cluster_id = module.params['cluster_id']
    message = module.params['message']
    h = httplib2.Http()

    response, content = h.request(endpoint + '/kube/' + account_alias +
            '/' + cluster_id + '/events', method='POST', body=json.dumps({'message' : message}))

    if response.status != 204:
        
        module.fail_json(changed=False, msg='Failed to create cluster event with message ' + message)

    module.exit_json(changed=True, content=content)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
