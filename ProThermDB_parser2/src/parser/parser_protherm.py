import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os, glob, time
from src.utils.paths import RAW_DATA_DIR


def pars_data(org_name, prot_name):

    org_name = org_name.capitalize()
    prot_name = prot_name.capitalize()

    # Папка для сохранения (в репозитории)
    download_dir = str(RAW_DATA_DIR)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True
    })
    chrome_options.add_experimental_option("detach", False)

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://web.iitm.ac.in/bioinfo2/prothermdb/search.html")

    button_list = ['cb1', 'cb7', 'cb8', 'cb18', 'cb23', 'cb27', 'cb28', 'cb29', 'cb31', 'cb32', 'cb33']
    for but in button_list:
        button_el = driver.find_element(By.ID, but)
        button_el.click()

    # ДЛЯ ОРГАНИЗМА
    if org_name is not None:
        org_input = driver.find_element(By.ID, "myInput2")
        org_input.clear()
        org_input.send_keys(org_name)

    # ДЛЯ ФЕМРЕНТА
    if prot_name is not None:
        protein_input = driver.find_element(By.ID, "myInput")
        protein_input.clear()
        protein_input.send_keys(prot_name)

    wait = WebDriverWait(driver, 5)
    submit_button = driver.find_element(By.XPATH, "//button[text()='Search']")
    submit_button.click()

    download_button = driver.find_element(By.XPATH, "//input[@value='Download Now!']")
    download_button.click()

    driver.quit()  # - close browser

    # Меняем название и расширение скаченного файла
    if prot_name and org_name:
        new_name = f"ProTherm_{prot_name}_{org_name}.csv"
    elif org_name and '/' in org_name:
        new_name = f"ProTherm_{org_name.replace('/', '-')}.csv"
    elif prot_name:
        new_name = f"ProTherm_{prot_name}.csv"
    else:
        new_name = f"ProTherm_{org_name}.csv"

    # Пытаемся найти и переименовать файл
    for i in range(10):

        files = glob.glob(os.path.join(download_dir, "*.tsv.crdownload")) + glob.glob(
            os.path.join(download_dir, "*.tsv")) + glob.glob(os.path.join(download_dir, "*.tmp"))

        if files:
            old_path = files[0]
            new_path = os.path.join(download_dir, new_name)

            # если файл с таким именем уже есть — удалим или добавим индекс
            if os.path.exists(new_path):
                base, ext = os.path.splitext(new_path)
                new_path = f"{base}_{int(time.time())}{ext}"

            try:
                os.rename(old_path, new_path)
                print(f"Файл найден и переименован: {new_path}")
                break
            except PermissionError:
                # если Chrome ещё не закончил запись — подождём
                print("Файл занят")
                time.sleep(2)
        else:
            print("Файл пока не найден")
            time.sleep(2)
    else:
        print("Файл не появился после 20 секунд ожидания.")

    df = pd.read_csv(new_path, sep='\t')

    # ПРОВЕРКА НА ПУСТУЮ ТАБЛИЦУ
    if df.empty:
        print(
            "По данному запросу данные не найдены.\n"
            "Проверьте точность написания названия организма или фермента.\n"
            "Название должно полностью совпадать с базой данных."
        )
        os.remove(new_path)
        return None

    return df
