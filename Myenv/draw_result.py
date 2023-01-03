import matplotlib.pyplot as plt

input = open('/Users/parkersix/Library/Mobile Documents/com~apple~CloudDocs/PHD相关/MyPaper/Segmentation+Edge/训练结果/log-25000-each10.txt', 'r',encoding="utf-8")

rangeUpdateTime = []
steps = []

for line in input:
    line = line.split()
    if 'reward:' in line:
        rangeUpdateTime.append(float(line[11].replace(',','')))
        steps.append(int(line[7].replace(',','')))


plt.figure('frame time')
plt.plot(steps,rangeUpdateTime)
plt.xlabel("Episods")
plt.ylabel("Mean average cost")
plt.tight_layout()
plt.savefig("25000-each10.pdf")
plt.show()