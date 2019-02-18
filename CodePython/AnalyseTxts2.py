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
# attention, on a transformé tous les 1 en 5, et tous les 2 en 9, E en e



def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        try:
            yield line.encode('utf-8')
        except Exception as e:
            1

def openCSV(csvString,delim=''):
    with open(csvString) as csvfile:
        if delim==",":
            rd=csv.reader(utf_8_encoder(csvfile),delimiter=',')
        else:
            rd=csv.reader(utf_8_encoder(csvfile),delimiter=',')
        return rd


def transfoCSV(fSyll,WordsList,AllWordsList):
    for word in fSyll:
        print word[0]
        word[0]=word[0].replace('1','5')
        word[0]=word[0].replace('2','9')
        word[0]=word[0].replace('E','e')
    fSyll=fusion(fSyll)
    # on retrie la liste
    fSyll=sorted(fSyll, key=operator.itemgetter(1),reverse=True)
    for i,word in enumerate(WordsList):
        WordsList[i]=word.replace('1','5')
        WordsList[i]=word.replace('2','9')
        WordsList[i]=word.replace('E','e')
    for i,word in enumerate(AllWordsList):
        AllWordsList[i]=word.replace('1','5')
        AllWordsList[i]=word.replace('2','9')
        AllWordsList[i]=word.replace('E','e')
    return [fSyll,WordsList,AllWordsList]


def fusion(Array):
    sArray=[]
    for x in Array:
        L= [a[0] for a in sArray]
        if x[0] not in L:
            sArray.append(x)
        else:
            sArray[L.index(x[0])][1]+=x[1]
    return sArray

def freqSyll(csvString):
    Array=[]
    # on récupère les syllabes avec leur fréquences
    with open(csvString) as csvfile:
        rd=csv.reader(utf_8_encoder(csvfile),delimiter=',')
        for row in rd:
            Array.append([row[0],float(row[1])])  
        # on les trie par fréquence
        SortedArray=[]
        SortedArray=sorted(Array, key=operator.itemgetter(1),reverse=True)
    return SortedArray 

def ListCV(csvString):
    SyllArray=[]
    # on récupère les CV
    with open(csvString) as csvfile:
        rd=csv.reader(utf_8_encoder(csvfile),delimiter=',')
        for row in rd:
            SyllArray.append(row[0])
    return list(set(SyllArray))

def SelectCV(SortedArray,SyllArray):
    # on ne garde que les CV
    CVArray=[[],[],[]]
    for elmt in SortedArray:
        if elmt[0] in SyllArray:
            if len(elmt[0])==1:
                CVArray[0].append(elmt)
            elif len(elmt[0])==2:
                CVArray[1].append(elmt)
            else:
                CVArray[2].append(elmt)
    return CVArray

def nbPhonemes(PhonemeList,nbSyll):
    P0=PhonemeList[0]
    P1=PhonemeList[1]
    S=sum(map(lambda x:x,P1))
    #print "S",S,"cons",str('t' in P0)
    S0=0
    L=[]
    for l in P1:
        nb=min(round((float(l)**1)*nbSyll/S),S-S0)
        if 't' in P0:
            nb=min(nb,7)
        if S0<nbSyll and nb==0 :
            nb=1
        L.append(nb)
        S0+=nb
    return L

def freqCons(csvString,nbSyll):
    Pho=[[],[],[]]
    # on récupère les phonèmes consonnes avec leur fréquences
    with open(csvString) as csvfile:
        rd=csv.reader(utf_8_encoder(csvfile),delimiter=',')
        for row in rd:
            Pho[0].append(row[0])
            Pho[1].append(float(row[1]))
    YX = sorted(zip(Pho[1], Pho[0]),key=operator.itemgetter(0),reverse=True)
    PhoCons=[[y for x,y in YX],[x for x,y in YX],[]]
    #on choisit le nombre de syllabes pour chaque consonne à sélectionner
    PhoCons[2]=nbPhonemes(PhoCons,nbSyll)
    return PhoCons

