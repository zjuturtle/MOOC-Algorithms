class Job:
    def __init__(self, weight: int, length: int):
        self.weight = weight
        self.length = length


def main():
    job_list = []
    with open('jobs.txt', 'r') as file:
        job_num = int(file.readlines(1)[0])
        while len(job_list) != job_num:
            lines = file.readlines(3000)
            for line in lines:
                line = line.split()
                job_list.append(Job(weight=int(line[0]), length=int(line[1])))
    job_list.sort(key=lambda job: job.weight, reverse=True)
    job_list.sort(key=lambda job: job.weight-job.length, reverse=True)
    completion = 0
    time = 0
    for i in range(0, len(job_list)):
        time = time + job_list[i].length
        completion += (time*job_list[i].weight)
    print(completion)


if __name__ == "__main__":
    main()
