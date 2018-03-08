import os
import numpy as np
import cv2
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--path',type=str)
parser.add_argument('--L',type=int)
parser.add_argument('--outpath',default='.',type=str)
args = parser.parse_args()

imglist=[]

def getData(path):
    for dir, subdirs,files  in os.walk(path):
        for file in files:
            img=cv2.imread(os.path.join(path,file))
            if img is not None:
                    imglist.append(img)


def getImagrModel(img1,img2,img3):
    model=(img3 & (img1^img2))|(img1&img2)
    return model


def bg_generation(L_level,outpath):
    L=L_level
    bglist=[]
    for i in range(3**(L-1)):
        ran=np.random.randint(low=0,high=(len(imglist)-1),size=(3))
        bg=getImagrModel(imglist[ran[0]],imglist[ran[1]],imglist[ran[2]])
        bglist.append(bg)
    cv2.imwrite(os.path.join(outpath,'L_%d.jpg'%1), bglist[0])
    for i in range(2,L+1):
        for j in range(3**(L-i)):
            bg=getImagrModel(bglist[3*j],bglist[3*j+1],bglist[3*j+2])
            bglist[j]=bg
        cv2.imwrite(os.path.join(outpath,'L_%d.jpg'%i), bglist[0])


if __name__ == '__main__':
    print("Start loading images...")
    getData(args.path)
    if len(imglist)==0:
        print("Error: no image in '%s'."%args.path)
        exit(1)
    print("Finish loading.")
    bg_generation(args.L,args.outpath)
    print("Finish background generation.")

