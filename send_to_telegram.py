import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def send_to_telegram(message):
    try:
        url = 'https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage'
        payload = {'chat_id': '<YOUR_CHAT_ID>', 'text': message}
        response = requests.post(url, json=payload)

        # Validate response
        if response.status_code == 200:
            logging.info('Message sent successfully!')
            return {'status': 'success', 'response': response.json()}
        else:
            logging.error(f'Error sending message: {response.status_code}, {response.text}')
            return {'status': 'error', 'error_message': f'Failed to send message. Status code: {response.status_code}'}
    except requests.exceptions.RequestException as e:
        logging.exception('Request failed')
        return {'status': 'error', 'error_message': str(e)}
    except Exception as e:
        logging.exception('An unexpected error occurred')
        return {'status': 'error', 'error_message': str(e)}

# Example usage
if __name__ == '__main__':
    result = send_to_telegram('Hello, Telegram!')
    print(result)