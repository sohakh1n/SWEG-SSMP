import os
import time
import redis
from PIL import Image

# Redis-Client einrichten
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

# Verzeichnisse für Bilder
uploads_dir = "src/uploads"
reduced_size_dir = os.path.join(uploads_dir, "reduced")

# Stelle sicher, dass das Verzeichnis existiert
os.makedirs(reduced_size_dir, exist_ok=True)


def resize_image(input_path, output_path, size=(800, 800)):
    with Image.open(input_path) as img:
        if img.mode == "RGBA":
            img = img.convert("RGB")
        img.thumbnail(size)
        img.save(output_path, format="JPEG")
    print(f"Image resized and saved to {output_path}")


def process_queue():
    is_idle = False  # Status-Flag: True, wenn Worker idle ist
    while True:
        image_path = redis_client.lpop("image_queue")
        if image_path:
            print(f"Dequeued image path: {image_path.decode('utf-8')}")
        else:
            print("Queue is empty, no images to process")

        if image_path:
            is_idle = False

            image_path = image_path.decode("utf-8")
            print(f"Processing image: {image_path}")

            # Verarbeitug des Bilds
            file_name = os.path.basename(image_path)
            output_path = os.path.join(reduced_size_dir, file_name)
            try:
                resize_image(image_path, output_path)
                print(f"Image processing completed: {output_path}")
            except Exception as e:
                print(f"Error processing image: {e}")
        else:
            if not is_idle:
                print("No images in the queue. Worker is idle...")
                is_idle = True

        time.sleep(2)  # Warte 2 Sekunden, bevor der Worker erneut prüft


if __name__ == "__main__":
    print("Image Worker started...")
    process_queue()
