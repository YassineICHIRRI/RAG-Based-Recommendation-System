from itemadapter import ItemAdapter
import pymongo

class NewsscrapperPipeline:
    
    def __init__(self):
        # Connect to MongoDB
        self.conn = pymongo.MongoClient('localhost', 27017)
        db = self.conn['news']  # Database name
        self.collection = db["almassa_news"]  # Collection name
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Process and normalize content: Flatten nested lists and join into a single string
        content = adapter.get('content', [])
        flattened_content = []
        for paragraph in content:
            if isinstance(paragraph, list):
                flattened_content.extend(paragraph)  
            else:
                flattened_content.append(paragraph) 
        adapter['content'] = ' '.join(flattened_content).strip()

        # Normalize date
        raw_date = adapter.get('date')
        if raw_date:
            try:
                # Arabic month translation to numerical format
                arabic_months = {
                    "يناير": "01", "فبراير": "02", "مارس": "03", "أبريل": "04",
                    "مايو": "05", "يونيو": "06", "يوليو": "07", "أغسطس": "08",
                    "سبتمبر": "09", "أكتوبر": "10", "نوفمبر": "11", "ديسمبر": "12"
                }
                parts = raw_date.split(' ')
                day, month, year = parts[0], arabic_months[parts[1]], parts[2]
                time = parts[-1]
                adapter['date'] = f"{year}-{month}-{day}T{time}"  
            except Exception as e:
                spider.logger.error(f"Date parsing failed: {raw_date} -> {e}")
                adapter['date'] = raw_date  # Fallback to raw date
        
        # Insert the processed item into MongoDB
        try:
            self.collection.insert_one(dict(adapter))  
        except pymongo.errors.PyMongoError as e:
            spider.logger.error(f"Failed to insert item into MongoDB: {e}")
        
        return item
