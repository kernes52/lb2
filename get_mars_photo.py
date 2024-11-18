import os
import requests #відправка http запрошень
import argparse #обробляти аргументи командного рядка, що передаються під час запуску скрипта.
from datetime import datetime

# Функція для завантаження фотографій
def download_mars_photos(earth_date, camera, api_key="DEMO_KEY"):  # виконувати запит до API NASA і завантажувати фотографії з Марса для заданої дати і камери.
    #адреса, для отримання фотографій з марсохода
    url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    params = {
        "earth_date": earth_date,
        "camera": camera,
        "api_key": api_key
    }

    response = requests.get(url, params=params) #виконує GET-запит передаючи параметри які ми зібрали в словнику

    if response.status_code != 200:
        print(f"Помилка при запиті до API: {response.status_code} - {response.text}")
        return

    data = response.json() #Отримуємо дані у форматі JSON із відповіді сервера перетворює відповідь в об'єкт Python (словник або список)
    if "error" in data:
        print(f"Помилка від API: {data['error']}")
        return

    photos = data.get("photos", []) #Витягуємо список фотографій з отриманих даних та даймо пустий

    if not photos:
        print("Фотографії не знайдено. Перевірте дату та камеру.")
        return

    rover_name = photos[0]["rover"]["name"]
    directory_name = f"{earth_date}_{rover_name}_{camera}"
    os.makedirs(directory_name, exist_ok=True)

    for photo in photos:
        img_url = photo["img_src"]
        img_name = os.path.join(directory_name, os.path.basename(img_url))
        print(f"Завантаження {img_url} в {img_name}...")
        img_data = requests.get(img_url).content
        with open(img_name, "wb") as f:
            f.write(img_data)

    print(f"Усі фотографії збережено в директорію: {directory_name}")

# Основна функція скрипта, яка запускає виконання програми
def main():
    parser = argparse.ArgumentParser(description="Скрипт для завантаження фото поверхні Марса")
    parser.add_argument("--earth-date", required=True, help="Дата на Землі у форматі YYYYMMDD")
    parser.add_argument("--camera", required=True, help="Камера (наприклад, RHAZ, FHAZ, MAST тощо)")

    args = parser.parse_args() #Зчитує і парсить аргументи командного рядка, передані під час запуску скрипта.

    # Очищення рядка дати від зайвих пробілів
    earth_date = args.earth_date.strip()

    # Перевірка формату дати
    try:
        datetime.strptime(earth_date, "%Y%m%d")
    except ValueError:
        print("Неправильний формат дати. Використовуйте YYYYMMDD.")
        return

    # Запуск функції завантаження фотографій
    download_mars_photos(earth_date, args.camera)

# дає змогу запускати код у блоці main(), тільки якщо скрипт був запущений безпосередньо
if __name__ == "__main__":
    main()
