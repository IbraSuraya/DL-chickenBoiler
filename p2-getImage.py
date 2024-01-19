import requests
import os
import re

def is_image_url(url):
    # Pola reguler untuk mendeteksi ekstensi gambar
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
    pattern = r'\.(' + '|'.join(image_extensions) + ')$'

    # Memeriksa apakah URL sesuai dengan pola reguler
    return re.search(pattern, url, flags=re.IGNORECASE) is not None
  
def download_images_from_urls(input_file, output_folder):
  with open(input_file, 'r') as file:
    urls = file.readlines()

  if not os.path.exists(output_folder):
    os.makedirs(output_folder)

  for url in urls:
    url = url.strip()  # Menghapus spasi atau karakter newline di sekitar URL
    try:
      response = requests.get(url, stream=True)
      if response.status_code == 200:
        # Ekstrak nama file dari URL
        if is_image_url(url):
          filename = os.path.join(output_folder, os.path.basename(url))
        else : 
          pass
          filename = os.path.join(output_folder, os.path.basename(url)+".png")
          
        # Menyimpan gambar
        with open(filename, 'wb') as image_file:
          for chunk in response.iter_content(chunk_size=128):
            image_file.write(chunk)
        
        print(f"Gambar {filename} berhasil diunduh.")
      else:
        print(f"Gagal mengunduh gambar dari {url}. Status code: {response.status_code}")
    except Exception as e:
      print(f"Terjadi kesalahan saat mengunduh gambar dari {url}: {str(e)}")

# Gantilah 'input.txt' dengan nama file yang sesuai
input_file = 'data\\url_unique2.txt'

# Gantilah 'data\\raw' dengan nama folder tempat menyimpan gambar yang diunduh
output_folder = 'data\\raw2'

download_images_from_urls(input_file, output_folder)