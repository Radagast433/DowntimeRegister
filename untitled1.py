# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 15:08:07 2022

@author: Sebafu
"""

import qrcode

img = qrcode.make('Some data here')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")