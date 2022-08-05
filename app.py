import re
import json
import spacy
import flask
from flask_cors import CORS, cross_origin
from flask import jsonify, request, make_response

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Defining the ssential variables to identify phone numbers and email addresses
PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')

# text = input("Enter your text:")
# Defining function to extarct phone numbers from text


def extract_phone_number(text):
    phone = re.findall(PHONE_REG, text)
    if phone:
        number = ''.join(phone[0])
        if text.find(number) >= 0 and len(number) < 16:
            return number
    return None

# Defining function to extarct emails from text


def extract_emails(text):
    return re.findall(EMAIL_REG, text)

# Defining function to extarct person names from text


def extract_name(text):
    person = []
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    for token in doc:
        if token.pos_ == 'PROPN':
            person.append(token.text)
    return person


@app.route('/predict', methods=['POST'])
@cross_origin()
def create_meeting():
    isSensitiveData = False
    flag = False
    text = json.loads(request.data)
    text = text['data']
    names = extract_name(text)
    if names:
        flag = True
    # Calling extract_emails function to extract emails
    emails = extract_emails(text)
    if emails:
        flag = True
    # Calling extract_phone_number function to extract phone number
    phone_number = extract_phone_number(text)
    if phone_number:
        flag = True
    if flag == True:
        isSensitiveData = True
        # print("Your text contains personal data!")
    response = {
        "isSensitiveData": isSensitiveData,
        "names": names,
        "emails": emails,
        "phone_number": phone_number
    }
    return jsonify(response)


# Calling the functions
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
