from collections import defaultdict, deque

# har user ke liye last 10 messages yaad
chat_memory = defaultdict(lambda: deque(maxlen=50))