def freqVoy(csvString,nbSyll):
    PhoVoy=[[],[],[]]
    # on récupère les phonèmes voyelles avec leur fréquences
    with open(csvString) as csvfile:
        rd=csv.reader(utf_8_encoder(csvfile),delimiter=',')
        for row in rd:
            PhoVoy[0].append(row[0])
            PhoVoy[1].append(float(row[1]))
    # on choisit le nombre de syllabes pour chaque voyelle a selectionner
        PhoVoy[2]=nbPhonemes(PhoVoy,nbSyll)
    return PhoVoy    
    

def SelectSyll2(PhoCons,PhoVoy,CVArray,nbSyll):
    nbCons=list(PhoCons[2])
    nbVoy=list(PhoVoy[2])
    # on en garde le bon nombre
    FinalArray=[]
    for elmt in CVArray:
        cons=elmt[0][0]
        voy=elmt[0][1]
        iC=PhoCons[0].index(cons)
        nC=nbCons[iC]
        iV=PhoVoy[0].index(voy)
        nV=nbVoy[iV]
        if nV>0 and nC>0:
            nbCons[iC]-=1
            nbVoy[iV]-=1
            FinalArray.append(elmt[0])
    # contraintes fortes, on refait une boucle pour completer les syllabes à 0
    for elmt in CVArray :
        cons=elmt[0][0]
        voy=elmt[0][1]
        iC=PhoCons[0].index(cons)
        nC=nbCons[iC]
        iV=PhoVoy[0].index(voy)
        nV=nbVoy[iV]
        if ((nV>0 and nC>-1) or (nV>-1 and nC>0)) and ((PhoCons[2][iC]==1 or PhoVoy[2][iV]==1)) and len(FinalArray)<nbSyll:
            nbCons[iC]-=1
            nbVoy[iV]-=1
            FinalArray.append(elmt[0])
    # contraintes fortes, on refait une boucle pour completer les syllabes + fréquentes
    for elmt in CVArray :
        cons=elmt[0][0]
        voy=elmt[0][1]
        iC=PhoCons[0].index(cons)
        nC=nbCons[iC]
        iV=PhoVoy[0].index(voy)
        nV=nbVoy[iV]
        if ((nV>-2 and nC>-1) or (nV>-1 and nC>-2)) and len(FinalArray)<nbSyll:
            nbCons[iC]-=1
            nbVoy[iV]-=1
            FinalArray.append(elmt[0])
    return FinalArray

def SelectSyll(CVArray,nbSyll):
    FinalArray=[[],[],[]]
    FinalArray[0]=[x[0] for x in CVArray[0][:nbSyll/9]]
    FinalArray[1]=[x[0] for x in CVArray[1][:nbSyll]]
    # on n'autorise que 4 schwa
    nbSchwa=0
    for syll in FinalArray[1]:
        if "*" in syll and nbSchwa<4:
            nbSchwa+=1
        if "*" in syll and nbSchwa==4:
            FinalArray[1].remove(syll)
    FinalArray[1]=FinalArray[1][:6*nbSyll/9]
    FinalArray[2]=[x[0] for x in CVArray[2][:2*nbSyll/9]]
    return FinalArray
 
 
def GeneratePM(FinalArray,nbSyll,LegalSchwa,BeginSchwa):
     # on génère les pseudo mots
    res=False
    nb9 = nbSyll/9
    while not res:
        ordre0=range(nb9)
        ordre1=range(6*nb9)
        ordre2=range(2*nb9)
        random.shuffle(ordre0)
        random.shuffle(ordre1)
        random.shuffle(ordre2)
        Mots=[]
        for i in range(nb9): #CVCVCV
            Mots.append(FinalArray[1][ordre1[3*i]]+FinalArray[1][ordre1[3*i+1]]+FinalArray[1][ordre1[3*i+2]])
        for i in range(nb9): # VCVCVC
            Mots.append(FinalArray[0][ordre0[i]]+FinalArray[1][ordre1[i+nb9*3]]+FinalArray[2][ordre2[i]])
        for i in range(nb9): #CVCVCVC
            Mots.append(FinalArray[1][ordre1[2*i+nb9*4]]+FinalArray[1][ordre1[2*i+nb9*4+1]]+FinalArray[2][ordre2[i+nb9]])
        res=ContraintesPM(Mots,LegalSchwa,BeginSchwa)
    return Mots   
   
