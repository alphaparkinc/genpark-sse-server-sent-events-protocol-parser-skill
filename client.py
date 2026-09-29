"""Server-Sent Events (SSE) Protocol Parser.
100% Python Standard Library.
"""

class SSEParser:
    """RFC-compliant Server-Sent Events (SSE) streaming frame parser."""
    def __init__(self):
        self.buffer = ""

    def feed(self, chunk: str) -> list:
        self.buffer += chunk
        events = []
        
        while "\n\n" in self.buffer or "\r\n\r\n" in self.buffer:
            delim = "\r\n\r\n" if "\r\n\r\n" in self.buffer and (self.buffer.find("\r\n\r\n") < self.buffer.find("\n\n") if "\n\n" in self.buffer else True) else "\n\n"
            frame, self.buffer = self.buffer.split(delim, 1)
            
            event_obj = {"event": "message", "data": "", "id": None, "retry": None}
            data_lines = []
            
            for line in frame.splitlines():
                line = line.strip("\r")
                if not line or line.startswith(":"):
                    continue
                if ":" in line:
                    field, val = line.split(":", 1)
                    if val.startswith(" "):
                        val = val[1:]
                    if field == "event":
                        event_obj["event"] = val
                    elif field == "data":
                        data_lines.append(val)
                    elif field == "id":
                        event_obj["id"] = val
                    elif field == "retry":
                        try:
                            event_obj["retry"] = int(val)
                        except ValueError:
                            pass
            
            if data_lines:
                event_obj["data"] = "\n".join(data_lines)
                events.append(event_obj)

        return events
