import requests
from io import BytesIO
from urllib.parse import quote
from urllib.parse import urlencode
import zipfile
import os
import glob
from PIL import Image


def download_file(base_url, public_key):
    final_url = base_url + urlencode({'public_key': public_key})

    try:
        # Получаем загрузочную ссылку
        response = requests.get(final_url)
        response.raise_for_status()

        # Получаем URL для скачивания файла или архива папки
        download_url = response.json()['href']

        # Скачиваем файл или архив
        file_response = requests.get(download_url)
        file_response.raise_for_status()

        # Сохраняем содержимое файла или архива
        with open('downloaded_file.zip', 'wb') as f:
            f.write(file_response.content)
            print('Содержимое папки сохранено как downloaded_file.zip')

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def extract_zip(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f'Содержимое архива извлечено в папку {extract_to}')

def collect_images_to_tiff(folder_path, output_tiff):
    images = []

    # Поиск всех файлов с расширением .png в указанной папке
    for file in glob.glob(os.path.join(folder_path, '*.png')):
        img = Image.open(file)
        images.append(img)

    if images:
        # Сохранение изображений в один tiff файл
        images[0].save(output_tiff, save_all=True, append_images=images[1:])
        print(f'Картинки успешно собраны в файл {output_tiff}')
    else:
        print(f'Нет изображений с расширением .png в папке {folder_path}')

def main():
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    public_key = 'https%3A%2F%2Fdisk.yandex.ru%2Fd%2FV47MEP5hZ3U1kg'  # Сюда вписываете вашу ссылку
    # Путь к скачанному ZIP архиву
    zip_file = 'downloaded_file.zip'
    # Папка, в которую будет извлечено содержимое архива
    extract_folder = 'extracted_content'
    path_way = 'Для тестового'
    # Список папок с изображениями внутри архива (задается вами)
    target_folders = ['1388_12_Наклейки 3-D_3', '1388_6_Наклейки 3-D_2', '1388_2_Наклейки 3-D_1', '1369_12_Наклейки 3-D_3']
    # Имя для выходного TIFF файла
    output_tiff = 'Result'

    try:
        # Скачиваем файл
        download_file(base_url, public_key)
        # Извлекаем содержимое архива
        extract_zip(zip_file, extract_folder)

        # Проходим по каждой целевой папке с изображениями
        for target_folder in target_folders:
            # Полный путь к нужной папке с изображениями
            folder_path = os.path.join(extract_folder, path_way, target_folder)

            # Имя выходного TIFF файла для текущей папки
            output_tiff_file = f'{output_tiff}_{target_folder}.tif'

            # Собираем изображения в один TIFF файл
            collect_images_to_tiff(folder_path, output_tiff_file)

    except Exception as e:
        print(f'Произошла ошибка: {e}')

if __name__ == "__main__":
    main()