# fast-foodie
Creating a food API with FastAPI.

# How to run project

Have docker installed on your local machine. 

Cloned the project 

On project directory run 

- `docker build -t fastfoodie .`

The above command will build the project and all it's needed dependencies required to start the application

- `docker run -p 8000:8000 fastfoodie`

This will start the application while mapping the local machine port to the expose image port.


# Manually testing the project

Run on your terminal (powershell for windows users) the following command `curl http://localhost:8000/foods` which would return an output such as 

```bash
StatusCode        : 200                                              StatusDescription : OK                                               
Content           : {"results":["German Potatoes Slice","Gernished 
                    Peppered Snake"]}
RawContent        : HTTP/1.1 200 OK
                    Content-Length: 64
                    Content-Type: application/json
                    Date: Mon, 25 Apr 2022 02:30:36 GMT
                    Server: uvicorn

                    {"results":["German Potatoes Slice","Gernished 
                    Peppered Snake"]}
Forms             : {}
Headers           : {[Content-Length, 64], [Content-Type, 
                    application/json], [Date, Mon, 25 Apr 2022 
                    02:30:36 GMT], [Server, uvicorn]}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : System.__ComObject
RawContentLength  : 64
```

visit the api documentation on your local by visiting `http://localhost:8000/docs`


