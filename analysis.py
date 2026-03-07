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

    # Load student data
    df = pd.read_csv("students.csv")

    # Calculate mid marks
    df["Mid_Final"] = df.apply(calculate_mid, axis=1)

    # Calculate total marks
    df["Total"] = df["Assignment"] + df["Mid_Final"] + df["Semester"]

    # Assign grade
    df["Grade"] = df["Total"].apply(assign_grade)

    # Pass / Fail
    df["Result"] = df["Total"].apply(pass_fail)

    # Ranking
    df["Rank"] = df["Total"].rank(method="min", ascending=False).astype(int)

    # Sort by rank
    df = df.sort_values("Rank")

    print("\n===== STUDENT RESULT ANALYSIS =====\n")

    table = df[[
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
        "Result"
    ]]

    print(table.to_string(index=False))

    # =====================
    # CLASS STATISTICS
    # =====================

    print("\n===== CLASS STATISTICS =====")

    print("Average Marks :", round(df["Total"].mean(),2))
    print("Highest Marks :", round(df["Total"].max(),2))
    print("Lowest Marks  :", round(df["Total"].min(),2))

    top_student = df.iloc[0]

    print("Top Student   :", top_student["Name"], "-", round(top_student["Total"],2))

    # Pass percentage
    pass_count = len(df[df["Result"] == "Pass"])
    total_students = len(df)

    pass_percentage = (pass_count / total_students) * 100

    print("Pass Percentage :", round(pass_percentage,2), "%")
    print("Top Student   :", top_student["Name"], "-", round(top_student["Total"],2))
    # Top 3 Students Leaderboard
    print("\n--- TOP 3 STUDENTS---")

    top3 = df.head(3)

    for i, row in top3.iterrows():
        print(f"{row['Rank']}. {row['Name']} - {round(row['Total'],2)} marks")

    # =====================
    # GRADE DISTRIBUTION
    # =====================

    print("\n===== GRADE DISTRIBUTION =====")

    print(df["Grade"].value_counts())

    # =====================
    # GRAPH
    # =====================

    plt.figure(figsize=(8,5))

    plt.bar(df["Name"], df["Total"])

    plt.title("Student Total Marks")
    plt.xlabel("Students")
    plt.ylabel("Marks")

    plt.tight_layout()

    plt.show()
    # Grade distribution chart

    grade_counts = df["Grade"].value_counts()

    plt.figure(figsize=(6,6))

    plt.pie(
        grade_counts,
        labels=grade_counts.index,
        autopct="%1.1f%%"
    )

    plt.title("Performance of the students")

    plt.show()

if __name__ == "__main__":
    main()