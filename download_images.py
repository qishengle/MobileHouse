import urllib.request
import os
import ssl

# Create an SSL context that doesn't verify certificates
ssl_context = ssl._create_unverified_context()

# Create directory if it doesn't exist
os.makedirs('assets/images/ch01', exist_ok=True)

# List of remaining images to download
images = [
    ('https://images.unsplash.com/photo-1472148439583-1f4cf81b80e0?w=800&q=80', 'china_urbanization_trend.png')
]

# Download each image
for img_url, img_name in images:
    try:
        print(f"Downloading {img_name}...")
        # Use the SSL context that doesn't verify certificates
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(img_url, f'assets/images/ch01/{img_name}')
        print(f"Successfully downloaded {img_name}")
    except Exception as e:
        print(f"Failed to download {img_name}: {e}")

print("Download complete!") 