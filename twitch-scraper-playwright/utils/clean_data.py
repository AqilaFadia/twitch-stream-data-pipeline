import re

def clean_scraped_data(data):
    cleaned_data = []
    for item in data:
        raw_viewers = str(item.get("viewers", "")).lower().strip()
        raw_viewers = raw_viewers.replace("viewers", "").replace(",", "").strip()
        viewers = 0

        try:
            if "k" in raw_viewers:
                viewers = int(float(raw_viewers.replace("k", "")) * 1000)

            elif "m" in raw_viewers:
                viewers = int(float(raw_viewers.replace("m", "")) * 1_000_000)

            elif raw_viewers.isdigit():
                viewers = int(raw_viewers)

            else:
                match = re.search(r"(\d+(\.\d+)?)", raw_viewers)
                if match:
                    viewers = int(float(match.group(1)))
        except:
            viewers = 0

        # Clean other fields
        cleaned_data.append({
            "title": item.get("title", "").strip(),
            "username": item.get("username", "").strip(),
            "viewers": viewers,
            "timestamp": item.get("timestamp", "").strip()
        })

    return cleaned_data
