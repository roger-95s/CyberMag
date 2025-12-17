from pydantic import BaseModel, Json
import json

class ReportsFormat(BaseModel):
    agent_name: str 
    site_name: str 
    title: str 
    url: str 
    publication_date: str   
    article_type: str  
    risk_level: str  
    executive_summary: list[str]
    sections: dict
     

# class ReportstList(BaseModel): 
#     report_card : list[ReportsFormat]

        

        
    