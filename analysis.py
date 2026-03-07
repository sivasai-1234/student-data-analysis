import pandas as pd
import matplotlib.pyplot as plt


# Calculate Mid marks (80% higher mid + 20% lower mid)
def calculate_mid(row):
    higher = max(row["Mid1"], row["Mid2"])
    lower = min(row["Mid1"], row["Mid2"])
    return (0.8 * higher) + (0.2 * lower)


# Assign grade
def assign_grade(total):

    if total >= 90:
        return "A"
    elif total >= 75:
        return "B"
    elif total >= 60:
        return "C"
    elif total >= 50:
        return "D"
    else:
        return "F"


# Pass / Fail
def pass_fail(total):

    if total >= 50:
        return "Pass"
    else:
        return "Fail"


def main():

    # Load student data from Excel
    df = pd.read_excel("students.xlsx")

    # Mid calculation
    df["Mid_Final"] = df.apply(calculate_mid, axis=1)

    # Total marks
    df["Total"] = df["Assignment"] + df["Mid_Final"] + df["Semester"]

    # Grade
    df["Grade"] = df["Total"].apply(assign_grade)

    # Result
    df["Result"] = df["Total"].apply(pass_fail)

    # Rank
    df["Rank"] = df["Total"].rank(method="min", ascending=False).astype(int)

    df = df.sort_values("Rank")

    print("\n===== STUDENT RESULT ANALYSIS =====\n")

    table = df[
        [
            "Rank",
            "Roll_No",
            "Name",
            "Assignment",
            "Mid1",
            "Mid2",
            "Mid_Final",
            "Semester",
            "Total",
            "Grade",
            "Result",
        ]
    ]

    print(table.to_string(index=False))

    # =====================
    # CLASS STATISTICS
    # =====================

    print("\n===== CLASS STATISTICS =====")

    print("Average Marks :", round(df["Total"].mean(), 2))
    print("Highest Marks :", round(df["Total"].max(), 2))
    print("Lowest Marks  :", round(df["Total"].min(), 2))

    top_student = df.iloc[0]

    print("Top Student   :", top_student["Name"], "-", round(top_student["Total"], 2))

    # Pass percentage
    pass_count = len(df[df["Result"] == "Pass"])
    total_students = len(df)

    pass_percentage = (pass_count / total_students) * 100

    print("Pass Percentage :", round(pass_percentage, 2), "%")
    # =====================
    # PERFORMANCE INSIGHTS
    # =====================

    print("\n===== PERFORMANCE INSIGHTS =====")

    # Class performance summary
    avg = df["Total"].mean()

    if avg >= 85:
        print("Class Performance: Excellent")
    elif avg >= 70:
        print("Class Performance: Good")
    elif avg >= 60:
        print("Class Performance: Average")
    else:
        print("Class Performance: Needs Improvement")


    # Hardest exam component
    assignment_avg = df["Assignment"].mean()
    mid_avg = df["Mid_Final"].mean()
    semester_avg = df["Semester"].mean()

    components = {
        "Assignment": assignment_avg,
        "Mid Exam": mid_avg,
        "Semester Exam": semester_avg
    }

    hardest = min(components, key=components.get)

    print("Hardest Component:", hardest)


    # Students needing improvement
    print("\nStudents Needing Improvement:")

    weak_students = df[df["Total"] < avg]

    if len(weak_students) == 0:
        print("None")
    else:
        print(weak_students[["Name","Total"]].to_string(index=False))

    # =====================
    # FAILING STUDENTS
    # =====================

    print("\n===== STUDENTS AT RISK =====")

    fail_students = df[df["Result"] == "Fail"]

    if len(fail_students) == 0:
        print("None 🎉")
    else:
        print(fail_students[["Name", "Total"]].to_string(index=False))

    # =====================
    # TOP 3 STUDENTS
    # =====================

    print("\n===== TOP 3 STUDENTS =====")

    top3 = df.head(3)

    for i, row in top3.iterrows():
        print(f"{row['Rank']}. {row['Name']} - {round(row['Total'],2)} marks")

    # =====================
    # GRADE DISTRIBUTION
    # =====================

    print("\n===== GRADE DISTRIBUTION =====")

    print(df["Grade"].value_counts())

    # =====================
    # BAR CHART
    # =====================

    sorted_df = df.sort_values("Rank")

    plt.figure(figsize=(8,5))
    plt.bar(sorted_df["Name"], sorted_df["Total"])

    plt.title("Student Total Marks")
    plt.xlabel("Students")
    plt.ylabel("Marks")

    plt.tight_layout()

    plt.savefig("marks_chart.png")

    plt.show()

    # =====================
    # PIE CHART
    # =====================

    grade_counts = df["Grade"].value_counts()

    plt.figure(figsize=(6,6))

    plt.pie(
        grade_counts,
        labels=grade_counts.index,
        autopct="%1.1f%%"
    )

    plt.title("Class Performance by Grade")

    plt.savefig("grade_chart.png")

    plt.show()

    # =====================
    # EXPORT REPORT
    # =====================

    df.to_excel("student_report.xlsx", index=False)

    print("\nReport exported successfully: student_report.xlsx")


if __name__ == "__main__":
    main()