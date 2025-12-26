from pydantic import BaseModel, Json
import json

class ReportsFormat(BaseModel):
    site_name: str 
    title: str 
    url: str 
    publication_date: str   
    article_type: str  
    risk_level: str  
    summary: list[str]
    sections: list[dict]
     

# class ReportstList(BaseModel): 
#     report_card : list[ReportsFormat]
