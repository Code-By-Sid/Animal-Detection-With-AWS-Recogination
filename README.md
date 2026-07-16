# 🐾 AI Animal Detection using Amazon Rekognition

## 📌 Project Overview

AI Animal Detection is a serverless AWS application that allows users to upload animal images through a web application. The uploaded images are stored in Amazon S3 and analyzed using Amazon Rekognition to identify the animals present in each image. The detected animal names, confidence scores, image details, and upload timestamp are stored in Amazon DynamoDB. The application also maintains the total count of each detected animal across all uploaded images and displays the results on the website.

This project demonstrates how AWS AI services can be used to build an intelligent animal recognition and counting system.

---

# 🚀 Features

* Upload animal images (.jpg, .jpeg, .png)
* Store uploaded images in Amazon S3
* Detect animals using Amazon Rekognition
* Identify multiple animals in a single image
* Store detection results in Amazon DynamoDB
* Count total occurrences of each animal
* Display uploaded images and detected animals
* Show confidence scores
* Responsive Flask web application

---

# 🏗️ System Architecture

```text
                 User
                   │
                   ▼
          Flask Web Application
                   │
                   ▼
              API Gateway
                   │
                   ▼
            AWS Lambda Function
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
   Upload Image  Amazon    DynamoDB
      to S3    Rekognition Store Results
        │
        ▼
   Animal Image Bucket
                   │
                   ▼
             Flask Website
```

---

# ☁️ AWS Services Used

* AWS Lambda
* Amazon API Gateway
* Amazon S3
* Amazon Rekognition
* Amazon DynamoDB
* Amazon CloudWatch
* IAM

---

# 📂 Project Structure

```text
AnimalDetection/

│── app.py
│── requirements.txt
│── README.md
│
├── templates
│     └── index.html
│
└── lambda
      └── lambda_function.py
```

---

# 📦 Prerequisites

* AWS Account
* Python 3.10+
* Flask
* Requests
* Boto3
* AWS CLI configured
* IAM Role with required permissions

---

# 📁 AWS Resources

## Amazon S3 Bucket

Stores uploaded animal images.

Example:

```text
animal-image-bucket
```

---

## DynamoDB Table

**Table Name**

```text
AnimalDetection
```

**Partition Key**

```text
ImageId
```

---

# 🔄 Project Workflow

1. User uploads an animal image through the website.
2. Flask sends the image to API Gateway.
3. API Gateway invokes the Lambda function.
4. Lambda uploads the image to Amazon S3.
5. Amazon Rekognition analyzes the image and detects animal labels.
6. Detection results and confidence scores are stored in DynamoDB.
7. The application updates the total count of each detected animal.
8. Flask retrieves the data and displays all uploaded images and statistics.

---

# 📡 API Endpoints

## Upload Animal Image

**POST**

```text
/upload
```

### Request

```json
{
  "filename": "tiger.jpg",
  "image": "Base64EncodedImage"
}
```

### Response

```json
{
  "message": "Image Uploaded Successfully",
  "animal": "Tiger",
  "confidence": 99.85,
  "imageURL": "https://animal-image-bucket.s3.amazonaws.com/tiger.jpg"
}
```

---

## Get Detection Results

**GET**

```text
/images
```

### Response

```json
{
  "images": [
    {
      "imageName": "tiger.jpg",
      "animal": "Tiger",
      "confidence": 99.85,
      "imageURL": "https://animal-image-bucket.s3.amazonaws.com/tiger.jpg",
      "timestamp": "2026-07-16 15:20:45"
    }
  ]
}
```

---

## Get Animal Counts

**GET**

```text
/counts
```

### Response

```json
{
  "counts": {
    "Tiger": 3,
    "Lion": 2,
    "Elephant": 5,
    "Dog": 4,
    "Cat": 6
  }
}
```

---

# 💾 DynamoDB Attributes

| Attribute  | Description             |
| ---------- | ----------------------- |
| ImageId    | Unique Image ID         |
| ImageName  | Uploaded Image Name     |
| ImageURL   | Amazon S3 Image URL     |
| Animal     | Primary Detected Animal |
| Confidence | Detection Confidence    |
| Labels     | All Detected Labels     |
| Timestamp  | Upload Date & Time      |

---

# 🖥️ Website Features

* Upload animal images
* Display uploaded image
* Show detected animal
* Display confidence score
* View all detected labels
* Display total count of each animal
* Responsive design

---

# ▶️ Running the Flask Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser:

```text
http://localhost:5000
```

or

```text
http://<EC2-PUBLIC-IP>:5000
```

---

# 🔐 IAM Permissions Required

The Lambda execution role requires permissions for:

* Amazon S3
* Amazon Rekognition
* Amazon DynamoDB
* CloudWatch Logs

---

# 📈 Future Enhancements

* Animal species classification
* Endangered species identification
* Animal counting within a single image
* Animal habitat prediction
* Multi-language support
* Search and filter by animal type
* Interactive analytics dashboard
* User authentication

---

# 👨‍💻 Technologies Used

* Python
* Flask
* HTML
* CSS
* AWS Lambda
* Amazon API Gateway
* Amazon S3
* Amazon Rekognition
* Amazon DynamoDB
* IAM
* CloudWatch

---

# 📸 Sample Output

```text
Image Name:
tiger.jpg

Detected Animal:
Tiger

Confidence:
99.85%

Other Labels:
• Wildlife
• Mammal
• Nature
• Big Cat

Uploaded:
16 July 2026

Animal Count Summary:
Tiger: 3
Lion: 2
Elephant: 5
Dog: 4
Cat: 6
```

---

# 📄 License

This project is developed for educational and learning purposes. It demonstrates the integration of AWS Lambda, Amazon S3, Amazon Rekognition, Amazon API Gateway, and Amazon DynamoDB to build an AI-powered animal detection and counting application.
