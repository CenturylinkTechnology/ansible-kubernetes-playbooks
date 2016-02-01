#!/usr/bin/python

HAS_HTTPLIB2 = True
try:
    import httplib2
except ImportError:
    HAS_HTTPLIB2 = False

import datetime
import time
import io

def main():

    module = AnsibleModule(
        argument_spec = dict(
            endpoint = dict(required=True),
            method = dict(required=False, default='GET'),
            status = dict(required=False, default=200),
            timeout = dict(required=False, default=60)
        )
    )

    if not HAS_HTTPLIB2:
        module.fail_json(msg="httplib2 is not installed")

    endpoint = module.params['endpoint']
    method = module.params['method']
    status = module.params['status']
    timeout = module.params['timeout']
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=timeout)
    available = False
    
    while datetime.datetime.now() < end:
    
        try:
            response, content = httplib2.Http().request(endpoint, method=method)

            if response.status == status:
                available = True
                break
            
        except:
            time.sleep(1)
    
    if not available:
        module.fail_json(changed=False, msg='Wait for ' + endpoint + ' unsuccessful.') 
        
    module.exit_json(changed=False)
            
# import module snippets
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()