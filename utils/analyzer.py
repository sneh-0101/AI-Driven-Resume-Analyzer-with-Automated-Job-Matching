import re

class ResumeAnalyzer:
    def __init__(self, resume_data, job_description=""):
        self.resume_data = resume_data
        self.job_description = job_description
        self.common_keywords = ["python", "flask", "javascript", "sql", "aws", "docker", "react", "rest api", "git"]

    def calculate_ats_score(self):
        score = 0
        text = self._get_full_text()
        
        # Check for essential sections
        if self.resume_data.get('summary'): score += 10
        if self.resume_data.get('skills'): score += 20
        if self.resume_data.get('experience'): score += 20
        
        # Keyword matching
        found_keywords = []
        for kw in self.common_keywords:
            if kw.lower() in text.lower():
                score += 5
                found_keywords.append(kw)
        
        return min(score, 100), found_keywords

    def generate_interview_questions(self):
        skills = self.resume_data.get('skills', [])
        questions = []
        for skill in skills[:3]: # Top 3 skills
            questions.append(f"Can you describe a challenging project where you used {skill}?")
            questions.append(f"What are the best practices you follow when working with {skill}?")
        return questions

    def _get_full_text(self):
        data = self.resume_data
        text = f"{data.get('full_name')} {data.get('summary')} {' '.join(data.get('skills', []))}"
        return text
