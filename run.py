import time, random, requests, sys
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

class color:
  PURPLE = '\033[95m'
  CYAN = '\033[96m'
  DARKCYAN = '\033[36m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  END = '\033[0m'

def listToString(s):
  str1 = " " 
  return (str1.join(s))

def check_element(xpath):
  try:
    driver.find_element_by_xpath(xpath)
    return True
  except NoSuchElementException:
    return False

# Hapus komen jika ingin browser tidak muncul
""" option = webdriver.Options()
option.add_argument('--headless')
option.add_argument('--no-sandbox') """
driver = webdriver.Firefox()

start = time.time()
time_convert = time.strftime('%H:%M:%S', time.gmtime(start))

url = 'https://sman1kaliwungu.sch.id/smanka/and.php'
acak_aktif = 'https://sman1kaliwungu.sch.id/smanka/acak2.php?stat=1'
acak_nonaktif = 'https://sman1kaliwungu.sch.id/smanka/acak2.php?stat=0'
username = input('Masukkan username >> ')
password = input('Masukkan password >> ')

driver.get(url)

def salah_soal(nomer, jawaban):
  driver.find_element_by_xpath('//div[@class="list23"]/div[@class="nosoal"]').click()
  list_soal = driver.find_elements_by_xpath('//div[@id="mySidenav"]/div[@class="menusamping"]/li') 

  for l in list_soal:
    driver.execute_script('arguments[0].scrollIntoView();', l)

  driver.find_element_by_xpath(f'//div[@id="mySidenav"]/div[@class="menusamping"]/li[{nomer}]').click()

  if str(jawaban) == 'A':
    driver.find_element_by_xpath('//div[@class="jawaban"]//table//label[@for="C"]').click()
  elif str(jawaban) == 'B':
    driver.find_element_by_xpath('//div[@class="jawaban"]//table//label[@for="E"]').click()
  elif str(jawaban) == 'C':
    driver.find_element_by_xpath('//div[@class="jawaban"]//table//label[@for="B"]').click()
  elif str(jawaban) == 'D':
    driver.find_element_by_xpath('//div[@class="jawaban"]//table//label[@for="A"]').click()
  elif str(jawaban) == 'E':
    driver.find_element_by_xpath('//div[@class="jawaban"]//table//label[@for="B"]').click()
  else:
    driver.find_element_by_xpath('//div[@class="jawaban"]//table//label[@for="C"]').click()

  driver.find_element_by_xpath('//div[@class="raguragu"]/label').click()
  if check_element('//div[@class="next"]/a/div') == True:
    driver.find_element_by_xpath('//div[@class="next"]/a/div').click()
  else:
    driver.find_element_by_xpath('//div[@class="back"]/a/div').click()

  print(f'Disalahkan nomer {nomer}\nJawaban yang benar:\n{jawaban}\n\n')
  time.sleep(1)

def login(username, password):
  driver.find_element_by_xpath('//form//input[@name="username"]').send_keys(username)
  driver.find_element_by_xpath('//form//input[@name="pass"]').send_keys(password)
  driver.find_element_by_xpath('//form//input[@type="submit"]').click()
  time.sleep(1)

login(username, password)

print(f'Mulai jam {time_convert}\n')

nama_peserta = driver.find_element_by_xpath('//div[@class="col-sm-12 garis"][1]').text.strip().split('\n')
kelas = driver.find_element_by_xpath('//div[@class="col-sm-12 garis"][2]').text.strip().split('\n')
mapel_aktif = driver.find_element_by_xpath('//div[@class="col-sm-12 garis"][3]').text.strip().split('\n')
jumlah_soal = driver.find_element_by_xpath('//form//input[@name="jml_soal"]').get_attribute('value')
id_mapel = driver.find_element_by_xpath('//form//input[@name="id_mapel"]').get_attribute('value')
token = driver.find_element_by_xpath('//form//input[@name="tokennya"]').get_attribute('hidden')

if token == None:
  print('Ada token yang harus diisi')
  token_text = input('Masukkan token >> ')
  driver.find_element_by_xpath('//form//input[@name="tokennya"]').send_keys(token_text)

print(f'{nama_peserta[0]}: {nama_peserta[1]}\n{kelas[0]}: {kelas[1]}\n{mapel_aktif[0]}: {mapel_aktif[1]}\n\nApakah yakin ingin melanjutkan?\njika lanjut isi dengan "iya" jika tidak ingin lanjut isi dengan "tidak"')
pilih = str(input('Gas atau mundur? >> '))
pilih = pilih.lower()

if pilih == 'iya':
  if mapel_aktif[1] == 'Tidak Ada Jadwal Ujian' or id_mapel == '':
    print(f'{color.RED}Mapel tidak ada, tidak bisa melanjutkan eksekusi{color.END}')
    driver.quit()
  else:
    print(f'{color.GREEN}Mapel ada jadi bisa dilanjut{color.END}')
    driver.find_element_by_xpath('//div//button[@type="submit"]').click()
    """ mulai_non = driver.find_element_by_xpath('///button').get_attribute('disabled')
    if mulai_non == None: """
    requests.get(acak_nonaktif)
    driver.find_element_by_xpath('//form/button[@type="submit"]').click()
    requests.get(acak_aktif)
    print('Pilih tipe soal\n[1] Semua pilihan ganda\n[2] Ada listening\n[3] Ada essai')
    pilih_tipe = int(input('Tipe soal >> '))
    print()
    print('Mau salah berapa?')
    salah = int(input('Salah >> '))

    if pilih_tipe == 1:
      jumlah_soal = driver.find_element_by_xpath('//div[@class="jawaban"]/form/input[@name="jml"]').get_attribute('value')
      print(f'Tipe soal pilihan ganda\nContoh: {color.RED}geo12vero-soal.xlsx{color.END}')
      file = input('Masukkan nama file yang ada di folder soal >> ')

      data = pd.read_excel(r'soal/'+file)
      for i in range(1, int(jumlah_soal)+1):
        soal = driver.find_element_by_xpath('//form/input[@name="no"]').get_attribute('value')
        dg = data.loc[data['no_soal'] == int(soal)]
        jawaban = listToString(dg['kunci'].values)
        tsoal = listToString(dg['pertanyaan'].values)
        tjawaban = listToString(dg[jawaban].values)
        print(f'Menemukan soal nomer {soal}\nSoal:\n{tsoal}\nJawaban:\n{jawaban}: {tjawaban}\n\n')
        driver.find_element_by_xpath(f'//div[@class="jawaban"]//table//label[@for="{jawaban}"]').click()
        if check_element('//div[@class="next"]/a/div') == True:
          driver.find_element_by_xpath('//div[@class="next"]/a/div').click()
        else:
          driver.find_element_by_xpath('//div[@class="back"]/a/div').click()
        time.sleep(1)

      selesai = time.strftime('%H:%M:%S', time.gmtime(time.time() - start))
      print(f'Selesai mengisi jawaban dalam waktu {selesai}\n')
      print('Apakah ingin diselesaikan atau tidak? jika ingin diselesaikan isi dengan "iya" jika tidak ingin diselesaikan isi dengan "tidak" jika ingin otomatis keluar ketik "otomatis"')
      pilih_selesai = str(input('Selesai atau tidak? >> '))
      pilih_selesai = pilih_selesai.lower()

      if pilih_selesai == 'iya':
        if salah > 0:
          for i in range(1, int(salah)+1):
            nomer = random.randint(1,int(jumlah_soal))
            dg = data.loc[data['no_soal'] == int(nomer)]
            jawaban = listToString(dg['kunci'].values)
            salah_soal(nomer, jawaban)

        driver.find_element_by_xpath(f'//div[@id="mySidenav"]/div[@class="menusamping"]/li[{jumlah_soal}]').click()
        driver.find_element_by_xpath('//div[@class="finish"]/a/div').click()
        driver.find_element_by_xpath('//div[@id="popup"]//input[@id="myCheckbox"]').click()
        driver.find_element_by_xpath('//div[@id="popup"]//input[@id="myButton"]').click()
        print('Tes telah diselesaikan')
        time.sleep(10)

      elif pilih_selesai == 'tidak':
        print('Tes tidak diselesaikan, silahkan selesai manual')
      elif pilih_selesai == 'otomatis':
        tunggu = int(input('Otomatis keluar berapa menit >> '))
        for i in range(tunggu,0,-1):
          print(f'{i} Menit', end='\r', flush=True)
          time.sleep(60)
          if check_element('//div[@class="next"]/a/div') == True:
            driver.find_element_by_xpath('//div[@class="next"]/a/div').click()
          else:
            driver.find_element_by_xpath('//div[@class="back"]/a/div').click()

        if salah > 0:
          for i in range(1, int(salah)+1):
            nomer = random.randint(1,int(jumlah_soal))
            dg = data.loc[data['no_soal'] == int(nomer)]
            jawaban = listToString(dg['kunci'].values)
            salah_soal(nomer, jawaban)

        driver.find_element_by_xpath(f'//div[@id="mySidenav"]/div[@class="menusamping"]/li[{jumlah_soal}]').click()
        driver.find_element_by_xpath('//div[@class="finish"]/a/div').click()
        driver.find_element_by_xpath('//div[@id="popup"]//input[@id="myCheckbox"]').click()
        driver.find_element_by_xpath('//div[@id="popup"]//input[@id="myButton"]').click()
        print('Tes telah diselesaikan')
      else:
        print('Tes tidak diselesaikan, silahkan selesai manual')

    elif pilih_tipe == 2:
      jumlah_soal = driver.find_element_by_xpath('//div[@class="jawaban"]/form/input[@name="jml"]').get_attribute('value')
      print('Tipe soal ada listening')
      file = input('Masukkan nama file yang ada di folder soal isinya listening >> ')
      file2 = input('Masukkan nama file yang ada di folder soal isinya pilihan ganda >> ')
      no_lis = input('Masukkan berapa soal listening yang ada >> ')

      data = pd.read_excel(r'soal/'+file)
      for i in range(1, int(no_lis)+1):
        soal = driver.find_element_by_xpath('//form/input[@name="no"]').get_attribute('value')
        dg = data.loc[data['no_soal'] == int(soal)]
        jawaban = listToString(dg['kunci'].values)
        tsoal = listToString(dg['pertanyaan'].values)
        tlis = listToString(dg['listening'].values)
        tjawaban = listToString(dg[jawaban].values)
        driver.find_element_by_xpath(f'//div[@class="jawaban"]//table//label[@for="{jawaban}"]').click()
        if check_element('//div[@class="next"]/a/div') == True:
          driver.find_element_by_xpath('//div[@class="next"]/a/div').click()
        print(f'Selesai mengerjakan nomer {i}\nSoal:\n{tlis}-{tsoal}\nJawaban:\n{jawaban}: {tjawaban}\n\n')
        time.sleep(1)

      data2 = pd.read_excel(r'soal/'+file2)
      no_lis = int(no_lis)+1
      for i in range(int(no_lis), int(jumlah_soal)+1):
        soal = driver.find_element_by_xpath('//form/input[@name="no"]').get_attribute('value')
        dg2 = data2.loc[data2['no_soal'] == int(soal)]
        jawaban = listToString(dg2['kunci'].values)
        tsoal = listToString(dg2['pertanyaan'].values)
        tjawaban = listToString(dg2[jawaban].values)
        driver.find_element_by_xpath(f'//div[@class="jawaban"]//table//label[@for="{jawaban}"]').click()
        if check_element('//div[@class="next"]/a/div') == True:
          driver.find_element_by_xpath('//div[@class="next"]/a/div').click()
        else:
          driver.find_element_by_xpath('//div[@class="back"]/a/div').click()
        print(f'Selesai mengerjakan nomer {i}\nSoal:\n{tsoal}\nJawaban:\n{jawaban}: {tjawaban}\n\n')
        time.sleep(1)

      if salah > 0:
        for i in range(1, int(salah)+1):
          nomer = random.randint(1,int(jumlah_soal))
          if int(nomer) <= 15:
            dg = data.loc[data['no_soal'] == int(nomer)]
            jawaban = listToString(dg['kunci'].values)
          else:
            dg2 = data2.loc[data2['no_soal'] == int(nomer)]
            jawaban = listToString(dg2['kunci'].values)
            
          salah_soal(nomer, jawaban)
      
      selesai = time.strftime('%H:%M:%S', time.gmtime(time.time() - start))
      print(f'Selesai mengisi jawaban dalam waktu {selesai}\n')
      print('Apakah ingin diselesaikan atau tidak? jika ingin diselesaikan isi dengan "iya" jika tidak ingin diselesaikan isi dengan "tidak"')
      pilih_selesai = str(input('Selesai atau tidak? >> '))
      pilih_selesai = pilih_selesai.lower()

      if pilih_selesai == 'iya':
        driver.find_element_by_xpath('//div[@class="list23"]/div[@class="nosoal"]').click()
        list_soal = driver.find_elements_by_xpath('//div[@id="mySidenav"]/div[@class="menusamping"]/li') 
        for l in list_soal:
          driver.execute_script('arguments[0].scrollIntoView();', l)
        list_soal_ragu = driver.find_elements_by_xpath('//div[@id="mySidenav"]/div[@class="menusamping"]/li/label[@class="angka2 hijau kuning"]')
        for o in list_soal_ragu:
          driver.find_element_by_xpath(f'//div[@id="mySidenav"]/div[@class="menusamping"]/li').click()
          driver.find_element_by_xpath('//div[@class="raguragu"]/label').click()
          if check_element('//div[@class="next"]/a/div') == True:
            driver.find_element_by_xpath('//div[@class="next"]/a/div').click()
          else:
            driver.find_element_by_xpath('//div[@class="back"]/a/div').click()
        driver.find_element_by_xpath(f'//div[@id="mySidenav"]/div[@class="menusamping"]/li[{jumlah_soal}]').click()
        driver.find_element_by_xpath('//div[@class="finish"]/a/div').click()
        driver.find_element_by_xpath('//div[@id="popup"]//input[@id="myCheckbox"]').click()
        driver.find_element_by_xpath('//div[@id="popup"]//input[@id="myButton"]').click()
        print('Tes telah diselesaikan')
        time.sleep(10)
      elif pilih_selesai == 'tidak':
        print('Tes tidak diselesaikan, silahkan selesai manual')
      elif pilih_selesai == 'otomatis':
        tunggu = int(input('Otomatis keluar berapa menit >> '))
        for i in range(tunggu,0,-1):
          print(f'{i} Menit', end='\r', flush=True)
          time.sleep(60)
          if check_element('//div[@class="next"]/a/div') == True:
            driver.find_element_by_xpath('//div[@class="next"]/a/div').click()
          else:
            driver.find_element_by_xpath('//div[@class="back"]/a/div').click()

        if salah > 0:
          for i in range(1, int(salah)+1):
            nomer = random.randint(1,int(jumlah_soal))
            if int(nomer) <= 15:
              dg = data.loc[data['no_soal'] == int(nomer)]
              jawaban = listToString(dg['kunci'].values)
            else:
              dg2 = data2.loc[data2['no_soal'] == int(nomer)]
              jawaban = listToString(dg2['kunci'].values)
              
            salah_soal(nomer, jawaban)

        driver.find_element_by_xpath(f'//div[@id="mySidenav"]/div[@class="menusamping"]/li[{jumlah_soal}]').click()
        driver.find_element_by_xpath('//div[@class="finish"]/a/div').click()
        driver.find_element_by_xpath('//div[@id="popup"]//input[@id="myCheckbox"]').click()
        driver.find_element_by_xpath('//div[@id="popup"]//input[@id="myButton"]').click()
        print('Tes telah diselesaikan')
      else:
        print('Tes tidak diselesaikan, silahkan selesai manual')

      
    elif pilih_tipe == 3:
      print('Tipe soal ada essai')
      file = input('Masukkan nama file yang ada di folder soal isinya essai >> ')
      file2 = input('Masukkan nama file yang ada di folder soal isinya pilihan ganda >> ')
      print('Fitur ini belum selesai')
    else:
      print(f'{color.RED}Tipe soal tidak ada{color.END}')

elif pilih == 'tidak':
  print('Tidak lanjut karena takut')
  driver.quit()
else:
  print('Maaf saya tidak paham')
  driver.quit()
