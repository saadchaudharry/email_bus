import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMessage

@csrf_exempt
def send_mail_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subject = data.get('subject', '')
            message = data.get('message', '')
            html_message = data.get('html_message', None)
            from_email = data.get('from_email', 'noreply@example.com')
            recipient_list = data.get('recipient_list', [])
            
            if not subject or not message or not recipient_list:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            send_mail(subject, message, from_email, recipient_list, html_message=html_message)
            return JsonResponse({'message': 'Email sent successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def email_message_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subject = data.get('subject', '')
            body = data.get('body', '')
            from_email = data.get('from_email', 'noreply@example.com')
            to = data.get('to', [])
            is_html = data.get('is_html', False)
            
            if not subject or not body or not to:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            email = EmailMessage(subject, body, from_email, to)
            if is_html:
                email.content_subtype = "html"
            email.send()
            return JsonResponse({'message': 'Email message sent successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
