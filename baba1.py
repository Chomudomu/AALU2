import requests
import subprocess
import time
import schedule
import threading
import config


def keep_codespace_active():
    while True:
        try:
              # Send a GET request to your Codespace URL
            response = requests.get(config.CODESPACE_URL)
            if response.status_code == 200:
                print("Codespace is active.")
            else:
                print(f"Failed to keep Codespace active. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
             print(f"Waiting for {config.REQUEST_INTERVAL} seconds before the next request...")
        time.sleep(config.REQUEST_INTERVAL)
        

def run_bot():
    try:
        # Start the bot process
        print("Starting the bot...")
        process = subprocess.Popen(['python', 'baba.py'])
        process.wait()  # Wait for the process to complete
        if process.returncode != 0:
            raise Exception(f"Bot crashed with return code {process.returncode}")
    except Exception as e:
        print(f"Bot crashed with exception: {e}")
        print("Restarting bot in 5 seconds...")
        time.sleep(5)
        run_bot()  # Restart the bot

def schedule_bot():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Schedule the bot to run every 3 hours
schedule.every(3).hours.do(run_bot)

def make_executable():
    try:
        # Change permissions of all files in the current directory to be executable
        subprocess.run('chmod +x *', shell=True, check=True)
        print("All files in the current directory are now executable.")
    except subprocess.CalledProcessError as e:
        print(f"Error making files executable: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
if __name__ == "__main__":
    print("Starting Codespace activity keeper and bot scheduler...")

    make_executable()  # Properly indented

    # Start the keep_codespace_active function in a separate thread
    keep_alive_thread = threading.Thread(target=keep_codespace_active)
    keep_alive_thread.daemon = True  # Ensuring the thread doesn't block the program from exiting
    keep_alive_thread.start()
    
    # Initial run to start the bot immediately
    run_bot()
    
    # Start the schedule loop
    schedule_bot()