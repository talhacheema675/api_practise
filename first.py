from fastapi import FastAPI

app=FastAPI() #create object with name app 
@app.get("/") #define the route of app
def hello():
    return {'message':'helloworld'}
@app.get("/about")
def about():
    return {'message':'it is an AI campus'}