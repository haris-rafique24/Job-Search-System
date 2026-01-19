import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, PDFSearchTool

# Set your API Keys
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPER_API_KEY"] = "5eb787e895d26e51f754031e92f0e55d73077172"

# 1. Initialize Tools
# This tool will index your PDF and allow the agent to query it
resume_search_tool = PDFSearchTool(pdf='Haris Rafique - Software Engineer.pdf')
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# 2. Define specialized Agents
researcher = Agent(
    role='Job Market Researcher',
    goal='Identify the top 3 job postings for {job_title} in {location}',
    backstory='Expert at parsing job boards and identifying high-growth companies.',
    tools=[search_tool, scrape_tool],
    verbose=True,
    allow_delegation=False
)

strategist = Agent(
    role='Career Strategist',
    goal='Analyze job descriptions and compare them against the candidate resume',
    backstory='Specialist in identifying skill gaps and cultural alignment.',
    tools=[resume_search_tool],
    verbose=True
)

writer = Agent(
    role='Resume Engineer',
    goal='Create a high-impact, ATS-optimized resume summary and experience section',
    backstory='Professional technical writer who knows how to bypass automated filters.',
    tools=[resume_search_tool],
    verbose=True
)

# 3. Define the Workflow Tasks
search_task = Task(
    description='Find 3 active job postings for {job_title} in {location}. Extract the full text of the best one.',
    expected_output='The full job description and company name of the best matching role.',
    agent=researcher
)

analysis_task = Task(
    description='Compare the job description with the candidate resume. Identify top 5 keywords missing from the resume.',
    expected_output='A list of keywords and a strategy on how to pivot the resume experience.',
    agent=strategist,
    context=[search_task]
)

writing_task = Task(
    description='Rewrite the "Professional Summary" and "Work Experience" sections of the resume to align with the job.',
    expected_output='A markdown formatted document containing the rewritten resume sections.',
    agent=writer,
    context=[analysis_task, search_task],
    output_file='tailored_resume_output.md'
)

# 4. Form the Crew
job_search_system = Crew(
    agents=[researcher, strategist, writer],
    tasks=[search_task, analysis_task, writing_task],
    process=Process.sequential, # Tasks run one after another
    verbose=True
)

# 5. Execute
print("### Starting the Multi-Agent Job Search System ###")
result = job_search_system.kickoff(
    inputs={
        'job_title': 'Python Engineer',
        'location': 'Remote'
    }
)

print("\n\n########################")
print("## FINAL TAILORED CONTENT ##")
print("########################\n")
print(result)