def ContraintesPM(Mots,LegalSchwa,BeginSchwa):
    for mot in Mots:
        if re.match("G.*|.+(@|5)(n|m).*",mot):
            return False
        elif mot[-1]=="*":
            return False
        elif mot.count("*")==2:
            return False
        elif mot.count("*")==1:
            id=mot.index("*")
            schema=mot[id-1:id+2]
            if id==1:
                if schema not in BeginSchwa:
                    return False
            else:
                if schema not in LegalSchwa:
                    return False
    return True

def LegSchwa(WordsList):
    LegalSchwa=[]
    BeginSchwa=[]
    for i,word in enumerate(WordsList):
        if "*" in word :
            id=word.index("*")
            if id!=0 and id!= len(word)-1 :
                LegalSchwa.append(word[id-1:id+2])
            if id==1:
                BeginSchwa.append(word[0:3])
    SetLegalSchwa=list(set(LegalSchwa))
    SetBeginSchwa=list(set(BeginSchwa))
    for i in SetLegalSchwa:
        if LegalSchwa.count(i)<500:
            SetLegalSchwa.remove(i)
    for i in SetBeginSchwa:
        if BeginSchwa.count(i)<500:
            SetBeginSchwa.remove(i)
    return [SetLegalSchwa,SetBeginSchwa]
  
def extractCVCVCVWords(csvString):
      # on extrait les mots de la base CVCVCV
    WordArray=[]
    # on récupère les syllabes avec leur fréquences
    with open(csvString) as csvfile:
        rd=csv.reader(utf_8_encoder(csvfile),delimiter=',')
        for row in rd:
            WordArray.append(row[0])
    return WordArray            
    
def extractAllWords(csvString):
    f=codecs.open(csvString,"r",encoding="utf-8")
    l = f.read().encode('utf-8').splitlines()
    for i,mot in enumerate(l):
        l[i]=mot[:-1]
    return l         

def calcDist(Mots,AllWordsList,nbSyll):
    nb9=nbSyll/9
    # on calcule leur distance de Levenshtein min avec la base
    WordDist=[]
    for i,mot in enumerate(Mots) :# pseudo-mots
        minD=1000000
        minWord=''
        nbD=0
        for word in AllWordsList:# base
            d=distance.levenshtein(mot,word)
            if d<minD:
                minD=d
                minWord=word
                nbD=1
            elif d==minD:
                nbD+=1
        WordDist.append([mot,minWord,minD,nbD])
    distList=[x[2] for x in WordDist]
    # nombre le plus commun
    [dist,nb]=Counter(distList).most_common(1)[0]
    if nb<12:
        return -1
    L1= distList[0:nb9]
    L2= distList[nb9:2*nb9]
    L3= distList[2*nb9:3*nb9]
    if L1.count(dist)<4 or L2.count(dist)<4 or L3.count(dist)<4:
        return -1 
    L1Res=[x for x in WordDist[0:nb9] if x[2]==dist]
    L2Res=[x for x in WordDist[nb9:2*nb9] if x[2]==dist]
    L3Res=[x for x in WordDist[2*nb9:3*nb9] if x[2]==dist]
    return L1Res+L2Res+L3Res

