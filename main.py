# main.py
import os
from store.store import SeleniumStore
import subprocess

src_folder = 'tests'
dest_folder = '.temp'

def replace_variables(file_content):
    for item in SeleniumStore:
        placeholder, replacement = item.value
        file_content = file_content.replace(placeholder, replacement)
    return file_content

def process_side_files(src_folder, dest_folder):
    try:
        os.makedirs(dest_folder, exist_ok=True)
        
        for filename in os.listdir(src_folder):
            if filename.endswith(".side"):
                src_filepath = os.path.join(src_folder, filename)
                dest_filepath = os.path.join(dest_folder, filename)
                
                with open(src_filepath, "r", encoding="utf-8") as file:
                    file_content = file.read()
                
                file_content = replace_variables(file_content)
                
                with open(dest_filepath, "w", encoding="utf-8") as file:
                    file.write(file_content)
                
                print(f"Processed {filename}.")
    
    except FileNotFoundError:
        print(f"The folder {src_folder} does not exist.")
    except IOError as e:
        print(f"An I/O error occurred: {str(e)}")

def run_selenium_side_runner(test_folder):
    try:
        for filename in os.listdir(test_folder):
            if filename.endswith(".side"):
                file_path = os.path.join(test_folder, filename)
                process = subprocess.run(["selenium-side-runner", "--headed", file_path], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(process.stdout)  # Display command output
                
    except subprocess.CalledProcessError as e:
        print(f"The test {file_path} failed to run. Error: {str(e)}")
    except FileNotFoundError:
        print(f"The file or folder {test_folder} does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

#本処理
process_side_files(src_folder, dest_folder)
run_selenium_side_runner(dest_folder)




