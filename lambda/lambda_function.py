import json
import boto3
import uuid
import base64

from decimal import Decimal
from datetime import datetime

# ============================
# AWS Clients
# ============================

s3 = boto3.client("s3")

rekognition = boto3.client("rekognition")

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("AnimalDetection")

# ============================
# Configuration
# ============================

BUCKET_NAME = "animal-image-detect"

ANIMAL_LABELS = [

    "Dog",
    "Cat",
    "Tiger",
    "Lion",
    "Elephant",
    "Horse",
    "Cow",
    "Buffalo",
    "Bear",
    "Monkey",
    "Wolf",
    "Fox",
    "Rabbit",
    "Goat",
    "Sheep",
    "Leopard",
    "Cheetah",
    "Camel",
    "Zebra",
    "Deer",
    "Giraffe",
    "Bird",
    "Eagle",
    "Parrot",
    "Fish",
    "Shark",
    "Whale",
    "Dolphin",
    "Snake",
    "Crocodile"

]

# ============================
# Decimal Serializer
# ============================

def decimal_default(obj):

    if isinstance(obj, Decimal):

        return float(obj)

    raise TypeError


# ============================
# Response Function
# ============================

def response(status, body):

    return {

        "statusCode": status,

        "headers": {

            "Content-Type": "application/json"

        },

        "body": json.dumps(
            body,
            default=decimal_default
        )

    }


# ============================
# Lambda Handler
# ============================

def lambda_handler(event, context):

    try:

        method = event["requestContext"]["http"]["method"]

        path = event["rawPath"]

        print(method)

        print(path)

        # ====================================================
        # POST /upload
        # ====================================================

        if method == "POST" and path.endswith("/upload"):

            body = json.loads(event["body"])

            filename = body["filename"]

            image = body["image"]

            image_bytes = base64.b64decode(image)

            # Upload to S3

            s3.put_object(

                Bucket=BUCKET_NAME,

                Key=filename,

                Body=image_bytes,

                ContentType="image/jpeg"

            )

            print("Image Uploaded")

            # Detect Labels

            rek_response = rekognition.detect_labels(

                Image={

                    "S3Object": {

                        "Bucket": BUCKET_NAME,

                        "Name": filename

                    }

                },

                MaxLabels=20,

                MinConfidence=70

            )

            labels = sorted(

                rek_response["Labels"],

                key=lambda x: x["Confidence"],

                reverse=True

            )

            detected = []

            # Store every detected animal

            for label in labels:

                name = label["Name"]

                confidence = round(
                    label["Confidence"],
                    2
                )

                print(name, confidence)

                if name in ANIMAL_LABELS:

                    detected.append({

                        "Animal": name,

                        "Confidence": confidence

                    })

                    table.put_item(

                        Item={

                            "DetectionId": str(uuid.uuid4()),

                            "ImageName": filename,

                            "ImageURL": f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}",

                            "Animal": name,

                            "Confidence": Decimal(str(confidence)),

                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        }

                    )

            print("Saved into DynamoDB")

                        # Return success for upload

            return response(

                200,

                {

                    "message": "Image Uploaded Successfully",

                    "image": filename,

                    "detectedAnimals": detected

                }

            )

        # ====================================================
        # GET /animals
        # ====================================================

        elif method == "GET" and path.endswith("/animals"):

            data = table.scan()

            items = data.get("Items", [])

            image_map = {}

            animal_count = {}

            for item in items:

                image_name = item["ImageName"]

                if image_name not in image_map:

                    image_map[image_name] = {

                        "imageName": image_name,

                        "imageURL": item["ImageURL"],

                        "timestamp": item["Timestamp"],

                        "animals": []

                    }

                image_map[image_name]["animals"].append(

                    {

                        "name": item["Animal"],

                        "confidence": float(item["Confidence"])

                    }

                )

                animal = item["Animal"]

                if animal in animal_count:

                    animal_count[animal] += 1

                else:

                    animal_count[animal] = 1

            images = list(image_map.values())

            print("========== Uploaded Images ==========")

            for img in images:

                print(img["imageName"])

                for a in img["animals"]:

                    print(
                        "   ",
                        a["name"],
                        "-",
                        a["confidence"]
                    )

            print("========== Animal Count ==========")

            for key, value in sorted(animal_count.items()):

                print(key, ":", value)

            return response(

                200,

                {

                    "images": images,

                    "animalCount": animal_count

                }

            )

        # ====================================================
        # Invalid Route
        # ====================================================

        else:

            return response(

                404,

                {

                    "message": "Invalid Route"

                }

            )

    except Exception as e:

        print("ERROR :", str(e))

        return response(

            500,

            {

                "error": str(e)

            }

        )