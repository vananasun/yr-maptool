import lzo
from PIL import Image
from base64 import b64decode, b64encode
from struct import unpack_from


class PreviewBase:

    def from_image(self, filename: str):
        """
        Loads a preview from an image file.

        :param filename
        """
        img = Image.open(filename).convert('RGB')
        self.pixels = img.tobytes()
        self.width = img.width
        self.height = img.height


    def from_previewpack(self, width:int, height:int, packstr: str):
        """
        Loads a preview from a Base64 encoded PreviewPack string.

        :param width: The image width from the [Preview] section.
        :param height: The image height from the [Preview] section.
        :param packstr: Base64 encoded PreviewPack string.
        """
        self.width = width
        self.height = height
        self.pixels = bytes()

        packstr = b64decode(packstr)

        total_bytes = len(packstr)
        read_bytes = 0
        while read_bytes < total_bytes:

            size_compressed = unpack_from("<H", packstr, read_bytes)[0]
            read_bytes += 2
            size_uncompressed = unpack_from("<H", packstr, read_bytes)[0]
            read_bytes += 2
            # print("Block of size {} -> unpack to {}".format(
            #     size_compressed, size_uncompressed))

            self.pixels += lzo.decompress(
                packstr[read_bytes : read_bytes+size_compressed],
                False, # no LZO header
                size_uncompressed
            )
            read_bytes += size_compressed
    

    def to_previewpack(self):
        """
        :returns: Base64 encoded PreviewPack string
        """
        packbytes = bytearray()
        bytes_read = 0
        bytes_remaining = self.width * self.height * 3 # RGB
        while bytes_remaining > 0:
            
            decompressed_size = min(8192, bytes_remaining)
            block_data = lzo.compress(
                self.pixels[bytes_read : bytes_read + decompressed_size],
                1, # 1 is the only compatible compression level
                False) # no header
            compressed_size = len(block_data)
            # print("Writing block {} -> {}".format(decompressed_size, compressed_size))

            packbytes += compressed_size.to_bytes(2, 'little', signed=False)
            packbytes += decompressed_size.to_bytes(2, 'little', signed=False)
            packbytes += block_data
            bytes_read += decompressed_size
            bytes_remaining -= decompressed_size
        
        return b64encode(packbytes).decode('utf-8')


    def save_image(self, filename: str):
        """
        Saves this preview under the given filename. The format is determined
        automatically by the filename extension.

        :param filename:
        """
        img = Image.frombytes("RGB", (self.width, self.height), self.pixels)
        img.save(filename) # , format: "png"

    
    def show(self):
        img = Image.frombytes("RGB", (self.width, self.height), self.pixels)
        img.show()