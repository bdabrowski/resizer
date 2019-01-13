# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid
import pytest
from PIL import Image

from resize import resize_image

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_files')
output_path = ''


def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    module.output_path = os.path.join('/tmp', str(uuid.uuid4()))
    os.mkdir(module.output_path)


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    if os.path.exists(module.output_path):
        for irpath, dirnames, filenames in os.walk(module.output_path):
            for filename in filenames:
                os.remove(os.path.join(module.output_path, filename))
        os.rmdir(module.output_path)


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'IMG_20181101_153502.jpg'),
    os.path.join(FIXTURE_DIR, 'IMG_20181101_153508.jpg'),
    os.path.join(FIXTURE_DIR, 'PANO_20181101_153612.jpg'),
)
def test_1(datafiles):
    """Test of image resize."""
    for image_path in datafiles.listdir():
        image = Image.open(str(image_path))
        new_full_path = resize_image(image, output_path, 100, 100)
        expected_full_path = os.path.join(output_path, os.path.basename(str(image_path)).replace('.jpg', '_100x100.jpg'))
        assert new_full_path == expected_full_path
        assert os.path.exists(expected_full_path)
