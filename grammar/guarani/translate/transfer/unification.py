class UnificationFailed(Exception):
    pass

# Should return None if unification fails
# Restriction: user cannot try to unify on nested features, only top level features.
def unify(left_features, right_features, feat):

    # Due to the restriction we can do the following:
    left_dict = left_features[feat]
    right_dict = right_features[feat]

    if (isinstance(left_dict, str) and isinstance(right_dict, str)):
        if left_dict == right_dict:
            return {feat: left_dict}
        else:
            return None
    elif not (isinstance(left_dict, str) and isinstance(right_dict, str)):
        try:
            res = {feat: nested_unify(left_dict, right_dict)}
            return res
        except UnificationFailed as e:
            return None
    else:
        return None 

def nested_unify(left, right):
    result = {}
    for key in left.keys():
        if key in right:
            if (left[key] is dict and right[key] is dict):
                result[key] =  nested_unify(left[key], right[key])
            elif (left[key] == right[key]):
                result[key] = left[key]
            else:
                raise UnificationFailed("Unification failed")
    return result