from flask import Flask, request, abort
import hmac
import hashlib
import os

app = Flask(__name__)

GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "your_secret_here")  # match with GitHub webhook

def verify_signature(payload, signature):
    mac = hmac.new(GITHUB_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    expected = 'sha256=' + mac.hexdigest()
    return hmac.compare_digest(expected, signature)

@app.route('/github-webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature or not verify_signature(request.data, signature):
        abort(403)  # Forbidden if signature fails

    data = request.json
    print("🔔 GitHub Webhook received!")
    print(f"Repo: {data['repository']['full_name']}")
    print(f"Pusher: {data['pusher']['name']}")
    print(f"Ref: {data['ref']}")
    return 'Webhook received', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
