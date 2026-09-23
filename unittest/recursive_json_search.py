from test_data import *
from policy import POLICY

def json_search(key, input_object, role=None):
    ret_val = []

    if isinstance(input_object, dict):
        for k, v in input_object.items():
            if k == key:
                # RBAC Check: If key exists in POLICY, verify if role is in the allowed list
                is_allowed = True
                if k in POLICY:
                    if role not in POLICY[k]:
                        is_allowed = False
                
                # Only add to result if role is valid or key is unrestricted
                if is_allowed:
                    temp = {k: v}
                    ret_val.append(temp)
                
            if isinstance(v, dict):
                ret_val.extend(json_search(key, v, role))
            elif isinstance(v, list):
                for item in v:
                    if not isinstance(item, (str, int)):
                        ret_val.extend(json_search(key, item, role))
    else:
        for val in input_object:
            if not isinstance(val, (str, int)):
                ret_val.extend(json_search(key, val, role))
                
    return ret_val

if __name__ == '__main__':
    # Test printing result with viewer role (no permission to read apiKey)
    print(json_search("apiKey", data, role="viewer"))