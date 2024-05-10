import os
import sys

def find_policy_by_tag(directory, target_tag):
    """
    Search through .rego files in the specified directory,
    looking for a file that includes the specified tag in its header comments.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".rego"):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    for line in f:
                        if line.startswith('# Tags:') and target_tag in line:
                            return path
    return None

if __name__ == "__main__":
    tag_to_find = sys.argv[1] if len(sys.argv) > 2 else 'instance'
    policy_dir = sys.argv[2] if len(sys.argv) > 2 else '.'
    policy_path = find_policy_by_tag(policy_dir, tag_to_find)
    if policy_path:
        print(policy_path)
    else:
        print("No policy file with specified tag found.", file=sys.stderr)
        sys.exit(1)
