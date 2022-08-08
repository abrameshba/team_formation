# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tqdm import tqdm

import Algorithms
import main_rarestfirst
import Utilities


def main_run(algori):
    import networkx as nx
    year = "2015"
    # for network in ["db"]:
    results = main_rarestfirst.Results()
    # networks = ["dblp"]
    networks = ["vldb", "sigmod", "icde", "icdt", "edbt", "pods", "www", "kdd", "sdm", "pkdd", "icdm", "icml",
                "ecml", "colt", "uai", "soda", "focs", "stoc", "stacs", "db", "dm", "ai", "th", "dblp"]
    # , "sigmod", "icde", "icdt", "edbt", "pods"
    cs = set()
    for network in tqdm(networks):
        # vldb = nx.read_gml("/home/ramesh/dblp/dblp_" + year + "/vldb.gml")
        graph = nx.read_gml("/home/ramesh/dblp/dblp_" + year + "/" + network + ".gml")
        skill_freq = dict()
        total = 0
        skill_experts = Utilities.get_skill_experts_dict(graph)
        for skill in skill_experts:
            if len(skill_experts[skill]) in skill_freq:  # skill with same number of experts
                skill_freq[len(skill_experts[skill])] += 1
            else:
                skill_freq[len(skill_experts[skill])] = 1
            total += len(skill_experts[skill])
        experts_per_skill = round(total / len(skill_experts), 2)
        for skill in skill_experts:
            if len(skill_experts[skill]) >= experts_per_skill:
                cs.add(skill)
            else:
                if len(skill_experts[skill]) <= 3:
                    # rare_skills.add(skill)
                    pass
                else:
                    cs.add(skill)  # rare skills
        print(network)
        graph = nx.read_gml("/home/ramesh/dblp/dblp_" + year + "/" + network + ".gml")
        # skills_name_id_dict = dict()
        # with  open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_titles.txt") as file:
        runs = 10
        tot_tasks = 10
        open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0_" + algori + "_results2.txt", "w").close()
        heading = results.get_heading()
        open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0_" + algori + "_results2.txt", "a").write(
            heading + "\n")
        open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0_" + algori + "_teams2.txt", "w").close()
        with open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0.txt", "r") as file:
            n_lines = Utilities.get_num_lines("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0.txt")
            crun = 0  # cu
            for line in tqdm(file, total=n_lines):
                crun += 1
                # task = dblp_data.get_task_from_title_graph(graph, line.strip("\n").split("\t")[1])
                task = line.strip("\n").split()
                # print(task)
                if len(set(task).intersection(cs)) < len(task):
                    # print(task)
                    continue
                record = ""
                start_time = time.time()
                team = Algorithms.tfs(graph, task, 2, 2)
                end_time = time.time()
                tg = team.get_team_graph(graph)
                # show_graph(tg)
                results.task_size += len(task)
                results.tot_time += end_time - start_time
                results.cardinality += team.cardinality()
                # results.radius += team.radius(tg)
                results.radius += 0
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
                     "_teams2.txt", "a").write(",".join(sorted(team.experts)) + "\n")
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
                    open("/home/ramesh/dblp/dblp_" + year + "/" + network + "_" + str(tot_tasks) + "_0_" + algori + "_results2.txt",
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
    main_run("tfs")
    # processes = []
    # for alg in ["rfs"]:
    #     p = multiprocessing.Process(target=multiprocessing_func, args=(alg,))
    #     processes.append(p)
    #     p.start()
    # for process in processes:
    #     process.join()
    tqdm.write('Time taken = {} seconds'.format(time.time() - begin_time))
