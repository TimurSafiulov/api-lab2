from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_scraper():
    print("🤖 Запускаємо Selenium WebDriver...")
    
    
    options = webdriver.ChromeOptions()
   
    driver = webdriver.Chrome(options=options)

    try:
       
        print("🌍 Переходимо на сторінку логіну...")
        driver.get("https://quotes.toscrape.com/login")

        
        print("🔐 Вводимо логін та пароль...")
        
        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys("admin_timur")
        
       
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("supersecret123")
        
        
        login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        login_button.click()

        
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Logout"))
        )
        print("✅ Авторизація пройшла успішно!")

       
        print("📄 Зчитуємо дані зі сторінки...")
        
        
        items = driver.find_elements(By.CLASS_NAME, "quote")
        
        print("\n--- Зібрані дані ---")
        for i, item in enumerate(items[:5], 1): 
            
            text = item.find_element(By.CLASS_NAME, "text").text
           
            author = item.find_element(By.CLASS_NAME, "author").text
            print(f"{i}. {author}: {text}")
            
        print("--------------------\n")

    except Exception as e:
        print(f"❌ Сталася помилка: {e}")
        
    finally:
        
        time.sleep(3)
        print("🚪 Закриваємо браузер...")
        driver.quit()

if __name__ == "__main__":
    run_scraper()