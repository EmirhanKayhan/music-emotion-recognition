import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pytube import YouTube 
import os

# create webdriver object
driver = webdriver.Edge()
#türler=["neşeli müzikler", ""]
# Youtube'a gitme ve "neşeli müzikler" aramasını yapma

driver.get("https://www.youtube.com")
indis = 1

muzikcesit=["Neşeli Müzikler", "Agresif Müzikler", "Hüzünlü Müzikler"]
muzikturleri = [["neşeli müzikler", "happy songs"],
 ["agresif şarkılar", "angry songs"],
  ["üzgün şarkılar", "Sad Songs"]]
deneme = 0
print(muzikcesit[deneme])
indirilenler =[]
for index in muzikcesit:
    for x in muzikturleri:
        for y in x:
            for i in range(5):
                h=1

                search_box = driver.find_element(By.XPATH, "//input[@id='search']")
                # Eğer search_box doluysa içeriği sil
                search_box.clear()
                search_box.send_keys(y)
                time.sleep(5) 
                search_box.send_keys(Keys.ENTER)
                time.sleep(5)  # Sayfanın tamamen yüklenmesini bekleyin

                # Oynatma listeleri sekmesine geçme 
                filters_tab = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/div/ytd-search-header-renderer/div[3]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]")
                filters_tab.click()
                playlists_tab = driver.find_element(By.XPATH, "/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-search-filter-options-dialog-renderer/div[2]/ytd-search-filter-group-renderer[2]/ytd-search-filter-renderer[3]/a/div/yt-formatted-string")
                playlists_tab.click()
                
                time.sleep(5)  # Sayfanın tamamen yüklenmesini bekleyin
                
                # İlk oynatma listesini seçme
                playlist = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-playlist-renderer[{indis}]/ytd-playlist-thumbnail/a/div[1]/ytd-playlist-video-thumbnail-renderer/yt-image/img")
                driver.execute_script("arguments[0].scrollIntoView(true);", playlist)  # Scroll to the element
                indis=indis+1
                time.sleep(5)
                playlist.click()
                time.sleep(5)  # Sayfanın tamamen yüklenmesini bekleyin
                videon = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-playlist-panel-renderer/div/div[1]/div/div[1]/div[1]/div/div/yt-formatted-string/span[3]")
                videosayisi=videon.text
                print(videosayisi)
                vsayisi=int(videosayisi)
                vsayisi=vsayisi-5

                # Oluşturmak istediğiniz klasörün adını belirtin
                klasor_adı = muzikcesit[deneme]
                
                print(klasor_adı)
                # Klasör oluşturma işlemi
                try:
                    os.mkdir(klasor_adı)
                    print(f"{klasor_adı} adında klasör oluşturuldu.")
                except FileExistsError:
                    print(f"{klasor_adı} adında bir klasör zaten mevcut.")
                except Exception as e:
                    print("Bir hata oluştu:", e)
                
                for a in range(vsayisi):
                    # Oynatma listesindeki videoların linklerini alıp yazdırma
                    
                    videolinki = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-playlist-panel-renderer/div/div[3]/ytd-playlist-panel-video-renderer[{h}]/a").get_attribute('href')
                    #print(videolinki)
                    yt = YouTube( 
                    str(videolinki)) 
                    # extract only audio 
                    video = yt.streams.filter(only_audio=True).first() 

                    # check for destination to save file  
                    destination = './'+klasor_adı

                    # download the file 
                    out_file = video.download(output_path=destination) 

                    # save the file 
                    base, ext = os.path.splitext(out_file) 
                    if base not in indirilenler:
                        new_file = base + '.mp3'
                        os.rename(out_file, new_file) 

                    # result of success 
                    print(str(h)+yt.title + " has been successfully downloaded.")
                    h=h+1
                    indirilenler.append(base)
        deneme=deneme+1
    
# Close the WebDriver
driver.quit()



