class LongTermMemory:

    def __init__(self, db):

        self.db = db


    def remember(
        self,
        category,
        content,
        importance=1,
    ):

        self.db.add_memory(
            category,
            content,
            importance,
        )


    def search(
        self,
        keyword,
    ):

        return self.db.search_memories(keyword)


    def all(
        self,
        category=None,
    ):

        return self.db.get_memories(category)


    def delete(
        self,
        memory_id,
    ):

        self.db.delete_memory(memory_id)