import msgpack 

class StreamKompressor:

    def __init__(self, chunk_size = 0, max_chunks = 0):

        self.streams = {}
        self.streams_count = 0

        self.max_chunks = max_chunks
        self.max_chunk_size = chunk_size
        self.chunks = []
        self.chunks_count = 1 

    #Encoding algorithm wrapper, returns msgpack encoded object
    def _encode(self, payload):
        return(msgpack.packb(payload))

    #Decoding algorithm wrapper, returns msgpack encoded object
    def _decode(self, payload):
        return(msgpack.unpackb(payload))

    def append(self, stream: dict):
        """
        Append a sampling object to the payload

        This method compress and adds the new sampling object to the buffer. 
        If chunk_size and max_chunks are defined, it creates the new chunks in the buffer and return False if no more chunks can be created,
        discarding the last stream

        Parameters
        stream : dict
            Sampling object example:  {'a': 2, 'b': 3, 't': 4456 }

        Returns
        bool
            True if sampling object is added to the chunk correctly
            False if no more chunks can be created, and the sampling object is discarded
        """

        streams = self.streams.copy()

        for field in stream:

            #Normalize the input as integer value
            value = int(stream[field])

            if not field in self.streams:
                streams[field] = [0] * self.streams_count

            if self.streams_count > 0:
                streams[field].append(value - sum(streams[field]))
            else:
                streams[field].append(value)

        if self.max_chunk_size and self._chunk_size() > self.max_chunk_size:
            self.chunks.append(self.streams)
            self.chunks_count += 1
            if self.max_chunks and self.chunks_count > self.max_chunks:
                return False

            self.streams = {}
            self.streams_count = 0

            self.append(stream)

        else:
            self.streams = streams.copy()

        self.streams_count += 1

        return True

    #Returns the on-process chunk size
    def _chunk_size(self):
        return len(self._encode(self.streams))

    def kompress(self, samples = []):
        """
        Returns the kompressed and encoded chunk sizes

        Parameters
        samplings : list 
            Optional: list of sampling objects

        Returns
        list
            List of the data chunks ordered from the oldest to the newest, false if chunk size is passed
            
        """

        if len(samples) > 0:
            for sample in samples:
                result = self.append(sample)
                if not result: 
                    return False

        return [self._encode(chunk) for chunk in self.chunks] + [self._encode(self.streams)]

    def dekompress(self, chunks = []):
        """
        Returns the dekompressed data in an object

        Parameters
        chunks : list 
            list of chunks

        Returns
        list
            List of the uncompressed data
            
        """
        result = []
        for chunk in chunks:
            decoded_chunk = self._decode(chunk)
            

            unpacked = False
            for index in decoded_chunk:
                #Init the uncompressed streams
                if not unpacked:
                    unpacked = [False] * len(decoded_chunk[index])
                
                count = 0
                for data in decoded_chunk[index]:
                    if not unpacked[count]:
                        unpacked[count] = {}
                    if count == 0:
                        unpacked[count][index] = data
                    else:
                        unpacked[count][index] = unpacked[count - 1 ][index] + data

                    count +=1

            result += unpacked
        
        return result 
