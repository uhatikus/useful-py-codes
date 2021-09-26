from __future__ import print_function
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster

from pathlib import Path


def read_files(images_dir):
    images = []
    for p in Path(images_dir).iterdir():
        if p.is_file() and (".jpg" in str(p) or ".png" in str(p) or ".jpeg" in str(p)):
            print(p)
            images.append(Image.open(str(p)))
    return images


def main():

    images_dir = '/Users/ukhatov/Documents/Projects/rome/start'
    result_dir = '/Users/ukhatov/Documents/Projects/rome/finish'


    images = read_files(images_dir)
    print(str(len(images)) + " images have been read")

    NUM_CLUSTERS_s = [2, 15]

    for im_num, im in enumerate(images):
        NUM_CLUSTERS = NUM_CLUSTERS_s[im_num]
        # print('reading image')
        # im = Image.open('image.jpg')
        # im = im.resize((150, 150))      # optional, to reduce time
        ar = np.asarray(im)
        shape = ar.shape
        ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

        print('finding clusters')
        codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
        print('cluster centres:\n', codes)

        vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
        counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

        index_max = scipy.argmax(counts)                    # find most frequent
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        print('most frequent is %s (#%s)' % (peak, colour))

        import imageio
        c = ar.copy()
        for i, code in enumerate(codes):
            c[scipy.r_[scipy.where(vecs==i)],:] = code
        imageio.imwrite(f'clusters_{im_num}.png', c.reshape(*shape).astype(np.uint8))
        print('saved clustered image')


if __name__ == '__main__':
    main()