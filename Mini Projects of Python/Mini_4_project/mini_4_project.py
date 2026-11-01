
def Total(marks):
    total = 0
    for i in marks:
        total += i
    return total

def calculateaverage(marks):
    average = Total(marks)/len(marks)
    return average

def getgrade(average):
    if average>= 75:
        return "Distinction"
    elif average>= 40:
        return "Pass"
    else:
        return "fail"
def builtreport(student):
    total = Total(student["marks"])
    avg = calculateaverage(student["marks"])
    grade = getgrade(avg)

    report = {
        "id" : student["id"],
        "name" : student["name"],
        "marks" : student["marks"],
        "Total" : total,
        "average" : avg,
        "grade" : grade
    }
    return report
def gettopper(records,limit = 75):
    top = filter(lambda r: r["average"]>=limit,records)
    return [r["name"] for r in top] 
students = [{
    "id" : 101, "name" : "prashant" ,"marks" : [78,89,98]
},
{
    "id" : 103, "name" : "jay" ,"marks" : [78,77,87]
}]
records = []
for s in students:
    records.append(builtreport(s))

print("-------------Student Performance-----------")
for r in records:
    print(f"Name:{r["name"]},id:{r["id"]},marks:{r["marks"]}")
    print(f"Total:{r["Total"]}, Average:{r["average"]:.2f}, Grade:{r["grade"]}")
    print()

print("High performers (average >= 75):", gettopper(records))
all_averages = [r["average"] for r in records]
print(f"class average: {calculateaverage(all_averages):.2f}")    

