import csv
from collections import defaultdict
from tabulate import tabulate

def process_data():
    data = defaultdict(lambda: defaultdict(int))  
    totals = defaultdict(int)                      

    try:
        with open('weightdata.csv', 'r') as file:  
            reader = csv.reader(file)
            header = next(reader)  

            for row in reader:
                gender = row[0]
                normal_weight = int(row[1])
                o1 = int(row[2])
                o2 = int(row[3])

                data[gender]['Normal'] += normal_weight
                data[gender]['Overweight1'] += o1
                data[gender]['Overweight2'] += o2

                totals['Normal'] += normal_weight
                totals['Overweight1'] += o1
                totals['Overweight2'] += o2

        gender_totals = {g: sum(data[g].values()) for g in data}
        overall_total = sum(totals.values())

        table = []
        for g in data:
            normal_count = data[g]['Normal']
            overweight1_count = data[g]['Overweight1']
            overweight2_count = data[g]['Overweight2']
            g_total = gender_totals[g]
            t_wt_normal = (normal_count / g_total * 100) if g_total > 0 else 0
            t_wt_overweight1 = (overweight1_count / g_total * 100) if g_total > 0 else 0
            t_wt_overweight2 = (overweight2_count / g_total * 100) if g_total > 0 else 0

            d_wt_normal = (normal_count / totals['Normal'] * 100) if totals['Normal'] > 0 else 0
            d_wt_overweight1 = (overweight1_count / totals['Overweight1'] * 100) if totals['Overweight1'] > 0 else 0
            d_wt_overweight2 = (overweight2_count / totals['Overweight2'] * 100) if totals['Overweight2'] > 0 else 0

            row = [
                g,
                normal_count,
                f"{t_wt_normal:.2f}%",
                f"{d_wt_normal:.2f}%",
                overweight1_count,
                f"{t_wt_overweight1:.2f}%",
                f"{d_wt_overweight1:.2f}%",
                overweight2_count,
                f"{t_wt_overweight2:.2f}%",
                f"{d_wt_overweight2:.2f}%",
                g_total,
                f"{(g_total / overall_total * 100):.2f}%"
            ]
            table.append(row)

        t_wt_total_normal = (totals['Normal'] / overall_total * 100) if overall_total > 0 else 0
        t_wt_total_overweight1 = (totals['Overweight1'] / overall_total * 100) if overall_total > 0 else 0
        t_wt_total_overweight2 = (totals['Overweight2'] / overall_total * 100) if overall_total > 0 else 0

        total_row = [
            "Total",
            totals['Normal'],
            f"{t_wt_total_normal:.2f}%",
            "100.00%",  
            totals['Overweight1'],
            f"{t_wt_total_overweight1:.2f}%",
            "100.00%",  
            totals['Overweight2'],
            f"{t_wt_total_overweight2:.2f}%",
            "100.00%",  
            overall_total,
            "100.00%"
        ]
        table.append(total_row)

        headers = [
            "Gender",
            "Normal Count", "t-wt", "d-wt",
            "Overweight I Count", "t-wt ", "d-wt ",
            "Overweight II Count", "t-wt ", "d-wt",
            "Total Count", "t-wt (Total)"
        ]

        print(tabulate(table, headers=headers, tablefmt='plain'))

    except FileNotFoundError:
        print("Couldn't open file")
        return

process_data()
