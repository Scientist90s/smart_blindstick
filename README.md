# A Blind Stick for visually impaired person
The motivation behind this project is **to help visually impaired person to percept their surroundings** better. The person must use a blindstick or a spectacles equipped with a camera, a mic and a speaker which will be acting as a node. Whenever the person wants to percept their surrounding they must press a buttonand the camera will capture a picture. This captured image is sent to a remote server where the inference will be generated using **CLIP model** which is **an image captioning model** and will be sent back to the person. The inference will be spoken out and he/she can hear it to better understand its surroundings. Later on he/she can ask some questions related to the things that is heard and again that speech will be converted to text and sent to server. The server will answer the questions using the **ViLT model** which is **a Vision and Language(V&L) model** and sent back to the person to read out to them.

## Steps for impementation
This repositroy will require you to install [python 3.6.8](https://www.python.org/downloads/release/python-368/).

Follow the below steps to successfully setup this repository to your local machine

1. clone the respository using
    ```
    git clone https://github.com/Scientist90s/smart_blindstick
    ```
2. Install [java](https://www.java.com/download/ie_manual.jsp) which is required for one of the dependency's installation
3. Navigate to node folder and install node dependencies using
    ```
    pip3 install -r requirements_node.txt
    ```
4. Navigate to server folder and install server dependencies using
    ```
    pip3 install -r requirements_server.txt
    ```
5. open server.py and change your acquired ip address at line 25
    ```
    self.host = "xxx.xxx.xxx.xxx"
    ```
6. Run `python3 server.py`
7. open node.py and change the value of read_image to `True` if you are not going to use camera
    ```
    self.read_image = True
    ```
8. open another terminal and run `python3 node.py`

## Pretrained weights
1. [COCO weights](https://drive.google.com/file/d/18SAyrszaf4wJLKuM8xoEkKuxUismVjI8/view?usp=sharing)
2. [Conceptual weights](https://drive.google.com/file/d/16nO7KA_-iABxA0TyP1llw136TFbgP2IO/view?usp=sharing)

## References
1. [CLIP reference](https://openai.com/blog/clip/)
2. [CLIP repository](https://github.com/rmokady/CLIP_prefix_caption)
3. [ViLT reference](https://arxiv.org/pdf/2102.03334.pdf)
4. [ViLT repository](https://github.com/dandelin/ViLT)
