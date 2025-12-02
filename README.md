# Email Bus

A Django project for sending emails via a JSON API.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install django
    ```

3.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```

4.  **Start the server:**
    ```bash
    python manage.py runserver
    ```

## API Documentation

The API exposes Django's email functionality via HTTP POST requests.

### Send Mail

*   **Endpoint:** `/api/send-mail/`
*   **Method:** `POST`
*   **Content-Type:** `application/json`
*   **Payload:**

    | Field | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `subject` | string | Yes | The subject of the email. |
    | `message` | string | Yes | The plain text body of the email. |
    | `html_message` | string | No | The HTML body of the email. |
    | `from_email` | string | No | The sender's email address. Defaults to `noreply@example.com`. |
    | `recipient_list` | array | Yes | A list of recipient email addresses. |

    **Example:**
    ```json
    {
        "subject": "Email Subject",
        "message": "Email Body",
        "html_message": "<h1>Email Body</h1>",
        "from_email": "sender@example.com",
        "recipient_list": ["recipient@example.com"]
    }
    ```

*   **Success Response:**
    *   **Code:** 200
    *   **Content:** `{"message": "Email sent successfully"}`

*   **Error Responses:**
    *   **Code:** 400 Bad Request
        *   **Content:** `{"error": "Missing required fields"}`
    *   **Code:** 405 Method Not Allowed
        *   **Content:** `{"error": "Invalid request method"}`

### Email Message

*   **Endpoint:** `/api/email-message/`
*   **Method:** `POST`
*   **Content-Type:** `application/json`
*   **Payload:**

    | Field | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `subject` | string | Yes | The subject of the email. |
    | `body` | string | Yes | The body of the email. |
    | `is_html` | boolean | No | Set to `true` if `body` contains HTML. Defaults to `false`. |
    | `from_email` | string | No | The sender's email address. Defaults to `noreply@example.com`. |
    | `to` | array | Yes | A list of recipient email addresses. |

    **Example:**
    ```json
    {
        "subject": "Email Subject",
        "body": "<h1>Email Body</h1>",
        "is_html": true,
        "from_email": "sender@example.com",
        "to": ["recipient@example.com"]
    }
    ```

*   **Success Response:**
    *   **Code:** 200
    *   **Content:** `{"message": "Email message sent successfully"}`

*   **Error Responses:**
    *   **Code:** 400 Bad Request
        *   **Content:** `{"error": "Missing required fields"}`
    *   **Code:** 405 Method Not Allowed
        *   **Content:** `{"error": "Invalid request method"}`

## Configuration

Currently, the project is configured to use the **Console Backend** for emails. This means sent emails will appear in the terminal output where the server is running, instead of being actually sent.

To change this, update `EMAIL_BACKEND` in `email_bus/settings.py`.
