
!pip uninstall tensorflow


!pip install tensorflow[gpu]

!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

nvcc --version

nvidia-smi

import tensorflow as tf
print("TensorFlow version:", tf.__version__)
print("GPU available:", tf.config.list_physical_devices('GPU'))
print("CUDA available:", tf.test.is_built_with_cuda())

import torch
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("CUDA version:", torch.version.cuda)
if torch.cuda.is_available():
    print("GPU device:", torch.cuda.get_device_name(0))




echo %PATH%
# Make sure CUDA paths are included

