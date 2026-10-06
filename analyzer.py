import ollama


def analyze_student(student_data):

    prompt = f"""
You are an AI Student Performance Analyzer.

Analyze the following student's academic information.

Student Name:
{student_data['name']}

Subjects and Marks:
{student_data['subjects']}

Attendance:
{student_data['attendance']}%

Average Study Hours:
{student_data['study_hours']} hours/day

Strengths:
{student_data['strengths']}

Weaknesses:
{student_data['weaknesses']}

Give a clear and student-friendly analysis.

Include:

1. Overall performance
2. Strong subjects
3. Weak subjects
4. Attendance analysis
5. Study habit analysis
6. Main problems affecting performance
7. Personalized improvement plan
8. Suggested daily study schedule
9. Tips to improve weak subjects
10. Motivation

Do not invent marks that were not provided.

Keep the answer practical and easy to understand.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]