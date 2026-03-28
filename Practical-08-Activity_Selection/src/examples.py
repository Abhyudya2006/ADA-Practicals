import random
import csv

class ActivitySelection:
    def __init__(self):
        pass

    def generate_activities(self, n):
        activities = []
        for _ in range(n):
            start = random.randint(0, 50)
            end = start + random.randint(1, 20)
            activities.append((start, end))
        return activities

    def activity_selection(self, activities):
        activities.sort(key=lambda x: x[1])
        selected = []
        last_end = -1

        for start, end in activities:
            if start >= last_end:
                selected.append((start, end))
                last_end = end

        return selected


def generate_examples():
    obj = ActivitySelection()

    with open("activity_selection_examples.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Example No", "Total Activities", "All Activities", "Selected Activities"])

        for i in range(1, 10):   # 5 examples

            # 🔥 Dynamic number of activities (1 to 10)
            n = random.randint(5, 10)

            activities = obj.generate_activities(n)
            selected = obj.activity_selection(activities.copy())

            writer.writerow([
                i,
                n,
                "; ".join([f"({s},{e})" for s,e in activities]),
                "; ".join([f"({s},{e})" for s,e in selected])
            ])

            print(f"Example {i} done (n = {n})")


if __name__ == "__main__":
    generate_examples()