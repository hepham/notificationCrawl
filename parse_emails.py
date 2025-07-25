import re
import os

def parse_emails_from_file(input_file, output_dir="parsed_emails"):
    """
    Parse emails from res.txt file and split into individual files
    Each email starts with a number followed by dot and text
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by pattern: number followed by dot and text at start of line
    # Pattern matches: start of line, number, dot, space, text
    email_pattern = r'^(\d+)\.\s+(.+?)(?=^\d+\.\s|\Z)'
    
    # Find all emails using regex with MULTILINE and DOTALL flags
    emails = re.findall(email_pattern, content, re.MULTILINE | re.DOTALL)
    
    print(f"Found {len(emails)} emails")
    
    # Save each email to a separate file
    for i, (email_num, email_content) in enumerate(emails, 1):
        # Clean up the email content
        email_content = email_content.strip()
        
        # Create filename
        filename = f"email_{i}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Write email to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{email_num}. {email_content}")
        
        print(f"Created: {filename}")
    
    print(f"\nSuccessfully parsed {len(emails)} emails into {output_dir}/ directory")

if __name__ == "__main__":
    # Parse emails from res.txt
    parse_emails_from_file("res.txt") 