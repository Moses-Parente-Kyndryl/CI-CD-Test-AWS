import os
import sys

def find_policy(directory, tag):
    """Search for policy files that contain a specific tag in their content."""
    for file_name in os.listdir(directory):
        if file_name.endswith('.rego'):
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r') as file:
                for line in file:
                    if tag in line and line.strip().startswith('# Tags:'):
                        return file_name
    return None

if __name__ == "__main__":
    policy_dir = sys.argv[1]
    tag = sys.argv[2]
    result = find_policy(policy_dir, tag)
    if result:
        print(result)
    else:
        print("No policy file with specified tag found.")
        sys.exit(1)
