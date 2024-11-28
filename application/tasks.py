# from celery import shared_task
# from .models import ServiceRequest, User, Role, Service
# import flask_excel as excel
# from .mail_service import send_message,send_report
# from jinja2 import Template

# @shared_task(ignore_result=False)
# def create_service_request_csv():
#     service_requests = ServiceRequest.query.all()
    
#     csv_output = excel.make_response_from_query_sets(service_requests, ["id", "service_id", "customer_id", "professional_id", "date_of_request", "date_of_completion", "rating", "remarks", "service_status"], "csv")
#     filename="test.csv"
    
#     with open(filename, 'wb') as f:
#         f.write(csv_output.data)

#     return filename

# @shared_task(ignore_result=True)
# def daily_reminder(subject):
#     service_requests = ServiceRequest.query.filter_by(service_status='requested').all()
#     if (len(service_requests) != 0):
#         professionals = User.query.filter(User.roles.any(Role.name == 'professional')).all()
#         for professional in professionals:
#             send_message(professional.email, subject, 'Hello Service Professional,\n\nYou have pending service requests.\nPlease visit the application to accept/reject the service requests.\n\nRegards,\nA to Z Household Services')
#         return "OK"
    
# @shared_task(ignore_result=True)
# def monthly_reminder(subject):
#     service_requests = ServiceRequest.query.filter_by(service_status='requested').all()
#     service_closed = ServiceRequest.query.filter_by(service_status='requested').all()
#     all_service_requests = ServiceRequest.query.all()
#     service_ids = []
#     for service_request in all_service_requests:
#         service_ids.append(service_request.service_id)
#     most_frequnt = max(set(service_ids), key=service_ids.count)
#     services = Service.query.all()
#     if (len(service_requests) != 0):
#         customers = User.query.filter(User.roles.any(Role.name == 'customer')).all()
#         for customer in customers:
#             with open('/home/dominatrix/Codes/Household_Services_Application_v2/application/test.html', 'r') as f:
#                 template = Template(f.read())
#                 send_report(customer.email, subject, template.render(email=customer.email,request=len(all_service_requests),close=len(service_closed),service_requests=all_service_requests,services=services, high=most_frequnt))
#         return "OK"


from celery import shared_task
from .models import ServiceRequest, User, Role, Service
import flask_excel as excel
from .mail_service import send_message, send_report
from jinja2 import Template
from collections import Counter
from typing import List, Optional

@shared_task(ignore_result=False)
def create_service_request_csv() -> str:
    """
    Generates a CSV report of all service requests in the system.
    Returns the filename of the generated CSV.
    
    The CSV includes key service request fields like IDs, dates, ratings, and status.
    """
    # Define fields to be exported
    export_fields = [
        "id", "service_id", "customer_id", "professional_id",
        "date_of_request", "date_of_completion", "rating",
        "remarks", "service_status"
    ]
    
    # Fetch all service requests and generate CSV response
    all_requests = ServiceRequest.query.all()
    csv_response = excel.make_response_from_query_sets(
        all_requests, 
        export_fields, 
        "csv"
    )
    
    # Save CSV to disk
    output_file = "test.csv"
    with open(output_file, 'wb') as file:
        file.write(csv_response.data)
    
    return output_file

@shared_task(ignore_result=True)
def daily_reminder(subject: str) -> Optional[str]:
    """
    Sends daily reminders to all professionals about pending service requests.
    Returns "OK" if reminders were sent, None if no pending requests exist.
    
    Args:
        subject: Email subject line for the reminder
    """
    # Get all pending service requests
    pending_requests = ServiceRequest.query.filter_by(
        service_status='requested'
    ).all()
    
    if not pending_requests:
        return None
        
    # Find all professionals in the system
    professionals = User.query.filter(
        User.roles.any(Role.name == 'professional')
    ).all()
    
    # Compose reminder message
    reminder_message = (
        'Hello Service Professional,\n\n'
        'You have pending service requests.\n'
        'Please visit the application to accept/reject the service requests.\n\n'
        'Regards,\nA to Z Household Services'
    )
    
    # Send reminders to all professionals
    for professional in professionals:
        send_message(professional.email, subject, reminder_message)
        
    return "OK"

@shared_task(ignore_result=True)
def monthly_reminder(subject: str) -> Optional[str]:
    """
    Sends monthly report emails to all customers with service request statistics.
    Returns "OK" if reports were sent, None if no data exists.
    
    Args:
        subject: Email subject line for the monthly report
    """
    # Gather all necessary service request data
    pending_requests = ServiceRequest.query.filter_by(
        service_status='requested'
    ).all()
    closed_requests = ServiceRequest.query.filter_by(
        service_status='requested'
    ).all()
    all_requests = ServiceRequest.query.all()
    
    if not pending_requests:
        return None
    
    # Find most requested service using Counter
    service_request_counts = Counter(
        request.service_id for request in all_requests
    )
    most_requested_service = service_request_counts.most_common(1)[0][0]
    
    # Get all services for reference
    services = Service.query.all()
    
    # Get all customers
    customers = User.query.filter(
        User.roles.any(Role.name == 'customer')
    ).all()
    
    # Load email template
    template_path = '/home/dominatrix/Codes/Household_Services_Application_v2/application/test.html'
    with open(template_path, 'r') as template_file:
        email_template = Template(template_file.read())
    
    # Send personalized report to each customer
    for customer in customers:
        report_context = {
            'email': customer.email,
            'request': len(all_requests),
            'close': len(closed_requests),
            'service_requests': all_requests,
            'services': services,
            'high': most_requested_service
        }
        
        rendered_report = email_template.render(**report_context)
        send_report(customer.email, subject, rendered_report)
        
    return "OK"