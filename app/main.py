from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pathlib
# so they can be run regardless of location (it was annoying me during testing)
try: import sql_init as sql; import sql_query
except: from . import sql_init as sql; from . import sql_query

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["POST"],
    allow_headers=['*']
)

@app.get("/", response_class=HTMLResponse)
async def display_form():
    # route to HTML file, then put up contents on page
    html_file = pathlib.Path(__file__).parent / "application.html"
    with open(html_file, "rt", encoding="utf-8") as html_content:
        return HTMLResponse(content=html_content.read(), status_code=200)

@app.post("/api/post")
async def return_data_for_query(data: dict): 
    # isolate type, get classes for initialization
    data_variety = data["form-type"].split('-')[0].title()
    class_dict = sql_query.construct_class_init_dict(sql_query.Search_Params)

    # now unneeded, so removing before giving data to sql_query.py
    del data["form-type"]
    # make keys lowercase so that data can be unpacked into optional arguments and replace
    # spaces with underscores (data_quality, not Data Quality as given by s-text-field labels)
    data = {('_'.join(k.split(' ')).lower() if type(k) == str else k): v for k, v in data.items()}
    # know that I did not choose the below naming choice; blame Discogs and their dump
    if data.get("real_name") != None:
        data["realname"] = data.pop("real_name")
    
    # then query the database with the appropriate parameters
    requested_data = sql_query.read_items(class_dict[data_variety](**data))

    # FastAPI automatically turns Python dictionaries into JSON, so no need to change
    return requested_data