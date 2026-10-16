
import re


class SemanticPlanner:
    def __init__(self):
        # Heuristic semantic relevance scores
        self.room_scores = {
            "Fridge": {
                "Kitchen": 0.90,
                "Living Room": 0.05,
                "Bedroom": 0.05
            },
            "Bed": {
                "Bedroom": 0.90,
                "Living Room": 0.08,
                "Kitchen": 0.02
            },
            "TV": {
                "Living Room": 0.80,
                "Bedroom": 0.18,
                "Kitchen": 0.02
            },
            "Sofa": {
                "Living Room": 0.85,
                "Bedroom": 0.10,
                "Kitchen": 0.05
            }
        }

        self.aliases = {
            "refrigerator": "Fridge",
            "fridge": "Fridge",
            "bed": "Bed",
            "television": "TV",
            "tv": "TV",
            "sofa": "Sofa"
        }

    def parse_task(self, task):
        task = task.lower()

        for word, category in sorted(
            self.aliases.items(),
            key=lambda item: -len(item[0])
        ):
            if re.search(r"\b" + re.escape(word) + r"\b", task):
                return category

        raise ValueError("Unsupported target object.")

    def rank_rooms(self, target, candidates):
        scores = self.room_scores[target]

        return sorted(
            candidates,
            key=lambda room: scores.get(room, 0),
            reverse=True
        )
