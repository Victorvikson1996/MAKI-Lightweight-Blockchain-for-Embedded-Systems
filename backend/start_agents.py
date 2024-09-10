import subprocess

def start_agent(agent_script, log_file):
    # Start the agent and redirect stdout and stderr to the log file
    return subprocess.Popen(["python", agent_script], stdout=log_file, stderr=log_file, text=True)

def main():
    # Open log files for both agents
    log_file_a = open("agent_a.log", "w")
    log_file_b = open("agent_b.log", "w")

    # Start both agents
    process_a = start_agent("agent_a.py", log_file_a)
    process_b = start_agent("agent_b.py", log_file_b)

    # Wait for both processes to complete
    process_a.wait()
    process_b.wait()

    # Close log files
    log_file_a.close()
    log_file_b.close()

if __name__ == "__main__":
    main()
