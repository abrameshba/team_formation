def rarestfirst(l_graph, l_task):
    """
    returns team of experts with minimum diameter distance
    :param l_graph:
    :param l_task:
    :return tuple(set, dictionary, string):
    """
    from Team import Team
    import networkx as nx
    from tqdm import tqdm
    import Utilities
    l_skill_expert = Utilities.get_skill_experts_dict(l_graph)
    rare_skills_support = [min([(len(l_skill_expert[l_skill]), l_skill) for l_skill in l_task], key=lambda x: x[0])]
    # print(rare_skills_support)    # print rarest skill support and skill
    rare_skills = [l_skill for count, l_skill in rare_skills_support]
    min_dd = 100  # minimum diameter distance
    best_team = Team()
    for rare_skill in tqdm(rare_skills, total=len(rare_skills)):
        for candidate in tqdm(l_skill_expert[rare_skill], total=len(l_skill_expert[rare_skill])):
            team = Team()
            for skill in l_task:
                team.task.add(skill)
            team.leader = candidate
            team.experts.add(candidate)
            if candidate not in team.expert_skills:
                team.expert_skills[candidate] = list()
                team.expert_skills[candidate].append(rare_skill)
            else:
                team.expert_skills[candidate].append(rare_skill)
            for l_skill in l_task:
                if l_skill != rare_skill:
                    closest_expert = ""
                    min_distance = 100
                    for expert in l_skill_expert[l_skill]:
                        if expert in l_graph and candidate in l_graph and nx.has_path(l_graph, candidate, expert):
                            distance = nx.dijkstra_path_length(l_graph, candidate, expert, weight="cc")
                            if min_distance > distance:
                                min_distance = distance
                                closest_expert = (expert + ".")[:-1]
                    if len(closest_expert) > 0:
                        team.experts.add(closest_expert)
                        if closest_expert in team.expert_skills:
                            team.expert_skills[closest_expert].append(l_skill)
                        else:
                            team.expert_skills[closest_expert] = list()
                            team.expert_skills[closest_expert].append(l_skill)
            # print(team)
            if team.is_formed():
                dd = team.diameter(l_graph)
                if dd is not None:
                    if min_dd > dd:
                        min_dd = dd
                        best_team = team
    return best_team


def best_sum_distance(l_graph, l_task):
    """
    returns team of experts with minimum sum distance
    :param l_graph:
    :param l_task:
    :return tuple(set, dictionary, string):
    """
    import Utilities
    from Team import Team
    import networkx as nx
    from tqdm import tqdm
    l_skill_expert = Utilities.get_skill_experts_dict(l_graph)
    least_sum_distance = 10000
    best_team = Team()
    for skill_i in tqdm(l_task, total=len(l_task)):
        for candidate in tqdm(l_skill_expert[skill_i], total=len(l_skill_expert[skill_i])):
            team = Team()
            for skill in l_task:
                team.task.add(skill)
            team.leader = candidate
            team.experts.add(candidate)
            if candidate not in team.expert_skills:
                team.expert_skills[candidate] = list()
                team.expert_skills[candidate].append(skill_i)
            else:
                team.expert_skills[candidate].append(skill_i)
            for skill_j in l_task:
                if skill_i != skill_j:
                    min_dis = 100
                    closest_expert = ""
                    for expert in l_skill_expert[skill_j]:
                        if nx.has_path(l_graph, candidate, expert):
                            dis = nx.dijkstra_path_length(l_graph, candidate, expert, weight="cc")
                            if min_dis > dis:
                                min_dis = dis
                                closest_expert = (expert + ".")[:-1]
                    if len(closest_expert) > 0:
                        team.experts.add(closest_expert)
                        if closest_expert not in team.expert_skills:
                            team.expert_skills[closest_expert] = list()
                            team.expert_skills[closest_expert].append(skill_j)
                        else:
                            team.expert_skills[closest_expert].append(skill_j)
            # print(team)
            if team.is_formed():
                sum_dist = team.sum_distance(l_graph, l_task)
                if sum_dist < least_sum_distance:
                    least_sum_distance = sum_dist
                    best_team = team
    return best_team


