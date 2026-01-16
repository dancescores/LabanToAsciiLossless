import json
import os

def parse_laban_block(block):
    """
    Parses a 5-character block [M][D][L][f][r] into a dictionary.
    """
    if block == "....." or block == "     ":
        return {"action": "hold"}
    if block.startswith("X"):
        return {"action": "neutral"}

    # Mapping codes to descriptive values for engine use
    directions = {
        "8": "forward", "2": "backward", "4": "left", "6": "right",
        "7": "fwd_left", "9": "fwd_right", "1": "back_left", "3": "back_right",
        "5": "place", "0": "airborne"
    }
    
    levels = {"^": "high", "-": "middle", "_": "low"}
    modes = {"s": "support", "g": "gesture"}

    return {
        "action": modes.get(block[0], "unknown"),
        "direction": directions.get(block[1], "none"),
        "level": levels.get(block[2], "none"),
        "flexion": "flexed" if block[3] == "v" else ("extended" if block[3] == "!" else "natural"),
        "rotation": "outward" if block[4] == ">" else ("inward" if block[4] == "<" else "natural")
    }

def convert_file(input_path, output_path):
    score_data = []
    
    with open(input_path, 'r') as f:
        for line in f:
            # Skip headers, empty lines, or comments
            clean_line = line.strip()
            if not clean_line or clean_line.startswith(("TIME", "=", "//")):
                continue
            
            # Split line by pipe and clean whitespace
            parts = [p.strip() for p in clean_line.split('|')]
            
            if len(parts) < 7:
                continue

            # Structure the frame
            frame = {
                "timestamp": parts[0],
                "left_arm":  parse_laban_block(parts[1]),
                "left_leg":  parse_laban_block(parts[2]),
                "trunk":     parse_laban_block(parts[3]),
                "right_leg": parse_laban_block(parts[4]),
                "right_arm": parse_laban_block(parts[5]),
                "head":      parse_laban_block(parts[6])
            }
            score_data.append(frame)

    with open(output_path, 'w') as out_f:
        json.dump(score_data, out_f, indent=4)
    print(f"Success! Converted to {output_path}")

# Example usage:
# convert_file("dance_score.txt", "dance_data.json")
