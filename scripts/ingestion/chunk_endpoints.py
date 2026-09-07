import json

def format_record(record):
    text = f"Endpoint: {record['method'].upper()} {record['path']}\n"
    text += f"Summary: {record['summary']}\n"
    if record['description']:
        text += f"Description: {record['description']}\n"

    if record['parameters']:
        text += "Parameters:\n"
        for p in record['parameters']:
            text += f"- {p['name']} ({p['in']}): {p['description']}\n"

    if record['responses']:
        text += "Responses:\n"
        for code, desc in record['responses'].items():
            text += f"- {code}: {desc}\n"

    text += f"Source: {record['externalDocs']}\n"
    return text



def split_text(text, max_chars=2000, overlap_chars=300):
    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        if end < len(text):
            break_point = text.rfind('\n', start, end)
            if break_point == -1 or break_point <= start:
                break_point = end
        else:
            break_point = len(text)

        chunks.append(text[start:break_point])

        next_start = break_point - overlap_chars
        if next_start < 0:
            next_start = 0
        # snap forward to the next space/newline so we never start mid-word
        while next_start < len(text) and text[next_start] not in (' ', '\n'):
            next_start += 1

        start = next_start
        if break_point == len(text):
            break

    return chunks


records = json.load(open('data/processed/endpoints.json'))

all_chunks = []
chunk_id = 0
for record in records:
    text = format_record(record)
    pieces = split_text(text)
    header = f"Endpoint: {record['method'].upper()} {record['path']}\nSummary: {record['summary']}\n"
    for i, piece in enumerate(pieces):
        if i > 0:
            piece = header + "...\n" + piece
        all_chunks.append({
            'chunk_id': chunk_id,
            'path': record['path'],
            'method': record['method'],
            'source_url': record['externalDocs'],
            'text': piece
        })
        chunk_id += 1

print(f"Total chunks: {len(all_chunks)}")
print("--- sample chunk ---")
print(all_chunks[0]['text'])

with open('data/processed/chunks.json', 'w') as f:
    json.dump(all_chunks, f, indent=2)
