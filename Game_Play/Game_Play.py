from collections import defaultdict
import time


def read_input():
    board_1d = defaultdict(int)
    with open("input6.txt", "r") as infile:
    # with open("/home/surbhi/IdeaProjects/ai_hw2/test/input0297.txt", "r") as infile:
    # with open("input_22.txt", "r") as infile:
        data = infile.readlines()

    beds = int(data[0])
    parking = int(data[1])
    L = int(data[2])
    L_ids_string = data[3:L+3]
    S = int(data[L+3])
    S_ids_string = data[L+4:L+S+4]
    total_applicants = int(data[L+S+4])
    all_applicants = data[L+S+5:L+S+5+total_applicants]

    L_ids = set()
    for id in L_ids_string:
        L_ids.add(id.strip())

    S_ids = set()
    for id in S_ids_string:
        S_ids.add(id.strip())

    beds_dictionary = {}
    for j in range(7):
        beds_dictionary[j+1] = beds

    parking_dict = {}
    for j in range(7):
        parking_dict[j+1] = parking

    applicants = {}

    for app in all_applicants:
        app_id = app[0:5]
        app_gender = app[5]
        app_age = int(app[6:9])
        pets = app[9]
        medical_condns = app[10]
        car = app[11]
        licence = app[12]

        days = []
        daycount = 0
        for day in range(13,20):
            if app[day] == '1':
                days.append(abs(13-day)+1) #days 1 to 7 mon to sun
                daycount+=1

        if car == 'Y' and licence == 'Y' and medical_condns == 'N':
            valid_spla = True
        else:
            valid_spla = False

        if app_gender == 'F' and app_age > 17 and pets == 'N':
            valid_lahsa = True
        else:
            valid_lahsa = False

        applicants[app_id] = (app_gender, app_age, pets, medical_condns, car, licence, days, daycount, valid_spla, valid_lahsa)
    # print(applicants)


    for app_id in S_ids:
        for day_no in applicants[app_id][6]:
            parking_dict[day_no] -= 1

    for app_id in L_ids:
        for day_no in applicants[app_id][6]:
            beds_dictionary[day_no] -= 1

    for id in S_ids:
        board_1d[id] = +1

    for id in L_ids:
        board_1d[id] = -1

    return applicants, beds_dictionary, parking_dict, board_1d


def beds_available(id, applicants, beds_dict):
    for day in applicants[id][6]:
        if beds_dict[day] <= 0:
            return False
    return True


def parking_available(id, applicants, parking_dict):
    for day in applicants[id][6] :
        if parking_dict[day]<=0:
            return False
    return True



def candidates_LAHSA(applicants, bed_dict, board_1d):
    candidates = []
    for id in applicants.keys():
        if applicants[id][9] == True  and board_1d[id] == 0 and beds_available(id, applicants, bed_dict):
            candidates.append(id)
    return candidates


def candidates_SPLA(applicants, parking_dict, board_1d):
    candidates = []
    for id in applicants.keys():
        if applicants[id][8] == True and board_1d[id] == 0 and parking_available(id, applicants, parking_dict):
            candidates.append(id)
    return candidates


def evaluate(board_1d, applicants):
    spla_score = 0
    lahsa_score = 0
    for k, v in board_1d.items():
        if v == SPLA:
            spla_score += len(applicants[k][6])
        elif v == LAHSA:
            lahsa_score += len(applicants[k][6])
    return spla_score, lahsa_score



