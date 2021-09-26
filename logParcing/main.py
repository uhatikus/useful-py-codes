from pathlib import Path
import json


def get_all():
    log_dir = 'logs_kraski2'
    # dict_fields = ["AGE", "CITY", "EMAIL", "ESSAY", "essayFileName", "essayOldFileName", "essayText", "essayTitle", "fileName", "NAME", "oldFileName", "SCHOOL", "SUPERVISOR", "supervisorContacts", "supervisorFIO", "SURNAME", "TIME", "TITLE"]
    bools = ["true", "false"]
    All = {}
    key_word = "PARTICIPANT"
    parts = ["ART",  "PHOTOS", "MUSIC", "DANCE", "PROFESSIONAL", "SCIENTIFIC", "LITERATURE"]
    All_inserts = [i + key_word for i in parts]
    All_inserts.append("PARTICIPANTFILE")
    All_inserts.append("IMAGEVERSION")
    All_inserts.append("NEWS")
    All_inserts.append("RASKRASKA")
    All_inserts.append("STORIES")


    for insert_name in All_inserts:
        All[insert_name] = []
    for p in list(Path(log_dir).iterdir()):#[0:3]
        if p.is_file() and ".DS" not in str(p):
            print(str(p))

            filei = open(p, 'r')
            lines = filei.readlines()
            for line in lines:
                if "?, ?, ?" in line:
                     print(line)
                     continue
                for insert_name in All_inserts:
                    if "INSERT INTO " + insert_name in line:

                        
                        fields = line.split(" VALUES ")[0][(len("INSERT INTO "+insert_name)+7):-1].replace("'", "").replace('"', '').split(", ")
                        # info = line.split(" VALUES ")[1][1:-2].replace("'", "").replace('"', '').split(", ")
                        info  = line.split(" VALUES ")[1][1:-2]

                    
                        if "IMAGEVERSION" in insert_name:
                            info = info.replace(", ","&&&").replace("'", "").replace('"', '').split("&&&")
                        else:
                            info = info.replace("', '","&&&").replace(", '","&&&").replace("', ","&&&").replace("'", "").replace('"', '').split("&&&")



                        # print(info)
                        # raise Exception("SASs")
                        info = [int(inf) if inf.isdigit() else inf.strip() for inf in info]
                        info = [(True if inf == bools[0] else False) if inf in bools else inf for inf in info]
                        # print(fields)
                        # print()
                        # print(info)
                        
                        PARTICIPANT = {}
                        flag = False
                        for k, field in enumerate(fields):
                            if field == "TITLE":
                                if "2020-" in str(info[k]):
                                    print(line)
                                    print(len(fields))
                                    print(len(info))
                                    flag = True

                            # if field == "TIME":
                            #     print(info[k])
                            #     if "2019-" in info[k]:
                            #         continue
                            #     if "2020-01" in info[k]:
                            #         continue
                            PARTICIPANT[field] = info[k]
                            # print(PARTICIPANT)
                            if flag or len(fields) != len(info):
                                # if "2020-" in str(info[k]):
                                print(line)
                                print(fields)
                                print(info)
                                raise Exception("SASs")


                        All[insert_name].append(PARTICIPANT)


    with open("all_kraski2_1.json", 'w') as f:

        # simplejson.dumps(simplejson.loads(output), indent=4, sort_keys=True))

        json.dump(All, f, indent=4, sort_keys=True)


# def get_participants():

#     log_dir = 'logs_kraski'
#     # dict_fields = ["AGE", "CITY", "EMAIL", "ESSAY", "essayFileName", "essayOldFileName", "essayText", "essayTitle", "fileName", "NAME", "oldFileName", "SCHOOL", "SUPERVISOR", "supervisorContacts", "supervisorFIO", "SURNAME", "TIME", "TITLE"]
#     bools = ["true", "false"]
#     PARTICIPANTS = {}
#     parts = ["ART",  "PHOTOS", "MUSIC", "DANCE", "PROFESSIONAL", "SCIENTIFIC", "LITERATURE"]

#     for part in parts:
#         PARTICIPANTS[part] = []
#     for p in list(Path(log_dir).iterdir()):#[0:3]
#         if p.is_file() and ".DS" not in str(p):
#             print(str(p))

