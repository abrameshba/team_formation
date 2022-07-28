def list_to_freq(wordlist) -> dict:
    """
    return dictionary generated from given list
    :param wordlist:
    :return:
    """
    word_freq = dict()
    for word in wordlist:
        if word not in word_freq:
            word_freq[word] = 1
        else:
            word_freq[word] += 1
    return word_freq


# Ref: https://stackoverflow.com/questions/18393842/k-th-order-neighbors-in-graph-python-networkx
def within_k_nbrs(l_gra, start, k):
    nbrs = {start}
    for _ in range(k):
        nbrs = set((nbr for n in nbrs for nbr in l_gra[n]))
    return nbrs

def at_k_nbrs(l_gra, start, k):
    sub = within_k_nbrs(l_gra, start, k)
    sup = within_k_nbrs(l_gra, start, k-1)
    return sub.difference(sup)

# Ref: https://thispointer.com/python-check-if-any-string-is-empty-in-a-list/
def is_empty_or_blank(msg):
    """ This function checks if given string is empty
     or contain only shite spaces"""
    import re
    return re.search("^ *$", msg)


# Ref: https://stackoverflow.com/questions/18393842/k-th-order-neighbors-in-graph-python-networkx
def knbrcover(l_graph, start, k):
    nbrs = within_k_nbrs(l_graph, start, k)
    dnbrs = nbrs.copy()
    hopskillcover = set()
    for n in dnbrs:
        if len(l_graph.nodes[n]) > 0:
            skls = list(filter(None, l_graph.nodes[n]["skills"].split(",")))
            if len(skls) == 0:
                nbrs.remove(n)
            else:
                hopskillcover.update(skls)
    return hopskillcover


def get_expert_skills_dict(graph):
    expert_skills = dict()
    for node in graph.nodes():
        if len(graph.nodes[node]) > 0:
            expert_skills[node] = graph.nodes[node]["skills"].split(",")
    return expert_skills


# ref : https://blog.nelsonliu.me/2016/07/30/progress-bars-for-python-file-reading-with-tqdm/
def get_num_lines(file_path):
    fp = open(file_path, "r+")
    import mmap
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines


# function to return key for any value
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key


def remove_numbers_symbols(instring):
    import re
    result1 = re.sub(r'[^\w]', ' ', instring)
    result = ''.join([i for i in result1 if not i.isdigit()])
    return result


def show_mygraph(d_graph):
    import networkx as nx
    import matplotlib.pyplot as plt
    pos = nx.spring_layout(d_graph)  # pos = nx.nx_agraph.graphviz_layout(G)
    nx.draw_networkx(d_graph, pos)
    labels = nx.get_edge_attributes(d_graph, 'weight')
    nx.draw_networkx_edge_labels(d_graph, pos, edge_labels=labels)
    plt.show()

# Ref : https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
def key_with_max_val(dictnry):
    """ a) create a list of the dict's keys and values;
        b) return the key with the max value"""
    v = list(dictnry.values())
    k = list(dictnry.keys())
    return k[v.index(max(v))]

def get_diameter_nodes(l_graph):
    """
    return diameter of graph formed by team
    diam(X) := max{sp_{X}(u,v) | u,v ∈ X}.
    :param l_graph:
    :return:
    """
    import networkx as nx
    # t_graph = self.get_team_graph(l_graph)
    if nx.number_of_nodes(l_graph) < 2:
        return 0
    else:
        spl = dict()
        for nd in l_graph.nodes:
            spl[nd] = nx.single_source_dijkstra_path_length(l_graph, nd)
        eccentrct = nx.eccentricity(l_graph, sp=spl)
        sour = key_with_max_val(eccentrct)  # source
        dest = key_with_max_val(nx.single_source_dijkstra(l_graph, sour)[0])  # destination
        return nx.dijkstra_path(l_graph, sour, dest)

# class DBLPRecord:
#
#     def __init__(self):
#         self.title = ""
#         self.authors = set()
#         self.year = ""
#         self.journal = ""


# def get_task_graph(l_graph, l_task):
#     """
#     return subgraph experts with shortest paths among
#     :param l_task:
#     :param l_graph:
#     :return dict:
#     """
#     task_experts = set()
#     skill_set = set(l_task)
#     for node in l_graph.nodes():
#         if len(l_graph.nodes[node]) > 0:
#             if len(set(l_graph.nodes[node]["skills"].split(",")).intersection(skill_set)) > 0:
#                 task_experts.add(node)
#     return l_graph.subgraph(task_experts).copy()


def get_skill_experts_dict(l_graph) -> dict:
    """
    return skill expert community dictionary for input l_graph
    :param l_graph:
    :return dict:
    """
    skill_experts = dict()
    for node in l_graph.nodes():
        if len(l_graph.nodes[node]) > 0:
            for skill in l_graph.nodes[node]["skills"].split(","):
                if skill in skill_experts:
                    skill_experts[skill].append(node)
                elif skill not in skill_experts:
                    skill_experts[skill] = list([node])
                else:
                    pass
    return skill_experts


def get_cmnt_skills_from_pub(publication) -> list:
    """
    returns non trivial words of publication as skills packed in set
    used to get skills of an expert
    non trivial keywords that appear at least twice in his/her publications are skills
    :param publication:
    :return:
    """
    from nltk import word_tokenize
    import re
    from nltk.corpus import stopwords
    all_words = word_tokenize(re.sub(r'[^a-zA-Z]', ' ', publication))
    filtered_words = set()
    from nltk.corpus import brown
    setofwords = set(brown.words())
    for word in all_words:
        if word.lower() not in stopwords.words('english') and len(word) > 2:
            filtered_words.add(word.lower())
    lst = list(filtered_words.intersection(setofwords))
    return sorted(lst)


def get_dblp_skills_from_pub(publication) -> list:
    """
    returns non trivial words of publication as skills packed in set
    used to get skills of an expert
    non trivial keywords that appear at least twice in his/her publications are skills
    :param publication:
    :return:
    """
    from nltk import word_tokenize
    import re
    from nltk.corpus import stopwords
    all_words = word_tokenize(re.sub(r'[^a-zA-Z]', ' ', publication))
    filtered_words = list()
    skills = set()
    from nltk.corpus import brown
    setofwords = set(brown.words())
    for word in all_words:
        if word.lower() not in stopwords.words('english') and len(word) > 2:
            filtered_words.append(word.lower())
    local_dict = list_to_freq(filtered_words)
    for word, freq in local_dict.items():
        if freq > 1 and word in setofwords:  # check non trivial words that appear at least twice
            skills.add(word.lower())
    lst = list(skills)
    return sorted(lst)