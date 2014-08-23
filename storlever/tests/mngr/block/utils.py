

test_block = None

def get_block_dev():
    global test_block
    if test_block is None:
        test_block = raw_input("Please input a free block dev(filepath) for block test: ")
        test_block = test_block.strip()

    return test_block


extra_test_block = None

def get_extra_block_dev():
    global extra_test_block
    if extra_test_block is None:
        extra_test_block = raw_input("Please input a extra free block dev(filepath) for lvm test: ")
        extra_test_block = extra_test_block.strip()

    return extra_test_block

def get_block_dev_simple():
    return raw_input("Please input a free block device (filepath like /dev/vdb) for block test: ").strip()





