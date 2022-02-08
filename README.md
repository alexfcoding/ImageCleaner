# ImageCleaner
Cleans similar or duplicate images from folder using perceptual image hashing with live preview

## How it works
[Perceptual hashing](https://en.wikipedia.org/wiki/Perceptual_hashing#:~:text=Perceptual%20hashing%20is%20the%20use,drastic%20change%20in%20output%20value)

#### The script detects similar images based on a simple algorithm:
- Reducing size of each image to NxN pixels (set by user)
- Converting to grayscale
- Calculating the mean of all color values
- Setting the color of each pixel to black if the NxN matrix value is above average, and to white otherwise
- [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance): comparing hashes with each other and count the number of different pixels
- The image is considered similar and moved from the folder if hamming distance is less than a threshold set by user

## How to run

Tested with Python 3.8.2, OpenCV 4.3.0, Ubuntu 20.04 LTS

Folder `input_images` contains 11 objects in 186 image variations created by YOLO neural detector from video

This example will leave all unique 11 objects in the folder, the rest will be moved to `similar_images`: 

`python image_hash.py -i images/input_images -o images/similar_images -s 16 -t 33`

Args:

`-i`: input path to scan

`-o`: output path to move similar images

`-s`: hash size (default=16)

`-t`: threshold percent value for detection from 0 to 100, where 0 is absolute similarity of hashes (only nearly identical images will be moved)

### Similar images search:
![](assets/search_similar.gif)

### Moving similar images to another folder (right column) leaving only unique (left column):
![](assets/move_similar.gif)

### Hash generation:
![](assets/hashed_harold.gif)

### Similarity threshold (t = 2%)  (moved 7 nearly identical images)
![](assets/2.jpg)

### Similarity threshold (t = 33%) (only unique objects remained, 175 similar images moved)
![](assets/33.jpg)


