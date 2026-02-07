from crewai import Task

def build_tasks(researcher):
    return [
        Task(
            description="Explain Steep Gold Rate Increase in India Market 2024-2025, Is it good to invest now ? ",
            expected_output="5 bullets, simple language.",
            agent=researcher,
        )
    ]

def csv_app_store_review_tasks(agent):
        return Task(
            description='Read "app_store_reviews.csv" and extract all text.',
            expected_output='Raw text summary of the CSV.',
            agent=agent
        )

def csv_support_email_review_tasks(agent):
        return Task(
            description='Read "app_store_reviews.csv" and extract all text.',
            expected_output='Raw text summary of the CSV.',
            agent=agent
        )

def classify_task(agent, context_tasks):
        return Task(
            description='Analyze feedback. Categorize as Bug/Feature/Spam. Add confidence scores.',
            expected_output='Filtered list of non-spam feedback with categories.',
            agent=agent,
            context=context_tasks 
        )



def bug_analysis_task(agent, context_tasks):
        return Task(
            description='Focus ONLY on "Bug" AND "Complaint" items. Extract Device/OS and Severity with confidence scores',
            expected_output='Extracts technical details: steps to reproduce, platform info, severity assessment',
            agent=agent,
            context=context_tasks
        )

def feature_extractor_task(agent, context_tasks):
        return Task(
            description='Focus ONLY on "Feature Requests". Estimate Business Value.',
            expected_output='List of potential features with value estimation.',
            agent=agent,
            context=context_tasks
        )

def ticket_extractor_task(agent, context_tasks):
        return Task(
            description='Format the analysis into Jira-style tickets: source_id, source_type, category, priority, technical_details, suggested_title',
            expected_output=' "Categories: Bug, Feature Request, Praise, Complaint, Spam" , "Priorities: Critical, High, Medium, Low" , "Technical details: For bugs, include device info, reproduction steps " ,"Suggested titles: Clear, actionable ticket titles" ',
            agent=agent,
            context=context_tasks
        )

def csv_ticket_writer_tasks(agent,context_tasks):
        return Task(
            description='Write CSV content to "expected_classifications.csv"',
            expected_output='Confirmation of file name and save status.',
            agent=agent,
            context=context_tasks
        )

def quality_check_task(agent,context_tasks):
        return Task(
            description='Reviews generated tickets for completeness and accuracy',
            expected_output='Summary of review with ticket Id , title , quality check score',
            agent=agent,
            context=context_tasks
        )