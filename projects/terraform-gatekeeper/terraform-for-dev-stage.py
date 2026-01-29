import subprocess
import sys

def run_terraform(env: str):  # use the variable named 'env' of type str inside the function, Golang style
    """
    Acts as a wrapper to run Terraform based on the environment.
    """
    if env.lower() == "prod":
        print("❌ CRITICAL: Automatic execution blocked for PROD.")
        print("Please use the manual CI/CD pipeline for Production changes.")
        return # When a return statement is executed, the function immediately terminates, 
               # and any code that follows it within the function's block is not run

    if env.lower() not in ['dev', 'staging']:
        print(f"❓ Unknown environment: {env}. Use 'dev' or 'staging'.")  # 'f' to update {env} with actual value

    print(f"🚀 Initializing Terraform for {env}...")

    try:
        # subprocess.run is like exec.Command in Go
        # We pass the command as a LIST of strings
        result = subprocess.run(
            ["terraform", "plan", "-var", f"-var={env}"],
            check=True,  # Throws an error if the command fails
            text=True,   # Returns output as a string, not bytes
            capture_output=True  # Captures stdout/stderr
        )
        # If you aren't sure what a variable can do, print the dir() of it. It lists every method 
        # and attribute available. like, print(dir(result))

        print("--- Terraform Plan Output ---")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"💥 Terraform failed!")
        print(e.stderr) # error stored as e variable and calling method stderr
    except FileNotFoundError:
        print("📂 Error: Terraform is not installed or not in your PATH.")


# --- Main Execution ---
if __name__ == "__main__":
    # Get user input (like fmt.Scanln in Go)
    target_env = input("Enter the environment to deploy (dev/staging/prod): ")
    run_terraform(target_env)
