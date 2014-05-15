

test_block = None

def get_block_dev():
    global test_block
    if test_block is None:
        test_block = raw_input("Please input a free block dev(filepath) for filesystem test:")
        test_block = test_block.strip()

    return test_block







