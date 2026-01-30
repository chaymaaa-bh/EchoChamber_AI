import pandas as pd
import os
import re

def parse_ascii_structure(lines):
    """
    Parses the ASCII tree structure to find parent-child relationships and depth.
    """
    rows = []
    stack = {} # Stores the last ID found at each indentation level
    current_post_id = None
    
    for line in lines:
        if "For Post ID:" in line:
            current_post_id = line.split(":")[-1].strip()
            # The post itself is at level -1 or 0 depending on the file
            stack = {0: current_post_id} 
            continue
            
        # Find the comment_id (usually 7 alphanumeric characters)
        match = re.search(r'([a-z0-9]{7})', line)
        if match:
            comment_id = match.group(1)
            # Indentation level tells us the depth in the conversation
            level = line.find(comment_id)
            
            # Find the parent: the closest previous ID with a lower level
            parent_id = None
            for last_level in sorted(stack.keys(), reverse=True):
                if last_level < level:
                    parent_id = stack[last_level]
                    break
            
            rows.append({
                'comment_id': comment_id,
                'parent_id': parent_id,
                'post_id': current_post_id,
                'depth': level // 4  # Estimating depth based on common 4-space indentation
            })
            stack[level] = comment_id # Update stack
            
    return pd.DataFrame(rows)

def perform_feature_engineering(df):
    """
    Creates 10+ features for the project requirements.
    """
    # 1-5. Existing: comment_id, body, score, parent_id, post_id
    
    # 6. Text length (characters)
    df['char_count'] = df['body'].astype(str).str.len()
    
    # 7. Word count
    df['word_count'] = df['body'].apply(lambda x: len(str(x).split()))
    
    # 8. Average word length
    df['avg_word_len'] = df['char_count'] / (df['word_count'] + 1)
    
    # 9. Is it a root comment? (Directly replying to the post)
    df['is_root'] = (df['parent_id'] == df['post_id']).astype(int)
    
    # 10. Target Binary (1 for toxic, 0 for neutral/positive)
    df['target_binary'] = (df['score'] > 0).astype(int)
    
    # 11. Thread Position (Depth) already added in parser
    
    return df

if __name__ == "__main__":
    # FILE PATHS - Ensure these match your MacBook folder exactly
    RAW_CSV = 'data/raw/ruddit_comments_score.csv'
    RAW_STRUCT = 'data/raw/Thread_structure.txt'
    OUTPUT = 'data/processed/full_dataset.csv'

    print("--- Starting EchoChamber AI Data Pipeline ---")
    
    if os.path.exists(RAW_CSV) and os.path.exists(RAW_STRUCT):
        # 1. Load data
        df_text = pd.read_csv(RAW_CSV)
        with open(RAW_STRUCT, 'r') as f:
            lines = f.readlines()
        
        # 2. Parse the ASCII tree
        print("Parsing thread structure...")
        df_struct = parse_ascii_structure(lines)
        
        # 3. Merge text/scores with hierarchy
        df_final = df_text.merge(df_struct, on='comment_id', how='inner')
        
        # 4. Feature Engineering
        print("Creating features...")
        df_final = perform_feature_engineering(df_final)
        
        # 5. Save
        os.makedirs('data/processed', exist_ok=True)
        df_final.to_csv(OUTPUT, index=False)
        
        print(f"\nSUCCESS! File saved at: {OUTPUT}")
        print(f"Total rows: {len(df_final)}")
        print(f"Total columns: {len(df_final.columns)}")
        print(f"Columns: {df_final.columns.tolist()}")
    else:
        print(f"ERROR: Files not found. Check {RAW_CSV} and {RAW_STRUCT}")