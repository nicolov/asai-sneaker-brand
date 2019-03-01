#!/usr/bin/env python

import json
from glob import glob
import os
from shutil import copyfile

interesting_brands = [
	'adidas',
	'Air Jordan',
	'Vans',
	# 'Nike',
]

def main():
	json_paths = glob('data/*.json')

	for b in interesting_brands:
		os.makedirs(f'organized/train/{b}')
		os.makedirs(f'organized/validation/{b}')

	for i, jp in enumerate(json_paths):
		with open(jp) as f:
			data = json.load(f)

		if not data['gender']:
			continue

		brand = data['brand_name']

		if brand in interesting_brands:
			img_name = os.path.basename(data['main_picture_url'])
			
			if img_name.startswith('missing'):
				continue

			img_name = img_name.replace('.png', '.jpg')	
			img_path = os.path.join(
				'imgs_cropped', data['gender'][0], img_name)
			print(img_path)

			if i % 10 < 2:
				dest_dir = f'organized/validation/{brand}'
			else:
				dest_dir = f'organized/train/{brand}'
			copyfile(
				img_path, os.path.join(dest_dir, img_name))

if __name__ == '__main__':
	main()