#             filei = open(p, 'r')
#             lines = filei.readlines()
#             for line in lines:
#                 for part in parts:
#                     if "INSERT INTO "+part+"PARTICIPANT" in line:

                        
#                         fields = line.split(" VALUES ")[0][(len("INSERT INTO "+part+"PARTICIPANT")+7):-1].replace("'", "").replace('"', '').split(", ")
#                         # info = line.split(" VALUES ")[1][1:-2].replace("'", "").replace('"', '').split(", ")
#                         info = line.split(" VALUES ")[1][1:-2].replace("', '","&&&").replace(", '","&&&").replace("', ","&&&").replace("'", "").replace('"', '').split("&&&")
#                         # print(info)
#                         # raise Exception("SASs")
#                         info = [int(inf) if inf.isdigit() else inf.strip() for inf in info]
#                         info = [(True if inf == bools[0] else False) if inf in bools else inf for inf in info]
#                         # print(fields)
#                         # print()
#                         # print(info)
                        
#                         PARTICIPANT = {}
#                         flag = False
#                         for k, field in enumerate(fields):
#                             if field == "TITLE":
#                                 if "2020-" in str(info[k]):
#                                     print(line)
#                                     print(len(fields))
#                                     print(len(info))
#                                     flag = True

#                             # if field == "TIME":
#                             #     print(info[k])
#                             #     if "2019-" in info[k]:
#                             #         continue
#                             #     if "2020-01" in info[k]:
#                             #         continue
#                             PARTICIPANT[field] = info[k]
#                             # print(PARTICIPANT)
#                             if flag or len(fields) != len(info):
#                                 raise Exception("SASs")


#                         PARTICIPANTS.append(PARTICIPANT)


#     with open("participants_kraski.json", 'w') as f:

#         # simplejson.dumps(simplejson.loads(output), indent=4, sort_keys=True))

#         json.dump(PARTICIPANTS, f, indent=4, sort_keys=True)


# def get_imageversions():

#     log_dir = 'logs_kraski'
#     # dict_fields = ["AGE", "CITY", "EMAIL", "ESSAY", "essayFileName", "essayOldFileName", "essayText", "essayTitle", "fileName", "NAME", "oldFileName", "SCHOOL", "SUPERVISOR", "supervisorContacts", "supervisorFIO", "SURNAME", "TIME", "TITLE"]
#     bools = ["true", "false"]
#     PARTICIPANTS = []

#     for p in list(Path(log_dir).iterdir()):#[0:3]
#         if p.is_file() and ".DS" not in str(p):
#             print(str(p))

#             filei = open(p, 'r')
#             lines = filei.readlines()
#             for line in lines:
#                 if "INSERT INTO IMAGEVERSIONS" in line:

                    
#                     fields = line.split(" VALUES ")[0][32:-1].replace("'", "").replace('"', '').split(", ")
#                     # info = line.split(" VALUES ")[1][1:-2].replace("'", "").replace('"', '').split(", ")
#                     info = line.split(" VALUES ")[1].split(")")[0][1:0].replace(", ","&&&").replace("'", "").replace('"', '').split("&&&")
#                     # print(info)

#                     # raise Exception("SASs")
#                     info = [int(inf) if inf.isdigit() else inf.strip() for inf in info]
#                     info = [(True if inf == bools[0] else False) if inf in bools else inf for inf in info]
#                     print(fields)
#                     # print()
#                     print(info)
                    
#                     PARTICIPANT = {}
#                     flag = False
#                     for k, field in enumerate(fields):
#                         if field == "TITLE":
#                             if "2020-" in str(info[k]):
#                                 print(line)
#                                 print(len(fields))
#                                 print(len(info))
#                                 flag = True

#                         # if field == "TIME":
#                         #     print(info[k])
#                         #     if "2019-" in info[k]:
#                         #         continue
#                         #     if "2020-01" in info[k]:
#                         #         continue
#                         PARTICIPANT[field] = info[k]
#                         # print(PARTICIPANT)
#                         if flag or len(fields) != len(info):
#                             raise Exception("SASs")


#                     PARTICIPANTS.append(PARTICIPANT)


#     with open("imageversions_kraski.json", 'w') as f:

#         # simplejson.dumps(simplejson.loads(output), indent=4, sort_keys=True))

#         json.dump(PARTICIPANTS, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    get_all()
    # get_imageversions()
    # get_participants()
