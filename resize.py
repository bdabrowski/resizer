# -*- coding: utf-8 -*-
from __future__ import unicode_literals

version = '0.0.1'

description = """\
Mass picture resizer.
"""
changes = []

from argparse import ArgumentParser, SUPPRESS
import os
import sys
import Image
import ImageOps
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    parser = ArgumentParser(description='Resizes pictures from defined directory.',
                            argument_default=SUPPRESS)
    parser.add_argument('id', 'input-directory', nargs='?', default='',
                        help='Full path to directory with photos.')
    parser.add_argument('od', '--output-directory', nargs='?', default='processed',
                        help='Full path to directory with photos. Default is `processed`.')
    parser.add_argument('-a', '--all', action='store_true',
                        default=False, help='Process all formats in directory (currently only JPG) and '
                                            'set input file format as default output format (currently only JPG).')
    parser.add_argument('-if', '--input-format', nargs='?',
                        default='all', help='Set input format (currently only JPG). Set `all` to find all formats. '
                                            'Default is `all`.')
    parser.add_argument('-of', '--output-format', nargs='?',
                        default='jpeg', help='Set output format (currently only JPG). Default is `jpeg`.')
    parser.add_argument('-h', '--height', nargs='?',
                        default='768', help='Set height in pixels for output images. Use `%` to set percent of reduction.'
                                            ' Default is 768.')
    parser.add_argument('-w', '--width', nargs='?',
                        default='1024', help='Set width in pixels for output images. Use `%` to set percent of reduction.'
                                             ' Default is 1024.')
    parser.add_argument('-n', '--name', nargs='?',
                        default='', help='Set name for all processed photos (default are current photo names).')

    args = parser.parse_args()

    if not os.path.isdir(args.input_directory):
        logging.info('Provided path %s does not exist.' % args.input_directory)
        sys.exit()

    input_directory = args.input_directory if args.input_directory else os.getcwd()
    output_directory = args.output_directory

    if not args.input_format in ['jpeg', 'jpg', 'JPEG', 'JPG', 'all', '']:
        logging.info('Input format %s is incorrect.' % args.input_format)
        parser.print_help()
        sys.exit()

    if not args.input_format in ['jpeg', 'jpg', 'JPEG', 'JPG', 'all', '']:
        logging.info('Output format %s is incorrect.' % args.output_format)
        parser.print_help()
        sys.exit()

    input_format = 'jpeg'
    output_format = 'jpeg'

    def check_size_format(size):
        def is_number(s):
            try:
                int(s)
                return True
            except ValueError:
                return False
        if size[-1] == '%':
            return is_number(size[:-1])
        else:
            return is_number(size)


    if not check_size_format(height):
        logging.info('height format `%s` is incorrect.' % height)
        parser.print_help()
        sys.exit()

    if not check_size_format(width):
        logging.info('width format `%s`  is incorrect.' % height)
        parser.print_help()
        sys.exit()

    is_percent_height = True if args.height[-1] == '%' else False
    is_percent_width =  True if args.width[-1] == '%' else False
    if is_percent_height:
        height = int(args.height[:-1])
    else:
        height = int(args.height)
    if is_percent_width:
        width = int(args.width[:-1])
    else:
        width = int(args.width)


    nodes = os.listdir(path)
    for index, node in enumerate(nodes):
        logging.info('Processing file %s' % node)
        if os.path.splitext(node)[1] in ['JPG', 'JPEG', 'jpg', 'jpeg']:
            logging.info('%s is not jpeg - skipped' % node)
            continue
        image_path = os.path.join(path, node)
        image = Image.open(image_path)
        size = (1024, 768)
        oimage = ImageOps.fit(image, size, Image.ANTIALIAS)
        name, extention = node.split(os.extsep)
        new_name = ''.join([name, '_', str(index), os.extsep, extention])
        new_full_path = os.path.join(new_path, new_name)
        oimage.save(new_full_path, 'JPEG')
        logging.info('Saved %s' % new_full_path)
