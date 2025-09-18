import torch
import numpy as np

state_dict = torch.load('model/addition_state.pth', map_location='cpu')

def save_state_dict_to_txt(state_dict, filepath="weights.txt"):
    with open(filepath, "w") as f:
        for name, tensor in state_dict.items():
            np_array = tensor.cpu().numpy()

            # Header comment
            f.write(f"# {name} — shape {np_array.shape}\n")

            # Handle 2D weight matrices
            if len(np_array.shape) == 2:
                f.write("[\n")
                for row in np_array:
                    row_str = ", ".join(f"{v:.6f}" for v in row)
                    f.write(f"    [{row_str}],\n")
                f.write("]\n\n")

            # Handle 1D bias vectors
            elif len(np_array.shape) == 1:
                row_str = ", ".join(f"{v:.6f}" for v in np_array)
                f.write(f"[{row_str}]\n\n")

            else:
                f.write(f"# Unsupported tensor shape: {np_array.shape}\n\n")

    print(f"✅ Weights saved to {filepath}")

save_state_dict_to_txt(state_dict)