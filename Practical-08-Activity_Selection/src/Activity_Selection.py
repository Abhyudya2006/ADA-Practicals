import random
import csv
import time

class ActivitySelection:
    def __init__(self):
        pass

    def generate_activities(self, n):
        activities = []
        for _ in range(n):
            start = random.randint(0, 1000)
            end = start + random.randint(1, 100)
            activities.append((start, end))
        return activities

    def activity_selection(self, activities):
        activities.sort(key=lambda x: x[1])
        selected = []
        last_end = -1

        for start, end in activities:
            if start >= last_end:
                selected.append((start, end))
                last_end = end   # fixed placement

        return selected


def performance_analysis():
    obj = ActivitySelection()

    with open("activity_selection_analysis_test2.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Number_of_Activities", "Time_Taken"])

        for n in range(1000, 50001, 1000):
            activities = obj.generate_activities(n)

            # 🔥 Warmup runs (not measured)
            for _ in range(3):
                obj.activity_selection(activities.copy())

            # ✅ Actual measured runs (average)
            runs = 5
            total_time = 0

            for _ in range(runs):
                temp_activities = activities.copy()  # avoid sorted reuse
                start_time = time.perf_counter()
                obj.activity_selection(temp_activities)
                end_time = time.perf_counter()
                total_time += (end_time - start_time)

            avg_time = total_time / runs

            writer.writerow([n, avg_time])
            print(f"Done for {n}")


if __name__ == '__main__':
    performance_analysis()