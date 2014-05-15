

test_net_if = None

def get_net_if():
    global test_net_if
    if test_net_if is None:
        test_net_if = raw_input("Please input a free ethernet interface for network test:")
        test_net_if = test_net_if.strip()

    return test_net_if







