from client import SSEParser

parser = SSEParser()
chunk = "event: delta\ndata: {\"token\": \"Hello\"}\n\nevent: delta\ndata: {\"token\": \" World\"}\n\n"
events = parser.feed(chunk)
print(f"Parsed {len(events)} events:")
for e in events:
    print(f"Event: {e['event']} | Data: {e['data']}")