# c = 0
def maximax(board_1d, applicants, parking_dict, bed_dict, depth, turn, spla_score, lahsa_score):
    global caching_lahsa, caching_spla, lahsalist, splalist

    bestScore = ["-1", initial_spla_score, initial_lahsa_score]
    cand_spla = candidates_SPLA(applicants, parking_dict, board_1d)
    cand_lahsa = candidates_LAHSA(applicants, bed_dict, board_1d)
    print(cand_spla, cand_lahsa)

    if cand_spla == [] and cand_lahsa == []:
        return [-1, spla_score, lahsa_score]

    if turn == SPLA:
        candidates = cand_spla
    else:
        candidates = cand_lahsa

    if candidates == [] and turn == 1:
        print("spla empty spla turn")
        key = ",".join(sorted(splalist))+";"+",".join(sorted(lahsalist))
        if key in caching_spla:
            s = int(caching_spla[key].split(",")[0])
            l = int(caching_spla[key].split(",")[1])
            score = ["-1",s,l]
        else:
            score = maximax(board_1d, applicants, parking_dict,bed_dict, depth, -turn, spla_score, lahsa_score)
            caching_spla[key] = str(score[1])+","+str(score[2])
        print("score", score)
        return score

    elif candidates == [] and turn == -1:
        print("lahsa empty lahsa turn")
        key = ",".join(sorted(splalist))+";"+",".join(sorted(lahsalist))
        if key in caching_lahsa:
            s = int(caching_lahsa[key].split(",")[0])
            l = int(caching_lahsa[key].split(",")[1])
            score = ["-1",s,l]
        else:
            score = maximax(board_1d, applicants, parking_dict,bed_dict, depth, -turn, spla_score, lahsa_score)
            caching_lahsa[key] = str(score[1])+","+str(score[2])
        return score

    for cand in candidates:
        print("cand", cand)

        cand_score = applicants[cand][7]
        board_1d[cand] = turn

        if turn == SPLA:
            splalist.append(cand)

            spla_score += cand_score
            for day in applicants[cand][6]:
                parking_dict[day] -= 1
            l1 = splalist[:]
            l2 = lahsalist[:]
            key = ",".join(sorted(l1))+";"+",".join(sorted(l2))
            if key in caching_spla:
                s = int(caching_spla[key].split(",")[0])
                l = int(caching_spla[key].split(",")[1])
                score = ["-1",s,l]
            else:
                score = maximax(board_1d, applicants, parking_dict,bed_dict, depth, -turn, spla_score, lahsa_score)
                caching_spla[key] = str(score[1])+","+str(score[2])

            board_1d[cand] = 0
            splalist.pop()

            score[0] = cand
            spla_score -= cand_score
            for day in applicants[cand][6]:
                parking_dict[day] += 1

            print(cand,score)
            if score[1] > bestScore[1]:
                bestS core = score
            elif score[1] == bestScore[1] and int(score[0]) < int(bestScore[0]):
                print(score)
                bestScore = score

        else:
            lahsalist.append(cand)
            lahsa_score += cand_score
            for day in applicants[cand][6]:
                bed_dict[day] -= 1
            key = ",".join(sorted(splalist))+";"+",".join(sorted(lahsalist))
            if key in caching_lahsa:
                s = int(caching_lahsa[key].split(",")[0])
                l = int(caching_lahsa[key].split(",")[1])
                score = ["-1",s,l]

            else:
                score = maximax(board_1d, applicants, parking_dict,bed_dict, depth, -turn, spla_score, lahsa_score)
                caching_lahsa[key] = str(score[1])+","+str(score[2])
            board_1d[cand] = 0
            lahsalist.pop()
            board_1d[cand] = 0

            lahsa_score -= cand_score
            for day in applicants[cand][6]:
                bed_dict[day] += 1

            if score[2] > bestScore[2]:
                bestScore = score
            elif score[2] == bestScore[2] and int(score[0]) < int(bestScore[0]):
                print(score)
                bestScore = score
    return bestScore


st = time.time()

SPLA = +1
LAHSA = -1

applicantss, bed_dicts, parking_dicts, board_1d = read_input()
initial_spla_score, initial_lahsa_score = evaluate(board_1d, applicantss)
# initial_spla_score = 0
# initial_lahsa_score = 0
caching_spla = {}
caching_lahsa  = {}
splalist = []
lahsalist = []
ans = maximax(board_1d, applicantss, parking_dicts, bed_dicts, 90, SPLA, initial_spla_score, initial_lahsa_score)
print(ans)
# print(type(ans[0]))

with open("output.txt", "w") as outfile:
    outfile.write(str(ans[0]))

print(time.time()-st)
print("submit")

