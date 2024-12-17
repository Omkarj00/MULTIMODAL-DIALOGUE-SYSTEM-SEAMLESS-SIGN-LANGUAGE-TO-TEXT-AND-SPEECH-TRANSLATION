# MULTIMODAL-DIALOGUE-SYSTEM-SEAMLESS-SIGN-LANGUAGE-TO-TEXT-AND-SPEECH-TRANSLATION

## Abstract : 
Increasing communication accessibility for deaf and hard-of-hearing communities has drawn a lot of attention in recent years, especially when integrating multiple dialogue systems. This report presents a comprehensive dialogue system developed across several conversational programs to enable smooth translation between sign language to speech and   text. The system uses a bidirectional approach to translate spoken language into text and sign language and to convert sign language into speech and text. With the ultimate goal of developing inclusive communication tools, this dialogue system tackles issues like contextual understanding, logical speech interpretation, and real-time processing. With an emphasis on its possible effects on accessibility and social inclusion, user studies and performance simulations are used to determine the efficiency of our methodology. We evaluate the effectiveness of our approach through user studies and performance simulations that focus on potential impacts on social inclusion and accessibility. The findings show that the proposed dialogue system not only enhances communication but also creates greater understanding between different language groups. 

## Final Outcome Of Our Project :

![](https://github.com/Omkarj00/MULTIMODAL-DIALOGUE-SYSTEM-SEAMLESS-SIGN-LANGUAGE-TO-TEXT-AND-SPEECH-TRANSLATION/blob/main/Images/UI.jpg)

## Overview  
This project aims to create an advanced and reliable system for sign language recognition. The system is designed to improve recognition accuracy, support various signing styles, and handle different sign language dialects, while providing a seamless user experience.

## Objectives  
- **Sign Language Recognition**:  
  Develop an effective system to recognize sign language movements accurately, accounting for diverse signing styles and dialects.  

- **Real-Time Conversion**:  
  Create a real-time algorithm to reliably convert sign language gestures into text.  

- **Natural Language Processing Module**:  
  Implement cutting-edge Natural Language Processing (NLP) methods and models to process text generated from both spoken input and sign language movements.  

- **Speech Synthesis and Recognition**:  
  Build a system for precise speech synthesis and recognition to efficiently convert spoken words into text for further processing.  

- **User-Friendly Interface**:  
  Design a user-friendly interface that allows for a seamless transition between spoken and sign language modes.  

## Sign Language to Text Conversion:
- **Input Layer**:
  -  Real-time gesture input via webcam using Open CV.
- **Preprocessing**:
  -  Grayscale conversion, noise reduction (Gaussian blur), adaptive thresholding, and resizing to 128×128 pixels for uniformity.
- **CNN Architecture**:
  - Convolutional layers extract features (e.g., edges, textures).
  - Max pooling reduces dimensionality while retaining key features.
  - Softmax outputs gesture probabilities.
- **Output Layer**:
  - Displays recognized letters and combines them into words.
 
![](https://github.com/Omkarj00/MULTIMODAL-DIALOGUE-SYSTEM-SEAMLESS-SIGN-LANGUAGE-TO-TEXT-AND-SPEECH-TRANSLATION/blob/main/Images/Sign%20to%20text.png)

## Text to Sign Language Conversion:
- **Input Layer** :
  - Text input via text box or speech input using Web Speech API.
- **Processing Layer**:
  - Speech recognition and text preprocessing (tokenization, stopword removal).
- **Mapping Layer**:
  - Map preprocessed text to Indian Sign Language (ISL) gestures using a predefined lexicon.
- **3D Animation Layer**:
  - Generate ISL animations using Blender.
- **Output Layer**:
  - Display animations for real-time communication.
 
![](https://github.com/Omkarj00/MULTIMODAL-DIALOGUE-SYSTEM-SEAMLESS-SIGN-LANGUAGE-TO-TEXT-AND-SPEECH-TRANSLATION/blob/main/Images/Text%20to%20sign.png)

# Technologies Used:
-Programming Languages: Python
- Deep Learning Frameworks: TensorFlow, Keras
- Computer Vision Libraries: OpenCV
- Speech and NLP: Google Text-to-Speech API, Web Speech API, NLTK
- Animation: Blender 3D
- GUI Development: Tkinter

# Screenshots :
![](https://github.com/Omkarj00/MULTIMODAL-DIALOGUE-SYSTEM-SEAMLESS-SIGN-LANGUAGE-TO-TEXT-AND-SPEECH-TRANSLATION/blob/main/Images/UI.jpg)
![](https://github.com/Omkarj00/MULTIMODAL-DIALOGUE-SYSTEM-SEAMLESS-SIGN-LANGUAGE-TO-TEXT-AND-SPEECH-TRANSLATION/blob/main/Images/sign%20recoganisation.png)
![](https://github.com/Omkarj00/MULTIMODAL-DIALOGUE-SYSTEM-SEAMLESS-SIGN-LANGUAGE-TO-TEXT-AND-SPEECH-TRANSLATION/blob/main/Images/Text%20to%20sign%20.jpg)
![](https://github.com/Omkarj00/MULTIMODAL-DIALOGUE-SYSTEM-SEAMLESS-SIGN-LANGUAGE-TO-TEXT-AND-SPEECH-TRANSLATION/blob/main/Images/sign%20animations.jpg)
