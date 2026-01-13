from pipeline.extractor import extract_constraints
from validate import validate_icr
import json
import sys

def main():
    try:
        print("Reading input...")
        text = open("test.txt").read()

        print("Extracting constraints...")
        output = extract_constraints(text)
        
        print("Validating output...")
        validate_icr(output)
        
        print("\n" + "="*60)
        print("EXTRACTED CONSTRAINTS")
        print("="*60)
        print(json.dumps(output, indent=2))
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total constraints extracted: {len(output['extracted_constraints'])}")
        print(f"Unmodeled rules: {len(output['unmodeled_rules'])}")
   
        with open("output.json", "w") as f:
            json.dump(output, f, indent=2)
        print("\nOutput saved to output.json")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()