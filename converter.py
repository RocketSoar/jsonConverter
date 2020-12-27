import os
import cv2
import numpy as np
import shutil
import argparse
from json_to_dataset import json_to_dataset

parser=argparse.ArgumentParser()
parser.add_argument('-jp','--json_path',type=str,required=True)
parser.add_argument('-o','--output_path',type=str,required=True)
#with_others or only_json
parser.add_argument('-m','--mode',type=str,default='with_others',choices=['with_others','only_json'])

args=parser.parse_args()

jsonPath=args.json_path
jsonPath=jsonPath.replace('\\','/')
outputPath=args.output_path
outputPath=outputPath.replace('\\','/')
mode=args.mode

tempOut="tempOutput"
if not os.path.exists(tempOut):
    os.makedirs(tempOut,exist_ok=True)
if not os.path.exists(outputPath):
    os.makedirs(outputPath,exist_ok=True)
#Warning:will delete all the files in outputPath
shutil.rmtree(outputPath)


def main():
    convertedCounter = 0
    otherFilesCounter = 0
    for root,_,imgs in os.walk(jsonPath):
        for img in imgs:
            print(os.path.join(root, img))
            if mode=='with_others':
                if "json" not in img:
                    newPath = root.replace(jsonPath, outputPath)
                    if not os.path.exists(newPath):
                        os.makedirs(newPath,exist_ok=True)
                    shutil.copy(os.path.join(root, img), newPath)
                    otherFilesCounter+=1
                    continue
            elif mode=='only_json':
                if "json" not in img:
                    continue
            else:
                print("mode error")
                return
            #convert
            json_to_dataset(os.path.join(root,img),tempOut)
            grayImg=cv2.imread(os.path.join(tempOut,"label.png"), cv2.IMREAD_GRAYSCALE)
            grayImg[np.where(grayImg>0)]=1
            grayImg.dtype="int8"
            newPath=root.replace(jsonPath,outputPath)
            if not os.path.exists(newPath):
                os.makedirs(newPath,exist_ok=True)
            np.save(os.path.join(newPath,img.replace("json","npy")),grayImg)
            convertedCounter+=1
    print(f"Converted {convertedCounter} json labels")
    print(f"Transfered {otherFilesCounter} other types of files")
if __name__=="__main__":
    main()