def tfs(l_graph, l_task, hops, lmbda):  # twice of average degree
    """
    return community based team formation using closest expert.
    :param l_graph:
    :param l_task:
    :return:
    """
    import random
    from Team import Team
    from tqdm import tqdm
    import Utilities
    import networkx as nx
    avg_degree = (2 * l_graph.number_of_edges()) / float(l_graph.number_of_nodes())
    hc = sorted([n for n, d in l_graph.degree() if len(l_graph.nodes[n]) > 0 and
                 d >= lmbda * avg_degree and
                 len(set(l_graph.nodes[n]["skills"].split(",")).intersection(set(l_task))) > 0],
                reverse=True)
    best_team = Team()
    best_ldr_distance = 1000
    # expert_skills = utilities.get_expert_skills_dict(l_graph)
    skill_experts = Utilities.get_skill_experts_dict(l_graph)
    # print(hc)
    for c_node in tqdm(hc, total=len(hc)):
        task_copy = set(l_task)
        # hops = 2
        random_experts = set()
        team = Team()
        # while hops < 3 and len(task_copy) > 0:
        team.clean_it()
        for skill in l_task:
            team.task.add(skill)
        task_copy.update(l_task)
        team.leader = c_node
        skill_cover = set(task_copy).intersection(
            set(l_graph.nodes[team.leader]["skills"].split(",")))  # expert skills matched with l_task
        team.experts.add(c_node)
        if len(skill_cover) > 0:
            if c_node in team.expert_skills:
                for skill in skill_cover:
                    team.expert_skills[c_node].append(skill)
            else:
                team.expert_skills[c_node] = list()
                for skill in skill_cover:
                    team.expert_skills[c_node].append(skill)
        task_copy.difference_update(skill_cover)
        hop_nodes = Utilities.within_k_nbrs(l_graph, c_node, hops)
        nbrhd = []
        # team.clean_it()
        # for skill in l_task:
        #     team.task.add(skill)
        # task_copy.update(l_task)
        # team.leader = c_node
        for node in hop_nodes:
            if len(l_graph.nodes[node])>0:
                skills = set(l_graph.nodes[node]["skills"].split(",")).intersection(task_copy)
                if len(skills) > 0:
                    dis = nx.dijkstra_path_length(l_graph, c_node, node, weight="cc")
                    nbrhd.append([node, skills, dis])
                    # nbrhd.append([node, skills])
        nbrhd.sort(key=lambda elem: (-len(elem[1]), elem[2]))  # sort neighbor hood max skills and min distance
        for nbr in nbrhd:
            if len(nbr[1].intersection(task_copy)) > 0:
                team.experts.add(nbr[0])
                team.expert_skills[nbr[0]] = nbr[1].intersection(task_copy)
                task_copy.difference_update(nbr[1].intersection(task_copy))
        tsk_lst = list(task_copy)
        while len(tsk_lst) > 0:
            skl = random.choice(tsk_lst)
            min_dis = 100
            close_expert = ""
            for expert in skill_experts[skl]:
                if nx.has_path(l_graph, team.leader, expert):
                    dis = nx.dijkstra_path_length(l_graph, team.leader, expert, weight="cc")
                    if min_dis > dis:
                        min_dis = dis
                        close_expert = (expert + ".")[:-1]
            team.experts.add(close_expert)  # first element of neighbor hood
            if close_expert not in team.expert_skills:
                team.expert_skills[close_expert] = list()
                team.expert_skills[close_expert].append(skl)
            else:
                team.expert_skills[close_expert].append(skl)
            tsk_lst.remove(skl)
            random_experts.add(close_expert)
            team.random_experts = random_experts
        if team.is_formed():
            ld = team.leader_skill_distance(l_graph, l_task)
            if best_ldr_distance > ld:
                best_ldr_distance = ld
                best_team = team
    return best_team


