
import os
import subprocess
import sys

def ensure_folders():
    for folder in ["scripts", "outputs"]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")

def create_default_scripts():
    scripts = {
        "scripts/short.txt": "# Edit this file with your short video script.\nWelcome to my channel! This is a short intro using my cloned voice.",
        "scripts/long.txt": "# Edit this file with your long video script.\nHello everyone, in this video we are going to dive deep into our topic using my cloned voice."
    }
    for path, content in scripts.items():
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(content)
            print(f"Created default script: {path}")

def process_script(file_path):
    if not os.path.exists(file_path):
        return None
    
    lines = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    
    return " ".join(lines)

def main():
    ensure_folders()
    create_default_scripts()

    jobs = [
        {"input": "scripts/short.txt", "output": "outputs/short_voice.wav"},
        {"input": "scripts/long.txt", "output": "outputs/long_voice.wav"}
    ]

    print("--- Starting Batch Voice Generation ---")
    
    for job in jobs:
        text = process_script(job["input"])
        if not text:
            print(f"Skipping {job['input']} (file missing or empty)")
            continue
        
        print(f"\nProcessing: {job['input']} -> {job['output']}")
        
        # Call clone_voice.py via subprocess
        try:
            cmd = [
                sys.executable, 
                "clone_voice.py", 
                text, 
                "--output", job["output"]
            ]
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"FAILED to generate audio for {job['input']}: {e}")

    print("\n--- Batch Process Complete ---")
    print(f"Check the 'outputs' folder for your files.")

if __name__ == "__main__":
    main()