# évaluation au moment de choisir les 60 et lorsqu'on en garde que 36
def evalScore(CVArray,tab,nb,PositionalSegmentFreq):
    # liste des mots choisis
    liste=[x[0] for x in tab]
    nbDist=[x[3] for x in tab]
    WordsConcat=''.join(liste)
    freq=sum(map(WordSegmentFreq,liste))
   # évaluation des fréquences des syllabes
    #SumFreq=sum([x[1] for x in CVArray[:nb]]) 
    #SumSyll=sum([x[1] for x in CVArray if x[0] in WordsConcat])
    Q=1#-SumSyll/SumFreq
    var=np.var(nbDist)
    return [var,freq/fMoy*6]#,fC,fV,Q]


def calculatePositionalSegmentFreq():
    dico={}
    for i in ['R','a','e','l','s','i','*','t','d','k','p','O','@','m','n','y','6','v','j','u','f','b','Z','5','z','w','g','S','9','8','2','?','N','h','G','o','r','c','x']:
        dico[i]=[0]*7
    with open("MotsCV3Schemas.csv") as csvfile:
        rd=csv.reader(utf_8_encoder(csvfile),delimiter=',')
        for row in rd:
            if row[0]!="phon":
                freq=row[3]
                for i,pho in enumerate(row[0]):
                    pho.replace('1','5')
                    pho.replace('2','9')
                    dico[pho][i]+=float(freq)
    return dico

def WordSegmentFreq(mot):
    res=0
    for i,pho in enumerate(mot):
        res+=PositionalSegmentFreq[pho][i]
    return res

def freqMoy(dico):
    somme=0
    for cle in dico:
        somme+=sum(dico[cle])
    somme/=len(dico)
    return somme

PositionalSegmentFreq=calculatePositionalSegmentFreq()
fMoy=freqMoy(PositionalSegmentFreq)
print fMoy*6
#### Main
nbSyll=72
nbList=1
# mots de la base en CVCVCV
WordsList1=extractCVCVCVWords('MotsCV.csv')
WordsList=extractAllWords('motsCVCVCV.txt')
# tous les mots de la base
AllWordsList=extractAllWords('BaseLexique/Mots.txt')
# liste des syllabes avec leur fréquence, séparée en 3 groupes
fSyll=freqSyll('FrequencesSyllabes.csv')
# on fusionne les sons non contrastés
#TODO a remettre [fSyll,WordsList,AllWordsList]=transfoCSV(fSyll,WordsList,AllWordsList)
## On ne garde que les CV
SyllArray=ListCV('Syllabes3Schemas.csv')
## on les associe avec leur fréquence, toujours liste de 3 listes
CVArray=SelectCV(fSyll,SyllArray)
## fréquence des consonnes + nombre à choisir
fCons=freqCons('FreqConsonnes.csv',nbSyll)
## fréquence des voyelles + nombre à choisir
fVoy=freqVoy('FreqVoyelles.csv',nbSyll)
## syllabes utilisées pour créer les pseudo-mots
FinalArray=SelectSyll(CVArray,nbSyll)
## evaluation des syllabes retenues
[LegalSchwa,BeginSchwa]=LegSchwa(WordsList)
##print evalScore(fCons,fVoy,CVArray,FinalArray,60)
### génération des pseudos mots
for n in range(10):
    MotsOpti=[]
    ErreurOpti=1500
    distOpti=0
    for i in range(10):
        Mots=GeneratePM(FinalArray,nbSyll,LegalSchwa,BeginSchwa)
        # on calcule les distances, on garde tous les mots à bonne distance
        Li=calcDist(Mots,WordsList1,nbSyll)
        #print Li
        if Li!=-1:
            ev=evalScore(CVArray,[x for x in Li],36,PositionalSegmentFreq)
            print ev
            if ev[0]<ErreurOpti and ev[0]>0:
                distOpti=Li[1]
                ErreurOpti=list(ev)
                MotsOpti=list(Li)

    print ErreurOpti
    print "\n"
    print MotsOpti
    print "\n \n"
    #print "fVoy",fVoy

