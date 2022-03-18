# A Blind Stick for visually impaired person
The motivation behind this project is **to help visually impaired person to percept their surroundings** better. The person must use a blindstick or a spectacles equipped with a camera, a mic and a speaker which will be acting as a node. Whenever the person wants to percept their surrounding they must press a buttonand the camera will capture a picture. This captured image is sent to a remote server where the inference will be generated using **CLIP model** which is **an image captioning model** and will be sent back to the person. The inference will be spoken out and he/she can hear it to better understand its surroundings. Later on he/she can ask some questions related to the things that is heard and again that speech will be converted to text and sent to server. The server will answer the questions using the **ViLT model** which is **a Vision and Language(V&L) model** and sent back to the person to read out to them.

## Steps for impementation

## Pretrained weights
1. [COCO weights](https://drive.google.com/file/d/18SAyrszaf4wJLKuM8xoEkKuxUismVjI8/view?usp=sharing)
2. [Conceptual weights](https://drive.google.com/file/d/16nO7KA_-iABxA0TyP1llw136TFbgP2IO/view?usp=sharing)

## References
1. [CLIP reference](https://openai.com/blog/clip/)
2. [CLIP repository](https://github.com/rmokady/CLIP_prefix_caption)
3. [ViLT reference](https://arxiv.org/pdf/2102.03334.pdf)
4. [ViLT repository](https://github.com/dandelin/ViLT)
