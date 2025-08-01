import subprocess

def run_script(script_path):
    try:
        print(f"🚀 Running: {script_path}")
        subprocess.run(["python", script_path], check=True)
        print(f"✅ Finished: {script_path}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_path}: {e}")

if __name__ == "__main__":
    # Paths to your scripts
    normalization_script = "1 - Normalization.py"
    tokenization_script = "2 - Tokenization.py"
    vectorization_script = "3 - Vectorization.py"

    # Run each step in order
    run_script(normalization_script)
    run_script(tokenization_script)
    run_script(vectorization_script)

    print("🎯 Pipeline completed successfully.")
