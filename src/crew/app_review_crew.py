from crewai import Crew

from src.tasks.tasks import csv_app_store_review_tasks
from src.tasks.tasks import csv_support_email_review_tasks
from src.agents.csv_reader_agent import csv_reader_agent
from src.agents.feedback_classifier_agent import feedback_classifier_agent
from src.tasks.tasks import classify_task
from src.agents.bug_analyzer_agent import bug_analyzer_agent
from src.tasks.tasks import bug_analysis_task
from src.agents.feature_extractor_agent import feature_extractor_agent
from src.tasks.tasks import feature_extractor_task
from src.agents.ticket_creator_agent import ticket_creator_agent
from src.tasks.tasks import ticket_extractor_task
from src.agents.csv_writer_agent import csv_writer_agent
from src.tasks.tasks import csv_ticket_writer_tasks
from src.agents.quality_centric_agent import quality_centric_agent
from src.tasks.tasks import quality_check_task


from crewai import Process

def build_crew() -> Crew:
    #researcher = build_researcher()
    #tasks = build_tasks(researcher)
    csvReaderAgent = csv_reader_agent()

    csvAppStoreReviewTask =  csv_app_store_review_tasks(csvReaderAgent)
    csvSupportEmailTask =  csv_support_email_review_tasks(csvReaderAgent)

    feedbackClassifierAppStoreAgent = feedback_classifier_agent()
    feedbackClassifierAppStoreTask =  classify_task(feedbackClassifierAppStoreAgent,context_tasks=[csvAppStoreReviewTask])
    
    feedbackClassifierEmailSupportAgent = feedback_classifier_agent()
    feedbackClassifierEmailSupportTask =  classify_task(feedbackClassifierEmailSupportAgent,context_tasks=[csvSupportEmailTask])
    
    bugAnalyzerAgent = bug_analyzer_agent()
    bugAnalysisTask =  bug_analysis_task(bugAnalyzerAgent,context_tasks=[feedbackClassifierAppStoreTask,feedbackClassifierEmailSupportTask])
    
    featureExtractorAgent = feature_extractor_agent()
    featureExtractorTask =  feature_extractor_task(featureExtractorAgent,context_tasks=[feedbackClassifierAppStoreTask,feedbackClassifierEmailSupportTask])

    ticketCreatorAgent = ticket_creator_agent()
    ticketCreatorTask =  ticket_extractor_task(ticketCreatorAgent,context_tasks=[bugAnalysisTask,featureExtractorTask])

    csvTicketWriterAgent = csv_writer_agent()
    csvTicketWriterTask =  csv_ticket_writer_tasks(csvTicketWriterAgent,context_tasks=[ticketCreatorTask])
   
    qualityCheckAgent = quality_centric_agent()
    qualityCheckTask =  quality_check_task(qualityCheckAgent,context_tasks=[ticketCreatorTask])
   
    return Crew(agents=[csvReaderAgent,feedbackClassifierAppStoreAgent,feedbackClassifierEmailSupportAgent,bugAnalyzerAgent,featureExtractorAgent,ticketCreatorAgent,csvTicketWriterAgent,qualityCheckAgent], tasks=[csvAppStoreReviewTask,feedbackClassifierAppStoreTask,feedbackClassifierEmailSupportTask,bugAnalysisTask,featureExtractorTask,ticketCreatorTask,csvTicketWriterTask,qualityCheckTask], process=Process.sequential, verbose=True)
