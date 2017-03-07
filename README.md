# **S**emantic **I**mage **L**ocal **E**nhancement

This project generates local image enhancements based on given keywords.

Example:

![](examples/original.jpg)

Using the keyword **Lily**

![](examples/enhanced.jpg)

# Installation

This project uses Python 3.5 and all the libraries can be installed using conda

`conda env create -f environment.yml`

# Code hierarchy

The main code is in the `src` folder and each subfolder contains a README that explains its content
The `matlab` directory contains previous scripts used to generate global image enhancement

Outside there are some python main files that do the following:

    * `copy-by-tag.py`: Given a tag name, copies the images from the flickr db into a folder of their own (Save directory might be changed)
    * `copy-masks.py`: Copies the generated masks into a directory structure similiar to flickr
    * `runner.py`: Contains an example to calculate z-values
    * `grabcut.py`: Allows to do grabcut on a given image. Taken from https://github.com/opencv/opencv/blob/master/samples/python/grabcut.py

# Notebooks

There are also a couple of notebooks that I used to generate the results.
They assume you have the following folder hierarchy:
    * z-values:
        - keyword1-zvalue.pkl
        - keyword1-zvalue-local.pkl
        - keyword2-zvalue.pkl
        - keyword2-zvalue-local.pkl
    * images:
        - keyword1:
            * image1_id.jpg
            * image2_id.jpg
        - keyword2:
            * image3_id.jpg
    * masks:
        - keyword1:
            * mask1_id.jpg
            * mask2_id.jpg
        - keyword2:
            * mask3_id.jpg
