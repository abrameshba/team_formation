# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tqdm import tqdm

import Algorithms
import Utilities


class Results:
    def __init__(self):
        self.tot_time = 0
        self.task_size = 0
        self.cardinality = 0
        self.radius = 0
        self.diameter = 0
        self.leader_distance = 0
        self.leader_skill_distance = 0
        self.sum_distance = 0
        self.shannon_task_diversity = 0
        self.shannon_team_diversity = 0
        # self.simpson_task_density = 0
        # self.simpson_team_density = 0
        self.simpson_task_diversity = 0  # task diversity
        self.simpson_team_diversity = 0
        self.gini_simpson_task_diversity = 0  # task diversity
        self.gini_simpson_team_diversity = 0
        self.random_experts = 0

    def clean_it(self):
        self.tot_time = 0
        self.task_size = 0
        self.cardinality = 0
        self.radius = 0
        self.diameter = 0
        self.leader_distance = 0
        self.leader_skill_distance = 0
        self.sum_distance = 0
        self.shannon_task_diversity = 0
        self.random_experts = 0
        self.shannon_team_diversity = 0
        # self.simpson_task_density = 0
        # self.simpson_team_density = 0
        self.simpson_task_diversity = 0  # task diversity
        self.simpson_team_diversity = 0
        self.gini_simpson_task_diversity = 0  # task diversity
        self.gini_simpson_team_diversity = 0

    def __str__(self):
        pass

    def get_heading(self):
        heading = ""
        heading += "Task_size"
        heading += "\t" + "Processing_time"
        heading += "\t" + "Cardinality"
        heading += "\t" + "Radius"
        heading += "\t" + "Diameter"
        heading += "\t" + "Leader_distance"
        heading += "\t" + "Leader_skill_distance"
        heading += "\t" + "Sum_distance"
        # heading += "\t" + "Shannon_task"
        # heading += "\t" + "Shannon_team"
        # # heading += "\t" + "task density"
        # # heading += "\t" + "team density"
        # heading += "\t" + "Simpson_task"  # task diversity
        # heading += "\t" + "Simpson_team"
        # heading += "\t" + "Gini_Simpson_task"  # task diversity
        # heading += "\t" + "Gini_Simpson_team"
        return heading


def main_run(algori):
    import networkx as nx
    year = "2015"
    # for network in ["db"]:
    results = Results()
    networks = ["vldb", "sigmod", "icde", "icdt", "edbt", "pods", "www", "kdd", "sdm", "pkdd", "icdm", "icml",
                "ecml", "colt", "uai", "soda", "focs", "stoc", "stacs", "db", "dm", "ai", "th", "dblp"]
    for network in tqdm(networks):
        print(network)
        graph = nx.read_gml("/home/ramesh/dblp/dblp_" + year + "/" + network + ".gml")
        # skills_name_id_dict = dict()
        # with  open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_titles.txt") as file:
        runs = 10
        tot_tasks = 10
        open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0_" + algori + "_results.txt", "w").close()
        heading = results.get_heading()
        open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0_" + algori + "_results.txt", "a").write(
            heading + "\n")
        open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0_" + algori + "_teams.txt", "w").close()
        with open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0.txt", "r") as file:
            n_lines = Utilities.get_num_lines("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0.txt")
            crun = 0  # cu
            for line in tqdm(file, total=n_lines):
                crun += 1
                # task = dblp_data.get_task_from_title_graph(graph, line.strip("\n").split("\t")[1])
                task = line.strip("\n").split()
                # print(task)
                record = ""
                start_time = time.time()
                team = Algorithms.rarestfirst(graph, task)
                end_time = time.time()
                tg = team.get_team_graph(graph)
                # show_graph(tg)
                results.task_size += len(task)
                results.tot_time += end_time - start_time
                results.cardinality += team.cardinality()
                results.radius += team.radius(tg)
                results.diameter += team.diameter(tg)
                results.leader_distance += team.leader_distance(tg)
                results.leader_skill_distance += team.leader_skill_distance(tg, task)
                results.sum_distance += team.sum_distance(tg, task)
                # results.shannon_task_diversity += team.shannon_task_diversity(graph)
                # results.shannon_team_diversity += team.shannon_team_diversity(graph)
                # results.simpson_task_diversity += team.simpson_diversity(graph, False)  # task diversity
                # results.simpson_team_diversity += team.simpson_diversity(graph, True)
                # results.gini_simpson_task_diversity += team.gini_simpson_diversity(graph, False)  # task diversity
                # results.gini_simpson_team_diversity += team.gini_simpson_diversity(graph, True)
                open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0_" + algori +
                     "_teams.txt", "a").write(",".join(sorted(team.experts)) + "\n")
                if crun % runs == 0:
                    record += str(results.task_size / runs)
                    record += "\t" + str(round(results.tot_time / runs, 3))
                    record += "\t" + str(results.cardinality / runs)
                    record += "\t" + str(results.radius / runs)
                    record += "\t" + str(results.diameter / runs)
                    record += "\t" + str(results.leader_distance / runs)
                    record += "\t" + str(results.leader_skill_distance / runs)
                    record += "\t" + str(results.sum_distance / runs)
                    # record += "\t" + str(results.shannon_task_diversity / runs)
                    # record += "\t" + str(results.shannon_team_diversity / runs)
                    # # record += "\t" + str(team.simpson_task_density(graph))
                    # # record += "\t" + str(team.simpson_team_density(graph))
                    # record += "\t" + str(results.simpson_task_diversity / runs)  # task diversity
                    # record += "\t" + str(results.simpson_team_diversity / runs)
                    # record += "\t" + str(results.gini_simpson_task_diversity / runs)  # task diversity
                    # record += "\t" + str(results.gini_simpson_team_diversity / runs)
                    open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0_" + algori + "_results.txt",
                         "a").write(
                        record + "\n")
                    results.clean_it()


def multiprocessing_func(algo):
    main_run(algo)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import time

    begin_time = time.time()
    main_run("rfs")
    # processes = []
    # for alg in ["rfs"]:
    #     p = multiprocessing.Process(target=multiprocessing_func, args=(alg,))
    #     processes.append(p)
    #     p.start()
    # for process in processes:
    #     process.join()
    tqdm.write('Time taken = {} seconds'.format(time.time() - begin_time))
