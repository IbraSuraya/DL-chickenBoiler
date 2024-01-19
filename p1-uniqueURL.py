file_path = 'data\\url.txt' 
output_path = "data\\url_unique.txt"
data = []

try:
  with open(file_path, 'r') as file:
    data = file.readlines()
  data = [line.strip() for line in data]
  print(f"Isi file:")
except FileNotFoundError:
  print(f"File '{file_path}' tidak ditemukan.")
except Exception as e:
  print("Terjadi kesalahan saat membaca file:", str(e))

print(len(data))
my_set = set(data)
print(len(my_set))


# Membuka file untuk penulisan
with open(output_path, 'w') as file:
  # Menulis setiap elemen dalam baris terpisah
  for element in my_set:
    file.write(str(element) + '\n')