def tfr(l_graph, l_task, hops, lmbda):  # twice of average degree
    """
    return community based team formation using closest expert.
    :param l_graph:
    :param l_task:
    :return:
    """
    import random
    from Team import Team
    import Utilities
    from tqdm import tqdm
    import networkx as nx
    avg_degree = (2 * l_graph.number_of_edges()) / float(l_graph.number_of_nodes())
    hc = sorted([n for n, d in l_graph.degree() if len(l_graph.nodes[n]) > 0 and
                 d >= lmbda * avg_degree and
                 len(set(l_graph.nodes[n]["skills"].split(",")).intersection(set(l_task))) > 0],
                reverse=True)
    best_team = Team()
    best_ldr_distance = 1000
    # expert_skills = utilities.get_expert_skills_dict(l_graph)
    skill_experts = Utilities.get_skill_experts_dict(l_graph)
    # print(hc)
    for c_node in tqdm(hc, total=len(hc)):
        task_copy = set(l_task)
        # hops = 2
        random_experts = set()
        team = Team()
        # while hops < 3 and len(task_copy) > 0:
        team.clean_it()
        for skill in l_task:
            team.task.add(skill)
        task_copy.update(l_task)
        team.leader = c_node
        skill_cover = set(task_copy).intersection(
            set(l_graph.nodes[team.leader]["skills"].split(",")))  # expert skills matched with l_task
        team.experts.add(c_node)
        if len(skill_cover) > 0:
            if c_node in team.expert_skills:
                for skill in skill_cover:
                    team.expert_skills[c_node].append(skill)
            else:
                team.expert_skills[c_node] = list()
                for skill in skill_cover:
                    team.expert_skills[c_node].append(skill)
        task_copy.difference_update(skill_cover)
        hop_nodes = Utilities.within_k_nbrs(l_graph, c_node, hops)
        nbrhd = []
        team.clean_it()
        for skill in l_task:
            team.task.add(skill)
        task_copy.update(l_task)
        team.leader = c_node
        for node in hop_nodes:
            if len(l_graph.nodes[node])>0:
                skills = set(l_graph.nodes[node]["skills"].split(",")).intersection(task_copy)
                if len(skills) > 0:
                    dis = nx.dijkstra_path_length(l_graph, c_node, node, weight="cc")
                    nbrhd.append([node, skills, dis])
                    # nbrhd.append([node, skills])
        nbrhd.sort(key=lambda elem: (-len(elem[1]), elem[2]))  # sort neighbor hood max skills and min distance
        for nbr in nbrhd:
            if len(nbr[1].intersection(task_copy)) > 0:
                team.experts.add(nbr[0])
                team.expert_skills[nbr[0]] = nbr[1].intersection(task_copy)
                task_copy.difference_update(nbr[1].intersection(task_copy))
        tsk_lst = list(task_copy)
        while len(tsk_lst) > 0:
            skl = random.choice(tsk_lst)
            random_expert = random.choice(skill_experts[skl])
            team.experts.add(random_expert)
            if random_expert not in team.expert_skills:
                team.expert_skills[random_expert] = list()
                team.expert_skills[random_expert].append(skl)
            else:
                team.expert_skills[random_expert].append(skl)
            tsk_lst.remove(skl)
            random_experts.add(random_expert)
            team.random_experts = random_experts
        if team.is_formed():
            ld = team.leader_skill_distance(l_graph, l_task)
            if best_ldr_distance > ld:
                best_ldr_distance = ld
                best_team = team
    return best_team


def best_leader_distance(l_graph, l_task):
    """
    returns team of experts with minimum leader distance
    :param l_graph:
    :param l_task:
    :return Team :
    """
    import Utilities
    import networkx as nx
    from Team import Team
    from tqdm import tqdm
    l_skill_expert = Utilities.get_skill_experts_dict(l_graph)
    ldr_distance = 1000
    best_team = Team()
    import math
    avg_degree = (2 * l_graph.number_of_edges()) / float(l_graph.number_of_nodes())
    hc = sorted([n for n, d in l_graph.degree() if len(l_graph.nodes[n]) > 0 and
                 d >= 1 * avg_degree and
                 len(set(l_graph.nodes[n]["skills"].split(",")).intersection(set(l_task))) > 0],
                reverse=True)
    for candidate in tqdm(hc, total=len(hc)):
        team = Team()
        for skill in l_task:
            team.task.add(skill)
        team.leader = candidate
        team.experts.add(candidate)
        skill_cover = set()
        if len(l_graph.nodes[team.leader])>0:
            skill_cover = set(l_task).intersection(
                set(l_graph.nodes[team.leader]["skills"].split(",")))  # expert skills matched with l_task
            for skill in skill_cover:
                if candidate in team.expert_skills:
                    team.expert_skills[candidate].append(skill)
                else:
                    team.expert_skills[candidate] = list()
                    team.expert_skills[candidate].append(skill)
        r_skills = set(l_task).difference(skill_cover)
        for skill in r_skills:
            min_dis = 100
            closest_expert = ""
            for expert in l_skill_expert[skill]:
                if nx.has_path(l_graph, candidate, expert):
                    dis = nx.dijkstra_path_length(l_graph, candidate, expert, weight="cc")
                    if min_dis > dis:
                        min_dis = dis
                        closest_expert = (expert + ".")[:-1]
            if len(closest_expert) > 0:
                team.experts.add(closest_expert)
                if closest_expert not in team.expert_skills:
                    team.expert_skills[closest_expert] = list()
                    team.expert_skills[closest_expert].append(skill)
                else:
                    team.expert_skills[closest_expert].append(skill)
        # print(team)
        if team.is_formed():
            cld = team.leader_skill_distance(l_graph, l_task)
            if ldr_distance > cld:
                ldr_distance = cld
                best_team = team
    return best_team


