from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

# CivilComplaints 데이터 스키마

class CivilComplaints(BaseModel):
    Gu: str
    doc_id: int
    answer_url: str
    title: Optional[str]  # Make title Optional to allow None
    request_content: Optional[str]  # Make request_content Optional to allow None
    attached_file: List[Dict[str, Optional[int]]]  # 이미지 파일들을 리스트로 처리
    answer: Optional[str]  # Make answer Optional to allow None
    answer_summary: Optional[str]  # Make answer_summary Optional to allow None
    extraced_reference: Optional[str]  # Make extraced_reference Optional to allow None
    date: datetime
    dept: str
    state: str
    note: Optional[str]  # Make note Optional to allow None

    class Config:
        # 날짜 형식 지정
        json_encoders = {
            datetime: lambda v: v.isoformat()  # datetime을 isoformat 문자열로 변환
        }



# GuOffice 데이터 스키마
class GuOffice(BaseModel):
    Gu: str
    url: str
    depts: Dict[str, str]  # 부서 정보는 카테고리와 부서 코드로 이루어진 딕셔너리

    class Config:
        # 날짜 형식 지정 (필요한 경우 추가)
        json_encoders = {
            datetime: lambda v: v.isoformat()  # datetime을 isoformat 문자열로 변환
        }


