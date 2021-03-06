# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_data.unpaired.ipynb (unless otherwise specified).

__all__ = ['RandPair', 'get_dls']

# Cell
from fastai.vision.all import *
from fastai.basics import *
from typing import List
from fastai.vision.gan import *

# Cell
class RandPair(Transform):
    "Returns a random image from domain B, resulting in a random pair of images from domain A and B."
    def __init__(self,itemsB): self.itemsB = itemsB
    def encodes(self,i): return random.choice(self.itemsB)

# Cell
#GET RID OF THIS
def get_dls(pathA, pathB, num_A=None, num_B=None, load_size=512, crop_size=256, bs=4, num_workers=2):
    """
    Given image files from two domains (`pathA`, `pathB`), create `DataLoaders` object.
    Loading and randomly cropped sizes of `load_size` and `crop_size` are set to defaults of 512 and 256.
    Batch size is specified by `bs` (default=4).
    """
    filesA = get_image_files(pathA)
    filesB = get_image_files(pathB)
    filesA = filesA[:min(ifnone(num_A, len(filesA)),len(filesA))]
    filesB = filesB[:min(ifnone(num_B, len(filesB)),len(filesB))]

    dsets = Datasets(filesA, tfms=[[PILImage.create, ToTensor, Resize(load_size),RandomCrop(crop_size)],
                                   [RandPair(filesB),PILImage.create, ToTensor, Resize(load_size),RandomCrop(crop_size)]], splits=None)

    batch_tfms = [IntToFloatTensor, Normalize.from_stats(mean=0.5, std=0.5), FlipItem(p=0.5)]
    dls = dsets.dataloaders(bs=bs, num_workers=num_workers, after_batch=batch_tfms)

    return dls