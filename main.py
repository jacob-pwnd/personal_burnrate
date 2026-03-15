import ollama
import csv
import os

#AI was used to generate this code. Code was tested and verified.
#Model used to generate code: Gemma3

def categorizer_app():
    model_name = 'Categorizer' 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'transactions.csv')
    output_file = os.path.join(script_dir, 'transactions_UPDATED.csv')

    try:
        #Open CSV File Named 'transactions.csv'
        #File must have rows labeled 'Item' 'Type' & 'Category'
        with open(input_file, mode='r', encoding='utf-8-sig') as infile:
            reader = csv.DictReader(infile)
            # Define the headers for the new file (must match the input)
            fieldnames = reader.fieldnames

            #Writing new file with categories
            with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

                print(f"--- Processing Rows ---")
                
                for row in reader:
                    item_name = row.get('Item', '').strip()
                    trans_type = row.get('Type', '').strip()
                    category_val = row.get('Category', '').strip()

                    # Only send item to Ollama if it's a Withdrawal and Category cell is empty
                    if trans_type.lower() == "withdrawal" and not category_val:
                        print(f"Categorizing: {item_name}...")
                        
                        response = ollama.chat(model=model_name, messages=[
                            {'role': 'user', 'content': item_name},
                        ])

                        # Put the Ollama's response into the 'Category' column for this row
                        row['Category'] = response['message']['content'].strip()
                        print(f"   -> Found: {row['Category']}")

                    # Write the row (either updated or original) to the new file. 
                    writer.writerow(row)

        print(f"\n--- Success! ---")
        print(f"Your updated data is saved in: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    categorizer_app()