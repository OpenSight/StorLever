

test_block = ""

def get_block_dev():
    global test_block
    if test_block is None or test_block == "":
        test_block = raw_input("Please input a block dev(filepath) for test:")

    return test_block







