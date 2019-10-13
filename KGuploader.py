#!/usr/bin/env python
# coding: utf-8

# In[2]:


#https://metacademy.org/graphs/api/v1/graph/w5br4vvq/?format=json
from tkinter import *
import json
import urllib
from urllib.request import urlopen
import xlsxwriter
import re

window=Tk()

def kg_creation():
    with open("ByjusgraphIdsList.txt", "w") as myfile:
        myfile.write(e1_value.get())

    graphIdsFile='ByjusgraphIdsList.txt'
    f = open(graphIdsFile)
    graphids = f.readlines()
    #http://52.77.223.93/graphs/api/v1/graph/94hgntze/?format=json
    baseurl = "http://52.77.223.93"
    bridgeurl = "/graphs/api/v1/graph/"
    KGWorkbook = xlsxwriter.Workbook(e2_value.get()+".xlsx")
    for graph in graphids:
        graphfetchurl=baseurl+bridgeurl+graph.strip()+'/?format=json'
        print (graphfetchurl)
        response = urlopen(graphfetchurl)
        data = json.loads(response.read())
        graphTitle=data['title']
        #print '****',graphTitle
        graphCanonicalId=graphTitle.split('_')[0]
        graphCanonicalTitle=graphTitle.split('_')[1]
        #print '****',graphTitle, graphCanonicalId, graphCanonicalTitle
        safeTitle=re.sub(r'\W+', '', graphTitle)
        worksheetNodes = KGWorkbook.add_worksheet("Nodes"+safeTitle[:25])
        worksheetRelations=KGWorkbook.add_worksheet("Edges"+safeTitle[:25])
        coceptIdDict={}
        row=0
        col=0
        header=['conceptName','conceptMetaAcadId','contentTeamConceptId','conceptCanonicalName','conceptPedOrder','description','conceptTags','isExternal','conceptSubtopicID']
        for elem in header:
                worksheetNodes.write(0,col,elem)
                col=col+1
        row = 1
        col = 0
        for conceptId in data['concepts']:
            concept_response = urlopen(baseurl + conceptId)
            concept_data=json.loads(concept_response.read())
            #print concept_data
            conceptMetaAcadId=concept_data['id']
            conceptCanonicalName=concept_data['title'].strip()
            conceptName=conceptCanonicalName.split('$_')[0]
            if conceptCanonicalName.count('$_')==0:
                conceptPedOrder="PED Order Missing"
            else:
                conceptPedOrder=conceptCanonicalName.split('$_')[1].split('_')[0]
            isExternal=False
            if '$_e' in conceptCanonicalName.lower() or '_e' in conceptCanonicalName.lower() :
                isExternal=True
            coceptIdDict[conceptMetaAcadId]=conceptName
            description=''
            conceptTags=''
            if '$_' in concept_data['summary'] and len(concept_data['summary'])>15 :
                description=concept_data['summary'].split('$_')[1].strip()
                if len(description)<=3:
                    description= 'No Description'
                if concept_data['summary'].count('$_')>=2:
                    conceptTags=concept_data['summary'].split('$_')[2].strip()
                if concept_data['summary'].count('$_')>=2:
                    conceptSubtopicID=concept_data['summary'].split('$_')[3].strip()
                else:
                    conceptTags='No Tags'
            else:
                description= 'No Description'
                conceptTags='No Tags'
            contentTeamConceptId=graphCanonicalId.strip()+'C'+conceptPedOrder
            payload= [conceptName,conceptMetaAcadId,contentTeamConceptId,conceptCanonicalName,conceptPedOrder,description,conceptTags,isExternal,conceptSubtopicID]
            col = 0
            for elem in payload:
                worksheetNodes.write(row,col,elem)
                col=col+1
            row=row+1
        row=0
        col=0
        header=['edgeMetaAcadId', 'edgeSourceId', 'edgeTargetId','sourceNodeName','targetNodeName']
        for elem in header:
                worksheetRelations.write(0,col,elem)
                col=col+1
        row = 1
        col = 0
        for edgeId in data['dependencies']:
            edge_response = urlopen(baseurl + edgeId)
            edge_data=json.loads(edge_response.read())
            edgeMetaAcadId=edge_data['id']
            edgeSourceId=edge_data['source'].split('/')[-2]
            edgeTargetId=edge_data['target'].split('/')[-2]
            payload= [edgeMetaAcadId, edgeSourceId, edgeTargetId,coceptIdDict[edgeSourceId],coceptIdDict[edgeTargetId]]
            col = 0
            for elem in payload:
                worksheetRelations.write(row,col,elem)
                col=col+1
            row=row+1

    KGWorkbook.close()
b1=Button(window,text="Create",command=kg_creation)
b1.grid(row=2,column=1)
e1_value=StringVar()
e1=Entry(window,textvariable=e1_value)
e1.grid(row=0,column=1,padx=10,pady=10)
e1=Label(window,text="Enter 8 character GraphID from Metacademy url")
e1.grid(row=0,column=0,padx=10,pady=10)
e2_value=StringVar()
e2=Entry(window,width=50,textvariable=e2_value)
e2.grid(row=1,column=1,padx=10,pady=10)
e2=Label(window,text="Enter ChapterName from Metacademy")
e2.grid(row=1,column=0,padx=10,pady=10)

window.mainloop()
    #print data
#https://metacademy.org/graphs/api/v1/graph/w5br4vvq/?format=json


# In[ ]:
