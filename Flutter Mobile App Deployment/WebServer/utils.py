import torch
from torchvision.utils import save_image

def load_checkpoint(checkpoint_file, model, optimizer, lr, device):
    print("=> Loading checkpoint")
    checkpoint = torch.load(checkpoint_file, map_location=device)
    
    state_dict = checkpoint["state_dict"]
    
    # If the keys are prefixed with "module.", remove it
    new_state_dict = {}
    for k, v in state_dict.items():
        if k.startswith("module."):
            new_state_dict[k[7:]] = v  # Remove the "module." part
        else:
            new_state_dict[k] = v

    # print(new_state_dict.keys())
    model.load_state_dict(new_state_dict)
    optimizer.load_state_dict(checkpoint["optimizer"])

    # If we don't do this then it will just have learning rate of old checkpoint
    # and it will lead to many hours of debugging \:
    for param_group in optimizer.param_groups:
        param_group["lr"] = lr

