import random
import csv

class ActivitySelection:

    def generate_sparse(self, n):
        activities = []
        for _ in range(n):
            start = random.randint(0, 1000)
            end = start + random.randint(1, 50)   # short duration → less overlap
            activities.append((start, end))
        return activities

    def generate_dense(self, n):
        activities = []
        for _ in range(n):
            start = random.randint(0, 1000)
            end = start + random.randint(100, 300)  # long duration → more overlap
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


def compare_sparse_dense():
    obj = ActivitySelection()

    with open("sparse_dense_ratio.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Total", "Sparse_Ratio", "Dense_Ratio"])

        for n in range(1000, 20001, 1000):

            runs = 5
            sparse_total = 0
            dense_total = 0

            for _ in range(runs):
                # Sparse
                s_act = obj.generate_sparse(n)
                s_sel = obj.activity_selection(s_act)
                sparse_total += len(s_sel)

                # Dense
                d_act = obj.generate_dense(n)
                d_sel = obj.activity_selection(d_act)
                dense_total += len(d_sel)

            avg_sparse = sparse_total / runs
            avg_dense = dense_total / runs

            sparse_ratio = avg_sparse / n
            dense_ratio = avg_dense / n

            writer.writerow([n, sparse_ratio, dense_ratio])
            print(f"Done for n = {n}")


if __name__ == "__main__":
    compare_sparse_dense()