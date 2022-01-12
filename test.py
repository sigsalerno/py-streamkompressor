import json 

from src.streamkompressor.streamkompressor import StreamKompressor

def result_bytesize(obj):
    size = 0

    for item in obj:
        size += len(item)

    return size 

if __name__ == "__main__":

    data = [
        {'a': 1, 'b': 2, 'c': 10000},
        {'a': 7, 'b': 1, 'c': 10001},
        {'a': 66, 'b': -1, 'c': 10002},
        {'a': 78, 'b': 1, 'c': 10003},
        {'a': 12, 'b': 1, 'c': 10004},
        {'a': -34, 'b': 1, 'c': 10005},
        {'a': -34, 'b': 1, 'c': 10006}
    ]

    LABEL = "Test"
    print(data)
    test_object_size = len(json.dumps((data)))
    print("Test object size: %i" % (test_object_size))

    sk = StreamKompressor(chunk_size=0, max_chunks=0)

    result = sk.kompress(data, label=LABEL)

    print(result)
    compressed_object_size = result_bytesize(result)
    print("Compressed object size: %i" % (compressed_object_size))
    print("Compressing Factor: %02f%% " % (100-(compressed_object_size/test_object_size)*100))

    decompressed, label = sk.dekompress(result)

    if decompressed == data:
        print("Compression OK")
    else:
        print("Compress/Decompress mismatch")
    
    
    if label == LABEL:
        print("Labelling OK " + label)
    else:
        print("Labelling mismatch")