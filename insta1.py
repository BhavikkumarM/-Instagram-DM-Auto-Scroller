from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time
import threading
import keyboard  # install with: pip install keyboard

# Setup Edge Options
options = Options()
options.add_argument("--start-maximized")

# Set path to EdgeDriver
service = EdgeService(executable_path="C:/Users/welcome/msedgedriver.exe")
driver = webdriver.Edge(service=service, options=options)

# Step 1: Open Instagram
driver.get("https://www.instagram.com/")
input("👉 Log in manually and press ENTER here once logged in...")

# Step 2: Open DMs and target chat
driver.get("https://www.instagram.com/direct/inbox/")
input("👉 Open the specific chat you want to extract and press ENTER here...")

time.sleep(3)

# Step 3: Locate scrollable chat area
scrollable_div_xpath = '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div[1]/div/div/div/div/div/div'
scrollable_div = driver.find_element(By.XPATH, scrollable_div_xpath)

# Flags
pause_scrolling = False
stop_scrolling = False
retry_scrolling = False

# Step 4: Keyboard control handler
def keyboard_control():
    global pause_scrolling, stop_scrolling, retry_scrolling
    while True:
        if keyboard.is_pressed('p'):
            pause_scrolling = not pause_scrolling
            print(f"{'⏸️ Paused' if pause_scrolling else '▶️ Resumed'} scrolling...")
            time.sleep(1)
        elif keyboard.is_pressed('q'):
            stop_scrolling = True
            print("🛑 Quitting scroll...")
            break
        elif keyboard.is_pressed('r'):
            retry_scrolling = True
            print("🔁 Retrying scroll from where left...")
            time.sleep(1)
        time.sleep(0.1)

# Start keyboard listener thread
keyboard_thread = threading.Thread(target=keyboard_control)
keyboard_thread.daemon = True
keyboard_thread.start()

# Step 5: Infinite scrolling with retry support
print("\n⏫ Scrolling started... Press 'P' to pause/resume, 'Q' to quit, 'R' to retry if error occurs.\n")

while True:
    if stop_scrolling:
        break

    if pause_scrolling:
        time.sleep(1)
        continue

    try:
        # Scroll to top
        driver.execute_script("arguments[0].scrollTop = 0", scrollable_div)
        print("🔄 Scrolling up...")
        time.sleep(5)
    except Exception as e:
        print(f"⚠️ Error occurred: {e}")
        print("⏳ Waiting for 'R' to retry or 'Q' to quit...")

        # Wait for user to press 'R' or 'Q'
        while not retry_scrolling and not stop_scrolling:
            time.sleep(0.5)

        if stop_scrolling:
            break
        elif retry_scrolling:
            try:
                # Re-locate scrollable chat div in case it was lost
                scrollable_div = driver.find_element(By.XPATH, scrollable_div_xpath)
                print("✅ Element reloaded. Resuming scroll...")
            except Exception as inner_error:
                print(f"❌ Retry failed: {inner_error}")
            retry_scrolling = False

print("✅ Scroll stopped by user.")

# Optional close
try:
    input("✅ Press ENTER to close the browser...")
except:
    pass

# driver.quit()  # Uncomment if you want to auto-close browser