def min_diam_sol(l_graph, l_task, hops):
    """
    Return team generated by Minimum diameter solution algorithm
    :param l_graph:
    :param l_task:
    :param hops:
    :return:
    """
    from tqdm import tqdm
    from Team import Team
    best_team = Team()
    max_dia = 100
    import Utilities
    import networkx as nx
    # skill_id_name_dict = dict()
    # with open("../dblp-2015/db-skills.txt", "r") as file:
    #     for line in file:
    #         line_words = line.strip("\n").split()
    #         skill_id_name_dict[line_words[0]] = line_words[1]
    diamtr_nodes = Utilities.get_diameter_nodes(l_graph)
    for user in tqdm(diamtr_nodes, total=len(diamtr_nodes)):
        team = Team()
        for skill in l_task:
            team.task.add(skill)
        ldnodes = list()
        for node in l_graph.nodes:
            if nx.dijkstra_path_length(l_graph, user, node) <= hops:
                ldnodes.append(node)
            else:
                pass
        pgraph = nx.subgraph(l_graph, ldnodes).copy()  # processed graph excluding nodes hops away from user
        # from networkx.algorithms import bipartite
        for radius in range(1, hops + 1):
            hop_nodes = Utilities.within_k_nbrs(pgraph, user, radius)
            hop_skill_cover = set()
            for node in hop_nodes:
                if node in l_graph and len(l_graph.nodes[node]) >= 2:
                    skls = list(filter(None, l_graph.nodes[node]["skills"].split(",")))
                    hop_skill_cover.update(skls)
            if len(hop_skill_cover.intersection(set(l_task))) == len(l_task):
                # bpt = nx.Graph()
                # for skill in l_task:
                #     bpt.add_node(skill_id_name_dict[skill], bipartite=0)
                # for node1 in hop_nodes:
                #     for skill in l_task:
                #         if len(pgraph.nodes[node1]) >= 2 and skill in pgraph.nodes[node1]["skills"]:
                #             bpt.add_node(node1, bipartite=1)
                #             bpt.add_edge(skill_id_name_dict[skill], node1, weight=1)
                # nx.draw(bpt, with_labels=True)
                # plt.show()
                c_task = set(l_task)
                team.leader = user
                team.experts.add(user)
                skill_cover = set()
                if len(pgraph.nodes[team.leader]) >= 2 and skill in pgraph.nodes[team.leader]["skills"]:
                    skill_cover = set(l_task).intersection(
                    set(pgraph.nodes[team.leader]["skills"].split(",")))  # expert skills matched with l_task
                for skill in skill_cover:
                    if len(skill_cover) > 0 and user not in team.expert_skills:
                        team.expert_skills[user] = list()
                        team.expert_skills[user].append(skill)
                    else:
                        team.expert_skills[user].append(skill)
                c_task.difference_update(skill_cover)
                for hop in range(1, radius + 1):
                    hop_nodes = Utilities.at_k_nbrs(pgraph, user, hop)
                    nbrhd = list()
                    for node in hop_nodes:
                        if len(pgraph.nodes[node]) >= 2:
                            skills = set(pgraph.nodes[node]["skills"].split(",")).intersection(l_task)
                            if len(skills):
                                dis = nx.dijkstra_path_length(pgraph, user, node, weight="cc")
                                nbrhd.append([node, skills, dis])
                    nbrhd.sort(
                        key=lambda elem: (-len(elem[1]), elem[2]))  # sort neighbor hood max skills and min distance
                    for nbr in nbrhd:
                        if len(nbr[1].intersection(c_task)) > 0:
                            team.experts.add(nbr[0])
                            team.expert_skills[nbr[0]] = nbr[1].intersection(c_task)
                            c_task.difference_update(nbr[1].intersection(c_task))
                break
        if team.is_formed():
            cld = team.diameter(l_graph)
            if 0 < cld < max_dia:
                max_dia = cld
                best_team = team
    return best_team


if __name__ == "__main__":
    import networkx as nx
    import Utilities
    # from dblpds import DBLPData
    import random
    import matplotlib.pyplot as plt

    # dblp_dt = DBLPData("2015")
    graph = nx.read_gml("../dblp-2015/db.gml")
    # task = dblp_dt.get_task_from_title_graph(graph,
    # "Novel Approaches in Query Processing for Moving Object Trajectories")
    # task = ["2387", "997", "2633", "792", "481", "2446", "1179", "67", "748", "2222"]   # popular
    # task = ["2628", "1873", "2473", "2622", "2023", "793", "67", "2574", "2645", "1007"]    # rarest
    task = ["1240", "1177", "245", "681"]
    team = tfs(graph, task,1,1)
    tg = team.get_team_graph(graph)
    nx.draw(tg)
    plt.show()


