import subprocess
import os


ALLOWED_ENVS = ['dev', 'staging']
def run_tf_command(action, env, tf_dir):
    cmd = ["terraform.exe", action, "-var-file={env}.tfvars", "-input=false"]

    if action in ["apply", "destroy"]:
        cmd.append("-auto-approve")

    print(f"Executing: terraform {action}...")

    try:
        timeout_val = 600 if action != "plan" else 60

        result = subprocess.run(
            cmd,
            cwd=tf_dir,
            check=True,
            text=True,
            capture_output=True,
            timeout=timeout_val
        )

        print(f"{action.upper()} Completed Successfuly!")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"{action.upper()} Failed!")
        print(e.stderr)

def main():
    
    target_env = input("Enter environment (dev/staging): ").lower()
    path_to_dir = os.path.abspath("../../../udemy-terraform/06-resources")
    
    print("\n--- Terraform Gatekeeper ---")
    print("1. Plan (Safe)")
    print("2. Apply (Changes Infrastructure)")
    print("3. Destroy (DANGER..!!)")

    choice = input("\n Select an action(1-3): ")
    if choice == "1":
            run_tf_command("plan", target_env, path_to_dir)
    elif choice == 2:
         run_tf_command("apply", target_env, path_to_dir)
    elif choice == 3:
         confirm = input(f"confirm DESTROY for {target_env}? (y/n)")
         if confirm.lower == 'y':
              run_tf_command("destroy", target_env, path_to_dir)
    else:
         print("Invalid Choice. Exiting.")
         return
    
if __name__ == "__main__":
     main()

              