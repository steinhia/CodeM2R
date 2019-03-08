# -*- coding: utf-8 -*-
import math
import distance
import csv
import operator
import random
import os
import numpy as np
from collections import Counter
import codecs
import re
import time
from functools import partial
import pickle

def calculatePositionalSegmentFreq(WordsList):
    dico={};dicoBi={};
    # pas de frequence pour les triphones, mais on veut des sequences legales
    Sum=1
    for row in WordsList:
        freq=float(row[1])*100#besoin de nombres entiers pour que le log soit représentatif
        if freq>0:
            Sum+=np.log10(freq)
            for i,pho in enumerate(row[0]):
                if not dico.has_key(pho):
                    dico[pho]=[0.0]*15
                dico[pho][i]+=np.log10(freq)
            for i in range(len(row[0])-1):
                biphone=tuple(row[0][i:i+2])
                if not dicoBi.has_key(biphone):
                    dicoBi[biphone]=[0.0]*15
                dicoBi[biphone][i]+=np.log10(freq)
    for key, value in dico.iteritems():
        for i,letter in enumerate(value):
            if value[i]>0 and Sum>0:
                value[i]/=Sum
    for key, value in dicoBi.iteritems():
        for i,letter in enumerate(value):
            if value[i]>0 and Sum>0:
                value[i]/=Sum
    return [dico,dicoBi]

def findTriphones(AllWordsList):
    list3=[]
    for l in AllWordsList:
        word=l[0]
        for i in range(len(word)-2):
            list3.append(tuple(word[i:i+3]))
    listFinal=list(set(list3))
    for i in listFinal:
        if list3.count(tuple(i))<100:
            listFinal.remove(i)
    return listFinal

def schema(mot,Voy,Cons):
    schema=''
    for letter in mot:
        if letter in Voy:
            schema+='V'
        elif letter in Cons:
            schema+='C'
    return schema

# pour éviter les \xc, au lieu de print l, for i in l : print i
f=codecs.open("german_lexicon.txt",encoding="utf-8")
l=f.read().encode('utf-8').splitlines()

#with open('germanWords.pkl','rb') as f:
#    [WordsList,AllWordsList,d,db,list3,dicoS]=pickle.load(f)

Voy=['a:','a','a~','E','e:','e','E:','y:','Y','y','i:','i','I','o','o:','O','U','u:','u','@','9','6','2:','?','OY','aU','aI','2:6','e:6','o:6','y:6','96','E6','u:6','E:6','O:6','i:6','I6','O6','Y6','U6','a:6','a6']

# 
Cons=['b','k','d','f','g','h','j','l','m','n','p','r','s','t','v','N','z','Z','C','ts','tS','dZ','S','x']
#
## on veut trouver la médiane des longuers de mots en allemand : 3
#WordLength=[]
#for i in l:
#    t=i.split()
#    if float(t[-1])!=0.0:
#        WordLength.append((1+t[1].count('-')))
#print np.median(WordLength)
#
## on veut trouver les schémas les plus fréquents pour les mots de 3 syll
## on commence par garder les mots de 3 syllabes
Syll3Words=[]
AllWordsList=[]
WordsList=[]
dico={}
## on trouve les 3 schémas les plus fréquents :
## CVCVCVC : vorsagen
## CVCCVCVC : zuwandern, weggeben, sublimen
## CVCVCCVC : subaltern
#
for i in l:
    t=i.split()
    f=float(t[-1])
    mot =[x for i,x in enumerate(t) if i>1 and i<len(t)-1]
    sch=schema(mot,Voy,Cons)
    if f!=0 and t[1].count('-')==2:
        dico[sch] = dico.get(sch, 0) + 1
        WordsList.append([mot,f])
    if f!=0.0:
        AllWordsList.append([mot,f])
    Syll3Words.append([t[0],mot,sch])
SchemaOk=[]
MotsSchemaOk=[]
for key in sorted(dico.items(),key=operator.itemgetter(1),reverse=True)[:3]:
    SchemaOk.append(key)

for i in Syll3Words:
    if i[2] in [x[0] for x in SchemaOk]:
        MotsSchemaOk.append(i)

[d,db]=calculatePositionalSegmentFreq(WordsList)
list3=findTriphones(AllWordsList)
# on veut extraire la fréquence des syllabes 
dicoS={}
for i in WordsList:
    wd=i[0]
    f=i[1]
    if f!=0:
        a=schema(wd,Voy,Cons)
        syll=[]
        if a=="CVCVCVC":
            syll=[wd[:2],wd[2:4],wd[4:]]
        if a=="CVCCVCVC":
            syll=[wd[:2],wd[2:5],wd[5:]]
        if a=="CVCVCCVC":
            syll=[wd[:2],wd[2:4],wd[4:]]
        for s in syll:
            dicoS[tuple(s)]=dicoS.get(tuple(s),0)+f

# à la fin, on veut 3 dico de listes
dicoSyll={"CV":[],"CVC":[],"v":[]}
for i in dicoS.items(): # TODO
    print i#,len(i[0])

with open('germanWords.pkl','wb') as f:
    pickle.dump([WordsList,AllWordsList,d,db,list3,dicoS],f,pickle.HIGHEST_PROTOCOL)
