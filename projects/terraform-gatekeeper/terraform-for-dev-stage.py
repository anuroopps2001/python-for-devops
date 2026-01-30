import subprocess
import sys
import os

def run_terraform(env: str, tf_scripts_dir: str):  # use the variable named 'env' of type str inside the function, Golang style
    print(f"DEBUG: current absolute path: {os.path.abspath(tf_scripts_dir)}")
    print(f"DEBUG: Files found: {os.listdir(tf_scripts_dir)}")

    if not os.path.exists(tf_scripts_dir):
        print(f"❌ Error: The directory '{tf_scripts_dir}' does not exist.")
        return

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

    print(f"📂 Switiching to dir: {tf_scripts_dir}")
    print(f"🚀 Initializing Terraform for {env}...")

    try:
        # subprocess.run is like exec.Command in Go
        # We pass the command as a LIST of strings
        result = subprocess.run(
            ["terraform.exe", "plan", f"-var-file=terraform.tfvars", "-input=false"],
            # By setting -input=false, we are telling Terraform: "If you're missing information, don't ask—just quit."
            cwd=os.path.abspath(tf_scripts_dir),
            check=True,  # Throws an error if the command fails
            text=True,   # Returns output as a string, not bytes
            capture_output=True,  # Captures stdout/stderr
            shell=False,
            timeout=30
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
    raw_path = "../../../udemy-terraform/06-resources/"

    path_to_tf = os.path.abspath(raw_path)

    # Get user input (like fmt.Scanln in Go)
    target_env = input("Enter the environment to deploy (dev/staging/prod): ")
    run_terraform(target_env, path_to_tf)
