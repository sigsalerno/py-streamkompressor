# StreamKompressor

StreamKompressor is a Python library for compressing and decompressing sample data streams from IoT devices and sensors.
It also can divide the data in a maximum-byte-number block size, ideal for sending data to a limited packet size communication protocol such LoraWan, non continuos satellite connectivity (LEO) or distributed storage systems.

## Algorithm
StreamKompressor manages only integer values and utf-8 encoded labels. It performs better with small labels (less characters as possible)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install https://github.com/sigsalerno/py-streamkompressor/archive/refs/heads/master.zip
```

## Usage

```python
from streamkompressor.streamkompressor import StreamKompressor

#Input Data example
data = [
    {'a': 1, 'b': 2, 'c': 10000},
    {'a': 7, 'b': 1, 'c': 10001},
    #...
    {'a': -34, 'b': 1, 'c': 10006}
]

#Initialize
sk = StreamKompressor()

#Compress
result = sk.kompress(data)

#Decompress
sk.dekompress(result)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)