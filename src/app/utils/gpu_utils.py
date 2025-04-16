import torch

def check_gpu():
    return {
        "available": torch.cuda.is_available(),
        "number of GPUs": torch.cuda.device_count(),
        "GPU name": torch.cuda.get_device_name(0)
    }