from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app= FastAPI()


students = {
    "S001":{"name":"Himanshu", "marks":85, "grade": "A"},
    "S002":{"name":"Atul", "marks":90, "grade": "A+"},
    "S004":{"name":"Saanvi", "marks":95, "grade": "A+"}
}


class MarksSubmission(BaseModel):
    student_id: str
    marks: int
    subject: str 
    
    
@app.get("/student/{student_id}")
def get_student(student_id: str):
    
    
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail=f"student with ID {student_id} does not exist"
        )
        
    return students[student_id]

@app.post("/submit-marks")
def submit_marks(submission: MarksSubmission):
    
    if submission.student_id not in students:
        raise HTTPException(
            status_code=400,
            detail = f"student with ID {submission.student_id}"
        )
        
    if submission.marks < 0 and submission.marks > 100:
        raise HTTPException(
            status_code= 400,
            detail= {
                "error": "marks must be 0 between 100",
                "marks_received": submission.marks,
                "fix": "Enter a valid value 0 between 100"
            }
        )
        
    if submission.subject.strip() == "":
        
        raise HTTPException(
            status_code= 400,
            detail= "Subject name cannot be empty"
        )
        
    try:     
        students[submission.student_id]["marks"] = submission.marks
    
        return {
                "message": "marks submitted successfully",
                "student": students[submission.student_id]["name"],
                "subject": submission.subject,
                "marks": submission.marks
            }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Something went to wrong on our side: {str(e)}"
        )
       