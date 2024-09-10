import time

def tail_log_file(log_file, label):
    try:
        with open(log_file, 'r') as file:
            file.seek(0, 2)  # Move to the end of the file
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.1)  # Sleep briefly
                    continue
                print(f"[{label}] {line}", end="")
    except KeyboardInterrupt:
        pass

def main():
    from threading import Thread

    # Create threads to tail both log files
    thread_a = Thread(target=tail_log_file, args=("agent_a.log", "Agent_A"))
    thread_b = Thread(target=tail_log_file, args=("agent_b.log", "Agent_B"))

    # Start the threads
    thread_a.start()
    thread_b.start()

    # Wait for threads to complete
    thread_a.join()
    thread_b.join()

if __name__ == "__main__":
    main()
