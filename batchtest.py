from transformers import pipeline
from torch.utils.data import Dataset
from tqdm.auto import tqdm

pipe = pipeline("text-classification", device=0)


class MyDataset(Dataset):
    def __len__(self):
        return 10000

    def __getitem__(self, i):
        return "This is a test"


dataset = MyDataset()

for batch_size in [64, 256, 512, 1024]: #256 best
    print("-" * 30)
    print(f"Streaming batch_size={batch_size}")
    for out in tqdm(pipe(dataset, batch_size=batch_size), total=len(dataset)):
        pass