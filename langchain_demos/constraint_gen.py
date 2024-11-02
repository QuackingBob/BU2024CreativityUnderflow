import base64
from openai import OpenAI
import os
import cv2
import json
 
import numpy as np
import time
from datetime import datetime
import json
import dotenv
dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY')
# Function to encode the image
def encode_image(image_array):
    # Convert numpy array to PNG format
    success, encoded_image = cv2.imencode('.png', image_array)
    if not success:
        raise ValueError("Could not encode image")
    return base64.b64encode(encoded_image.tobytes()).decode('utf-8')

class LaTeXGenerator:
    def __init__(self, save_dir='./'):
       
        base_dir = os.path.dirname(__file__)
        self.client = OpenAI(api_key=API_KEY)
        self.base_dir = os.path.join(save_dir, 'vlm_query')

        with open(os.path.join(base_dir, 'prompt_template.txt'), 'r') as f:
            self.prompt_template = f.read()

    def _build_prompt(self, img):
        img_base64 = encode_image(img)
        prompt_text = self.prompt_template
        # save prompt
     #   with open(os.path.join(self.task_dir, 'prompt.txt'), 'w') as f:
     #       f.write(prompt_text)
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    },
                ]
            }
        ]
        return messages
 
     
    def generate(self, img,):
        """
        Args:
            img (np.ndarray): image of the scene (H, W, 3) uint8
            instruction (str): instruction for the query
        Returns:
            save_dir (str): directory where the constraints
        """
        # create a directory for the task
        fname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.task_dir = os.path.join(self.base_dir, fname)
        os.makedirs(self.task_dir, exist_ok=True)
        # save query image
        # image_path = os.path.join(self.task_dir, 'query_img.png')
        # cv2.imwrite(image_path, img[..., ::-1])
        # build prompt
        
        messages = self._build_prompt(img)
        print(messages)
        
        # stream back the response
        stream = self.client.chat.completions.create(model='chatgpt-4o-latest',
                                                        messages=messages,
                                                        temperature=0,
                                                        max_tokens=2048,
                                                        stream=True)
        
        output = ""
        start = time.time()
        for chunk in stream:
            print(f'[{time.time()-start:.2f}s] Querying OpenAI API...', end='\r')
            if chunk.choices[0].delta.content is not None:
                output += chunk.choices[0].delta.content
        print(f'[{time.time()-start:.2f}s] Querying OpenAI API...Done')
        # save raw output
        with open(os.path.join(self.task_dir, 'output_raw.tex'), 'w') as f:
            f.write(output)
        print(output)
        
        return output
         
