import pickle

with open("msu_index.pkl", "rb") as f:
    chunks = pickle.load(f)   

print(type(chunks))
print(len(chunks))

for i in range(3):
    print(f"\nChunk {i}:")
    print(repr(chunks[i])[:500])
