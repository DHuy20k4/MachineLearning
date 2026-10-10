
import requests

url = "http://127.0.0.1:5000/api/predict"

# Dữ liệu thử nghiệm minh họa, không phải số đo của một mẫu cụ thể.
sample = {
    "Area": 50000,
    "Perimeter": 850,
    "MajorAxisLength": 200,
    "MinorAxisLength": 150,
    "AspectRatio": 1.33,
    "Eccentricity": 0.66,
    "ConvexArea": 51000,
    "EquivDiameter": 252,
    "Extent": 0.75,
    "Solidity": 0.98,
    "Roundness": 0.87,
    "Compactness": 0.86,
    "ShapeFactor1": 0.004,
    "ShapeFactor2": 0.001,
    "ShapeFactor3": 0.74,
    "ShapeFactor4": 0.99,
}


response = requests.post(
    "http://127.0.0.1:5000/api/predict-batch",
    json={"samples": [sample, sample]},
    timeout=10,
)

print("HTTP status:", response.status_code)
print(response.text)
