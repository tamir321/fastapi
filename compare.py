
def compare(expected, actual):
    print(f"compare actual- {actual}")
    print(f"compare expected- {expected}")
    for att,val in expected.items():
         print(f"att - {att} actual[att] - {actual[att] }  val - {val}")
         if actual[att] != val:
             return False
    return True