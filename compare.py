def compare(expected, actual):
    if type(expected) == dict:
        for att, val in expected.items():
            if att in actual:
                if actual[att] != val:
                    print(f"att - {att} actual[att] - {actual[att]}  val - {val}")
                    return False
            else:
                print(f"key {att} is missing in {actual}")
                return False
        return True
    else:
        print("not dict")
        if expected==actual:
            return True
        else:
            print(f"expect {expected} ,actual {actual} ")
            return False

def compare_arr(expected, actual):
    results = []
    if type(expected) == list:
        if len(expected) != len(actual):
            print(f"expect to get {len(expected)} actual size {len(actual)}")
            return False
        for exp, act in zip(expected, actual):
            val = compare(exp, act)
            if not val:
                print(f"expected {exp} actual - {act} ")
            results.append(val)
    elif type(expected) == dict:
        print("dict")
        results.append(compare(expected, actual))
    else:
        results.append(expected==actual)
    return all(results)


a = [{"name": "doggie","status": "sold"},{"name": "doggie1","status": "sold"},{"name1": "doggie","status": "sold"}]
b = [{"name": "doggie","status": "sold"},{"name": "doggie","status": "sold"},{"name": "doggie","status": "sold"}]

z= {"name": "doggie","status": "sold"}
g= {"name": "doggie","status": "sold","some":2}
print (compare_arr(a, b))
