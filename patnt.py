from fastapi import FastAPI,Path,HTTPException,Query
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

class Patient(BaseModel):
    
    id:str
    name: Annotated[str, Field(...,title='patient name',description='write patient name',example="talha cheema")]
    #... inicate that field are compulsory
    city:str
    age:int
    gender:Annotated[Literal['male','female','other'],Field(description='write the gender of patient')]
    height:int
    weight:int
    
    @computed_field
    @property
    def calculte(self)->float:
        bmi=self.weight/(self.age**2)
        return bmi

    @computed_field
    @property
    def calverdict(self)->str:
        if self.weight>80:
            return "overweight"
        elif self.weight<60:
            return "underweight"

        else: return "fit"


class Pat_update(BaseModel):
    
    id:str
    name: Annotated[Optional[str], Field(title='patient name',description='write patient name',example="talha cheema")]
    #... inicate that field are compulsory
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Literal['male','female','other']] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    



def loaddata():
    with open('patients.json','r') as f: #open file in read mode as we put "r" at end
         data=json.load(f)
         return data
         #filter_data=[]
         #for patient in data.values():
          #  filter_data.append({"name": patient["name"],"age":patient["age"],"city":patient["city"]})
         #return filter_data

def savedata(data):
    with open('patients.json','w')as f:
        json.dump(data,f) #f indicate to dump data in file
    return JSONResponse(status_code=201, content={'message':'data added successfully'})


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hmpage():
    return {'message':'welcome to patient management system'}


@app.get("/about")
def abtt():
    return {'message':'this is the satete of the art patient management systen'}


@app.get("/view")
def aview():
    data=loaddata()
    return data

@app.get("/patientview/{s}")#name must be same as function below as "s" also in below function
def view_patient(s:str=Path(description='id of patient', example='P001')):
    data=loaddata()
    if s in data:
        return data[s]
    else:#print("not found")
        raise HTTPException(status_code=404, detail='patient not found')


@app.get("/sort_patient")
def sorte(sortby:str=Query(description='how to sort it'),sortorder:str=Query('asc',description='sort in ascending')):
    valid_filed=['height','weight', 'bmi','age']
    validsort=['asc','desc']
    data=loaddata()
    if sortby not in valid_filed:
        raise HTTPException(status_code=400, detail=f'invalid selection select from {valid_filed}')
    if sortorder not in validsort:
        raise HTTPException(status_code=400, detail=f'invalid sort selection select from {validsort}')
    sortans= True if sortorder=='desc' else False
    sorteddata =sorted(data.values(), key=lambda x: x.get(sortby, 0), reverse=sortans)
    return sorteddata

   


@app.post('/create')
def create_pat(patient:Patient):
    data=loaddata()
    if patient.id in data: #check if id already present
        raise HTTPException(status_code=400, detail="patient id alredy exist")
    data[patient.id]=patient.model_dump(exclude=['id']) #load data
    savedata(data)


@app.put('/edit/{patient_id}')
def update_pat(patient_id:str, patient_upt:Pat_update):
    data=loaddata()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")
    infor=data[patient_id]
    #infor is dict but patient_upt is pydantic object so convet latter into former to work on it 
    newinfo=patient_upt.model_dump(exclude_unset=True) #leave those value which not set by clinet
    for key, value in newinfo.items():
        infor[key]=value
    #infro->Pydantic object ->updated bmi and verdict->pydantic object ->dict 
    infor['id']=patient_id
    patpydobj=Patient(**infor)
    infor=patpydobj.model_dump(exclude=['id'])
    data[patient_id]=infor
    savedata(data) 
    return JSONResponse(status_code=200, content="patient info updated")


@app.delete('/delete/{patient_del}')
def deletpat(patient_del:str):
    data=loaddata()
    if patient_del not in data:
        raise HTTPException(status_code=404, detail='patient nor exist')
    del data[patient_del]
    savedata(data)
    return JSONResponse(status_code=200,content='update successfully')






